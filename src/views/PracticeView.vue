<template>
<div id="background" class="bg-gradient-to-b from-background-color to-black text-center flex flex-col items-center h-screen">
    <h1 class="text-4xl font-semibold my-14 hover:scale-125 duration-150 text-text-color">Span Racer</h1>
    <span v-if="text">
        <CipherAnalysisComponent :text="text" @letterChange="sendChangedLetter"/>
    </span>
    <span v-else>
        loading...
    </span>
    <PinkButton @click="newText()">New Text</PinkButton>
</div>
</template>

<script setup lang="ts">
    import { cipheredLettersCount, lettersGuessed, textUtilReset } from '@/tools/TextUtil';
    import CipherAnalysisComponent from '../components/CipherAnalysisComponent.vue';
    import PinkButton from '../components/pinkButton.vue'
    import Protocol from '../tools/Protocol'
    import axios from 'axios'
    import {ref} from 'vue'

    // const text = "DJ DK C QLXDWI WF SDGDU PCX. XLRLU KQCSLKBDQK, KJXDHDET FXWZ C BDIILE RCKL, BCGL PWE JBLDX FDXKJ GDSJWXO CTCDEKJ JBL LGDU TCUCSJDS LZQDXL. IYXDET JBL RCJJUL, XLRLU KQDLK ZCECTLI JW KJLCU KLSXLJ QUCEK JW JBL LZQDXL’K YUJDZCJL PLCQWE, JBL ILCJB KJCX, CE CXZWXLI KQCSL KJCJDWE PDJB LEWYTB QWPLX JW ILKJXWO CE LEJDXL QUCELJ. QYXKYLI RO JBL LZQDXL’K KDEDKJLX CTLEJK, QXDESLKK ULDC XCSLK BWZL CRWCXI BLX KJCXKBDQ, SYKJWIDCE WF JBL KJWULE QUCEK JBCJ SCE KCGL BLX QLWQUL CEI XLKJWXL FXLLIWZ JW JBL TCUCVO…";
    const text = ref('');
    var socket: WebSocket | null = null;

    
    init();
    async function init() {
        await setupText();
        await connectToServerSocket();
    }
    async function restartPractice() {
        text.value = '';
        textUtilReset();
        await init();
    }
    async function setupText() {
        const response = await axios.get("/api/practice");
        console.log(response.data);
        text.value = response?.data?.text;
        cipheredLettersCount.value = response?.data?.cipheredLettersCount

        if (text)
            return text;
        else
            return null;
    }
    async function connectToServerSocket() {
        console.log("start connecting")
        var ws = new WebSocket('ws://localhost:8080/api/practice')
        ws.onopen = (event) => {
            console.log("Connected to server socket");
            socket = ws;
        };
    }
    async function sendChangedLetter(originLetter: string, gussedLetter: string) {
        if (socket == null)
            return

        const message = Protocol.Request.changeLetter(originLetter, gussedLetter);
        socket.onmessage = (event) => {
            console.log(event.data);
            if (event.data === Protocol.GAME_ENDED)
                console.log("haha ended YESSS");
            lettersGuessed.value = parseInt(event.data);
        }
        socket.send(message);
    }

    async function newText() {
        if (socket == null) {
            restartPractice();
            return
        }
        console.log("receiving new text");
        const message = Protocol.Request.newText;
        socket.onmessage = async (event) => {
            socket?.close();
            socket = null;
        }
        socket.send(message);
        console.log(`i sent ${message}`);
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
