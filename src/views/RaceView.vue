<template>
    <div id="background" class="bg-gradient-to-b from-background-color to-black text-center flex flex-col items-center h-screen">

        <h1 v-if="gameStatus == QUEUE" class="my-xl text-4xl font-semibold hover:scale-125 duration-150 text-text-color">Waiting for Players...</h1>
        <h1 v-else-if="gameStatus == COUNTDOWN" class="my-xl text-4xl font-semibold hover:scale-125 duration-150 text-text-color">
            Get ready!
            <!-- here should be the countdown animation -->
        </h1>
        <h1 v-else class="my-xl text-4xl font-semibold hover:scale-125 duration-150 text-text-color">SPAN RACER</h1>
        
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
    import { COUNTDOWN, COUNTDOWN_TIME, ONGOING, QUEUE } from '@/Constants';
    
    game.reset();
    game.setText('Waiting for other players to connect...', 0);
    
    let text = game.text;
    
    joinGame();
    // waitInQueue();

    /**
     * connect to server and enter a race.
     * get the race's text length (cipherLettersCount)
     */
    async function joinGame() {
        await webClient.socket.connectToServer('/race/join');
        
        const textLengthResponse = await webClient.socket.receive()
        const textLength = Protocol.Response.textLength(textLengthResponse)
        game.setTextLength(textLength); // text
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

            const event = info[0];

            if (event == Protocol.Response.Event.UpdateExistingPlayers) {
                for (let i = 1; i < info.length; i++) {
                    const username = info[i];
                    game.createOpponent(username)
                }
            }
            else if (event == Protocol.Response.Event.PlayerJoined) {
                const username = info[1];
                game.createOpponent(username);
            }
            else if (event == Protocol.Response.Event.PlayerLeft) {
                const username = info[1];
                game.removeOpponent(username);
            }
            else if (event == Protocol.Response.Event.StartCountdown) {

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
                    }
                )
            }
        }
    }

    async function getText() {
        return await webClient.socket.sendAndReceive(Protocol.Request.text);
    }

    async function sendChangedLetter(originLetter: string, gussedLetter: string) {
        
    }
    </script>