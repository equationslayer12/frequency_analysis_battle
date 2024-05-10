<template>
    <div id="background" class="bg-gradient-to-b from-background-color to-black text-center flex flex-col items-center h-screen">
        <h1 class="my-xl text-4xl font-semibold hover:scale-125 duration-150 text-text-color">Waiting for Players...</h1>
        <span class="mx-2xl max-w-race-width md:w-race-width">
            <ClientProgressBar class="mb-md"/>
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
    import { game } from '@/game/Game';
    import CipherAnalysisComponent from '@/components/CipherAnalysisComponent.vue';
    import ClientProgressBar from '@/components/progress_bar/ClientProgressBar.vue';
    import { webClient } from '@/webclient/WebClient';
    import Protocol from '@/webclient/Protocol';
    
    game.reset();
    game.setText('Waiting for other players to connect...', 16);
    
    let text = game.text;
    
    joinGame()

    async function joinGame() {
        await webClient.socket.connectToServer('/race/join');
        const textLength = webClient.socket.sendAndReceive(Protocol.Request.textLength)
    }
    
    
    </script>