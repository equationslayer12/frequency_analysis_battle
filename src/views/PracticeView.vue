<template>
<div id="background" class="bg-gradient-to-b from-background-color to-black text-center flex flex-col items-center h-screen">
    <h1 class="my-xl text-4xl font-semibold hover:scale-125 duration-150 text-text-color">Span Racer</h1>
    <PinkButton v-if="gameStatus == ENDED">Congratulations!</PinkButton>
    <span v-if="game.text.value" class="mx-2xl max-w-race-width md:w-race-width">
        <ClientProgressBar class="mb-md"/>
        <CipherAnalysisComponent @letterChange="sendChangedLetter"/>
    </span>
    <span v-else>
        loading...
    </span>
    <PinkButton @click="newText()">New Text</PinkButton>
</div>
</template>

<script setup lang="ts">
    import { game, gameStatus } from '@/game/Game';
    import ClientProgressBar from '@/components/progress_bar/ClientProgressBar.vue';
    import CipherAnalysisComponent from '@/components/CipherAnalysisComponent.vue';
    import PinkButton from '@/components/pinkButton.vue'
    import Protocol from '@/webclient/Protocol'
    import { webClient } from '@/webclient/WebClient';
    import SocketClient from '@/webclient/SocketClient';
import { ENDED } from '@/Constants';

    let socketClient: SocketClient = new SocketClient();
    
    init();
    async function init() {
        await setupText();
        await connectToServerSocket();
    }
    async function restartPractice() {
        game.reset();
        await init();
    }
    async function setupText() {
        const response = await webClient.APIRequest("/practice");
        const text = response?.text;
        const cipheredLettersCount = response?.cipheredLettersCount;
        if (text === undefined || cipheredLettersCount === undefined)
            return null

        game.setText(text, cipheredLettersCount);
        game.start()
    }
    async function connectToServerSocket() {
        console.log("start connecting")
        await socketClient.connectToServer('/practice');
    }
    async function sendChangedLetter(originLetter: string, gussedLetter: string) {
        if (!socketClient.isConnected())
            return

        const request = Protocol.Request.changeLetter(originLetter, gussedLetter);
        const response = await socketClient.sendAndReceive(request);

        console.log(response);
        if (!response)
            return

        if (response === Protocol.GAME_ENDED) {
            console.log("haha ended YESSS");
            socketClient.disconnect();
            game.endGame();
        }
        else {
            game.textState.totalLettersGuessed.value = parseInt(response);
        }
    }

    async function newText() {
        if (!socketClient.isConnected()) {
            restartPractice();
            return
        }
        console.log("receiving new text");

        const request = Protocol.Request.newText;
        const response = await socketClient.sendAndReceive(request);

        socketClient.disconnect();
        restartPractice();

    }
    /**
     * the more the text is solved, the greener the background is.
     * this function calculates this color
     * @param point between 0-1, how much close the result will be to the solved color
     */
    // function BgToSolvedRange(point: number) {
    //     const bgColor = 
    // }
</script>
