<template>
    <div id="background" class="bg-gradient-to-b from-background-color to-black text-center flex flex-col items-center h-screen">

        <h1 v-if="gameStatus == QUEUE" class="my-xl text-4xl font-semibold hover:scale-125 duration-150 text-text-color">Waiting for Players...</h1>
        <h1 v-else-if="gameStatus == COUNTDOWN" class="my-xl text-4xl font-semibold hover:scale-125 duration-150 text-text-color">
            Get ready!
            <!-- here should be the countdown animation -->
        </h1>
        <h1 v-else class="my-xl text-4xl font-semibold hover:scale-125 duration-150 text-text-color">SPAN RACER</h1>
        <PinkButton v-if="game.is_finished.value">Congratulations!</PinkButton>
        
        <span class="mx-2xl max-w-race-width md:w-race-width">
            <!-- <span class="text-text-color text-lg" v-for="(opponent, username) in opponents">{{ opponent.player }}</span> -->
            <ClientProgressBar class="mb-md" />
            <OpponentProgressBar class="mb-md" v-for="(opponent, username) in opponents" :opponent="opponent.player" />
            <span v-if="text">
                <CipherAnalysisComponent @letterChange="sendChangedLetter"/>
            </span>
            <span v-else>
                <CipherAnalysisComponent @letterChange=""/>
            </span>
        </span>
    </div>
    </template>
    
    <script setup lang="ts">
    import { cipheredLettersCount, game, opponents, gameStatus } from '@/game/Game';
    import CipherAnalysisComponent from '@/components/CipherAnalysisComponent.vue';
    import ClientProgressBar from '@/components/progress_bar/ClientProgressBar.vue';
    import { webClient } from '@/webclient/WebClient';
    import Protocol from '@/webclient/Protocol';
    import OpponentProgressBar from '@/components/progress_bar/OpponentProgressBar.vue';
    import { COUNTDOWN, ENDED, ONGOING, QUEUE, SYNC_DATA_DELAY } from '@/Constants';
    import PinkButton from '@/components/pinkButton.vue';

    game.reset();
    game.setText('Waiting for other players to connect...', 0);
    
    let text = game.text;
    
    let socketLock = false;
    
    joinGame();

    /**
     * connect to server and enter a race.
     * get the race's text length (cipherLettersCount)
     */
    async function joinGame() {
        await webClient.socket.connectToServer('/race/join');
        
        const textLengthResponse = await webClient.socket.receive()
        const textLength = Protocol.Response.textLength(textLengthResponse)
        game.setTextLength(textLength);
        await webClient.socket.send(Protocol.success)
        
        await waitInQueue();
    }

    /**
     * constantly update information about users, and then init countdown when game is ready.
     */
    async function waitInQueue() {
        while (game.status.value == QUEUE) {
            console.log("waiting in da queue");

            const queueInfoResponse = await webClient.socket.receive();
            const info = Protocol.Response.splitResponse(queueInfoResponse);

            console.log(`receiving in da queue: ${info}`);
            
            await handleQueueResponse(info);
        }
    }

    async function handleQueueResponse(info: string[]) {
        const event = info[0];

        switch (event) {
            case Protocol.Response.Event.UpdateExistingPlayers:
                updateExistingPlayers(info);
                break;
            case Protocol.Response.Event.PlayerJoined:
                playerJoined(info);
                break;
            case Protocol.Response.Event.PlayerLeft:
                playerLeft(info);
                break;
            case Protocol.Response.Event.StartCountdown:
                await startCountdown();
                break;
            default:
                console.warn(`Unhandled event: ${event}`);
        }
    }

    function updateExistingPlayers(info: string[]) {
        for (let i = 1; i < info.length; i+=2) {
            const username = info[i];
            const userId = Number(info[i+1]);

            game.createOpponent(username, userId)
        }
    }

    function playerJoined(info: string[]) {
        const username = info[1];
        const userId = Number(info[2]);
        game.createOpponent(username, userId);
    }

    function playerLeft(info: string[]) {
        const userId = Number(info[1]);
        game.removeOpponent(userId);
    }

    async function startCountdown() {
        const countdown = game.startCountdown();
        game.setText("", cipheredLettersCount.value)
        const text = await getText();
        console.log("ahaha the text is:");
        console.log(text);

        countdown.then(
            (data) => {
                console.log("oh boy we are starting!");
                game.setText(text, cipheredLettersCount.value)
                game.start();
                sync_data_with_server()
            }
        )
    }

    /**
     * every second send a request to sync the data.
     */
    async function sync_data_with_server() {
        while (webClient.socket.isConnected()) {
            await game.sleep(SYNC_DATA_DELAY * 1000);
            
            const request = Protocol.Request.syncData;

            const response = await webClient.socket.sendAndReceive(request);
            const data = Protocol.Response.sync(response)

            handleSyncResponse(data);
        }
    }

    async function handleSyncResponse(data: {
        gameStatus: string;
        userIds: number[];
        scores: number[];
    }) {
        const gameStatus = data.gameStatus;
        const userIds = data.userIds;
        const userScores = data.scores;

        console.log(gameStatus);
        updatePlayerScores(userIds, userScores);

        if (gameStatus == ENDED) {
            await endGame();
        }
    }

    function updatePlayerScores(userIds: number[], userScores: number[]) {
        for (let i = 0; i < userIds.length; i++) {
            const user_id: number = userIds[i];
            let user_score: number = userScores[i];
            if (user_score == Protocol.FINISHED)
                user_score = game.cipheredLettersCount.value

            // set user_id's score to be user_score
            const player = game.opponents.value[user_id].player;
            if (player != undefined)
                player.progress.current = user_score;
        }
    }

    async function getText() {
        return await webClient.socket.sendAndReceive(Protocol.Request.text);
    }

    async function endGame() {
        await webClient.socket.disconnect();
        game.endGame();
    }
    async function sendChangedLetter(originLetter: string, gussedLetter: string) {
        if (!webClient.socket.isConnected())
            return
        
        if (game.is_finished.value)
            return

        const request = Protocol.Request.changeLetter(originLetter, gussedLetter);
        const response = await webClient.socket.sendAndReceive(request);
        if (!response)
            return

        console.log(response);
        
        if (response == Protocol.FINISHED.toString()) {
            console.log("gg");
            game.finishGame();
            return;
        }
        try {
            game.textState.totalLettersGuessed.value = parseInt(response);
        } catch {
            return
        }
    }
</script>
