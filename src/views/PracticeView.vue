<template>
    <h1 class="text-4xl font-semibold my-14 hover:scale-125 duration-150 text-text-color">Span Racer</h1>
    <span v-if="text">
        <CipherAnalysisComponent :text="text" @letterChange="sendChangedLetter"/>
    </span>
    <span v-else>
        loading...
    </span>
</template>

<script setup lang="ts">
    import CipherAnalysisComponent from '../components/CipherAnalysisComponent.vue';
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
    async function setupText() {
        const response = await axios.get("/api/practice");
        console.log(response.data);
        text.value = response?.data?.text;
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
        const message = Protocol.Encrypt.changeLetter(originLetter, gussedLetter);
        console.log(message);
        socket?.send(message);
    }
</script>
