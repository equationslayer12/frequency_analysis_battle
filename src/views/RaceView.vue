<template>
    <div id="background" class="bg-gradient-to-b from-background-color to-black text-center flex flex-col items-center h-screen">

        <h1 v-if="gameStatus == QUEUE" class="my-xl text-4xl font-semibold hover:scale-125 duration-150 text-text-color">Waiting for Players...</h1>
        <h1 v-else-if="gameStatus == COUNTDOWN" class="my-xl text-4xl font-semibold hover:scale-125 duration-150 text-text-color">Get ready!</h1>
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
    import { COUNTDOWN, COUNTDOWN_TIME, QUEUE } from '@/Constants';
    
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
            else if (event == Protocol.Response.Event.GameIsStarting) {
                /**
                 * 1. Server sent game is starting event.
                 * 2. Start measuring time.
                 * 3. Receive text from server.
                 * 4. Wait for (3 seconds - already passed seconds)
                 * 5. Set the text and start the game.
                 */
                const startTime = Date.now();
                game.startCountdown();  // start countdown animation

                const text = await getText();
                const elapsedTime = (Date.now() - startTime);
                
                const timeToSleep = COUNTDOWN_TIME - elapsedTime;
                console.log(`Sleeping for ${timeToSleep} seconds`);
                if (timeToSleep > 0)
                    await sleep(timeToSleep * 1000)
                console.log("Starting!")

                game.setText(text, cipheredLettersCount.value)
                game.start();
            }
        }
    }

    async function getText() {
        return await webClient.APIRequest("/race/text");
    }

    async function sendChangedLetter(originLetter: string, gussedLetter: string) {
        
    }
    
    /**
     * delay.
     * @param ms milliseconds to delay
     */
    async function sleep(ms: number) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }


    </script>