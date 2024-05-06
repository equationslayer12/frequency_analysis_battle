<template>
    <main class="mx-2xl flex flex-col items-center">
    <ProgressBar :current="totalLettersGuessed" :end="cipheredLettersCount" class="mb-md"></ProgressBar>
    <div id="textbox" class="mb-md max-w-race-width border-text-color border-2 border-opacity-20 rounded-xl bg-primary-color text-ignore-color shadow-lg shadow-slate-900">
        <Switch @toggle="hiddenModeActive = !hiddenModeActive" class="mt-md mb-lg"/>
        <span id="text" class="mb-md mx-xl flex flex-wrap text-xl font-mono justify-between gap-x-2">
            <span v-for="word in game.text.value.split(' ')">
            <span v-for="letter in word">
                <LetterComponent :letter="letter"/>
            </span>
        </span>

        </span>
    </div>

    <div id="letter-bank" class="mb-sm flex w-full justify-around">
        <span v-for="letter in alphabet" class="text-text-color font-bold" :class="{'letter-bank--guessed': lettersState[letter].value.otherLettersGuessedCount > 0}">
            {{ letter }}
        </span>
    </div>

    <AnalysisTools/>
    </main>
</template>

<script setup lang="ts">
    import { alphabet } from '@/Constants'
    import Protocol from '@/webclient/Protocol'
    import Switch from '@/components/Switch.vue'
    import AnalysisTools from '@/components/AnalysisTools.vue'
    import LetterComponent from '@/components/LetterComponent.vue'
    import ProgressBar from '@/components/ProgressBar.vue'
    import { game, totalLettersGuessed, cipheredLettersCount, selectedLetter, lettersState, hiddenModeActive } from '@/game/Game'
    
    const emit = defineEmits(["letterChange"]);
    
    setupTextAnalysis()
    function setupTextAnalysis() {
        if (!game.text)
            game.setText("DJ DK C QLXDWI WF SDGDU PCX. XLRLU KQCSLKBDQK, KJXDHDET FXWZ C BDIILE RCKL, BCGL PWE JBLDX FDXKJ GDSJWXO CTCDEKJ JBL LGDU TCUCSJDS LZQDXL. IYXDET JBL RCJJUL, XLRLU KQDLK ZCECTLI JW KJLCU KLSXLJ QUCEK JW JBL LZQDXL’K YUJDZCJL PLCQWE, JBL ILCJB KJCX, CE CXZWXLI KQCSL KJCJDWE PDJB LEWYTB QWPLX JW ILKJXWO CE LEJDXL QUCELJ. QYXKYLI RO JBL LZQDXL’K KDEDKJLX CTLEJK, QXDESLKK ULDC XCSLK BWZL CRWCXI BLX KJCXKBDQ, SYKJWIDCE WF JBL KJWULE QUCEK JBCJ SCE KCGL BLX QLWQUL CEI XLKJWXL FXLLIWZ JW JBL TCUCVO…", 23);
    }

    // const text = "JVUI LUMNCJUIG KCL GIXVGEIS XO KPL KOYI AJCEIX OQ XCXOOPEI PE CE CXXIYAX XO GILWVI KPL QGPIES KCE LOJO QGOY XKI WJVXWKIL OQ XKI DPJI TCETLXIG BCHHC XKI KVXX. JPXXJI SOIL JVUI UEON XKCX XKI TCJCWXPW IYAPGI KCL LIWGIXJM HITVE WOELXGVWXPOE OE C EIN CGYOGIS LACWI LXCXPOE IDIE YOGI AONIGQVJ XKCE XKI QPGLX SGICSIS SICXK LXCG. NKIE WOYAJIXIS, XKPL VJXPYCXI NICAOE NPJJ LAIJJ WIGXCPE SOOY QOG XKI LYCJJ HCES OQ GIHIJL LXGVTTJPET XO GILXOGI QGIISOY XO XKI TCJCZM…";
    // const text = "“OK OH R WRFD KOIS QPF KNS FSTSJJOPX. RJKNPAGN KNS WSRKN HKRF NRH TSSX WSHKFPCSW, OIBSFORJ KFPPBH NRYS WFOYSX KNS FSTSJ QPFMSH QFPI KNSOF NOWWSX TRHS RXW BAFHASW KNSI RMFPHH KNS GRJREC. SYRWOXG KNS WFSRWSW OIBSFORJ HKRFQJSSK, R GFPAB PQ QFSSWPI QOGNKSFH JSW TC JADS HDCVRJDSF NRH SHKRTJOHNSW R XSV HSMFSK TRHS PX KNS FSIPKS OMS VPFJW PQ NPKN. KNS SYOJ JPFW WRFKN YRWSF, PTHSHHSW VOKN QOXWOXG CPAXG HDCVRJDSF, NRH WOHBRKMNSW KNPAHRXWH PQ FSIPKS BFPTSH OXKP KNS QRF FSRMNSH PQ HBRMS…”";
    // const text = "HDD NKWGT, GFNF KT WQFY. SHG. XGHT XQZDJ K YHL? K BQZDJ NFHDDL WFT KS TNQZMDF. KT'Y H MFF DHX LQZ'NF SQT YZIIQYFJ TQ THDU TQ H GZCHS. K BHS'T MFDKFEF K'C JQKSW TGKY. K'EF WQT TQ. QG, K BHS'T JQ KT. BQCF QS! SQ. LFY. SQ. JQ KT. K BHS'T. GQX YGQZDJ K YTHNT KT?  'LQZ DKUF VHRR?' SQ, TGHT'Y SQ WQQJ. GFNF YGF BQCFY! YIFHU, LQZ AQQD! K'C YQNNL. LQZ'NF THDUKSW. LFY, K USQX. LQZ'NF THDUKSW! K'C YQ YQNNL. SQ, KT'Y QU. KT'Y AKSF. K USQX K'C JNFHCKSW MZT K JQS'T NFBHDD WQKSW TQ MFJ.";
    document.addEventListener('keyup', keypress);

    function keypress(event: any) {
        let fromLetter = selectedLetter.value;
        if (!fromLetter)
            return;
        const toLetter = event.key.toUpperCase();
        if (game.textState.isLetter(toLetter)) {
            game.changeLetter(fromLetter, toLetter);
            emit("letterChange", fromLetter, toLetter)
        }
        else if (toLetter == 'BACKSPACE') {
            game.removeLetter(fromLetter)
            emit("letterChange", fromLetter, Protocol.deleteChar);
        }
        else if (toLetter == 'ESCAPE')
            game.textState.unselectLetter();
    }


</script>

<style scoped>
    .letter-bank--guessed {
        @apply line-through text-ignore-color font-normal;
    }

</style>

<style>
    .guessed {
        @apply text-green-500 font-semibold;
    }

    .duplicate {
        @apply text-yellow-500 font-semibold;
    }

    .selected {
        @apply bg-accent-color text-background-color rounded-sm font-normal;
    }

    ::selection {
        background: magenta;
        color:black
    }
</style>