<template>
    <main class="flex flex-col items-center">
    <div id="textbox" class="border-accent-color border-2 border-opacity-20 rounded-xl border- bg-secondary-color text-ignore-color flex flex-wrap justify-between gap-x-2 text-xl font-mono h-96 aspect-video p-8 shadow-lg shadow-slate-900 py-0">
        <Switch @toggle="textUtil.hiddenModeActive.value = !textUtil.hiddenModeActive.value" />
        <span v-for="word in textUtil.text.split(' ')">
            <span v-for="letter in word">
                <LetterComponent :letter="letter"/>
            </span>
        </span>
    </div>

    <div id="letter-bank" class="flex w-full justify-around">
        <span v-for="letter in textUtil.alphabet" class="text-accent-color font-bold" :class="{'letter-bank--guessed': letterBank[letter].count > 0}">
            {{ letter }}
        </span>
    </div>

    <AnalysisTools/>
    </main>
</template>

<script setup>
    import {ref, reactive} from 'vue'
    import Switch from '../components/Switch.vue'
    import AnalysisTools from '../components/AnalysisTools.vue'
    import LetterComponent from '../components/LetterComponent.vue'
    import ElementBorder from '../components/ElementBorder.vue'
    import textUtil from '../tools/TextUtil'

    const props = defineProps({
        text: String
    });

    const emit = defineEmits(["letterChange"]);
    var letter = '';
    if (props.text)
        textUtil.setText(props.text);
    else
        textUtil.setText("DJ DK C QLXDWI WF SDGDU PCX. XLRLU KQCSLKBDQK, KJXDHDET FXWZ C BDIILE RCKL, BCGL PWE JBLDX FDXKJ GDSJWXO CTCDEKJ JBL LGDU TCUCSJDS LZQDXL. IYXDET JBL RCJJUL, XLRLU KQDLK ZCECTLI JW KJLCU KLSXLJ QUCEK JW JBL LZQDXL’K YUJDZCJL PLCQWE, JBL ILCJB KJCX, CE CXZWXLI KQCSL KJCJDWE PDJB LEWYTB QWPLX JW ILKJXWO CE LEJDXL QUCELJ. QYXKYLI RO JBL LZQDXL’K KDEDKJLX CTLEJK, QXDESLKK ULDC XCSLK BWZL CRWCXI BLX KJCXKBDQ, SYKJWIDCE WF JBL KJWULE QUCEK JBCJ SCE KCGL BLX QLWQUL CEI XLKJWXL FXLLIWZ JW JBL TCUCVO…");


    // const text = "JVUI LUMNCJUIG KCL GIXVGEIS XO KPL KOYI AJCEIX OQ XCXOOPEI PE CE CXXIYAX XO GILWVI KPL QGPIES KCE LOJO QGOY XKI WJVXWKIL OQ XKI DPJI TCETLXIG BCHHC XKI KVXX. JPXXJI SOIL JVUI UEON XKCX XKI TCJCWXPW IYAPGI KCL LIWGIXJM HITVE WOELXGVWXPOE OE C EIN CGYOGIS LACWI LXCXPOE IDIE YOGI AONIGQVJ XKCE XKI QPGLX SGICSIS SICXK LXCG. NKIE WOYAJIXIS, XKPL VJXPYCXI NICAOE NPJJ LAIJJ WIGXCPE SOOY QOG XKI LYCJJ HCES OQ GIHIJL LXGVTTJPET XO GILXOGI QGIISOY XO XKI TCJCZM…";
    // const text = "“OK OH R WRFD KOIS QPF KNS FSTSJJOPX. RJKNPAGN KNS WSRKN HKRF NRH TSSX WSHKFPCSW, OIBSFORJ KFPPBH NRYS WFOYSX KNS FSTSJ QPFMSH QFPI KNSOF NOWWSX TRHS RXW BAFHASW KNSI RMFPHH KNS GRJREC. SYRWOXG KNS WFSRWSW OIBSFORJ HKRFQJSSK, R GFPAB PQ QFSSWPI QOGNKSFH JSW TC JADS HDCVRJDSF NRH SHKRTJOHNSW R XSV HSMFSK TRHS PX KNS FSIPKS OMS VPFJW PQ NPKN. KNS SYOJ JPFW WRFKN YRWSF, PTHSHHSW VOKN QOXWOXG CPAXG HDCVRJDSF, NRH WOHBRKMNSW KNPAHRXWH PQ FSIPKS BFPTSH OXKP KNS QRF FSRMNSH PQ HBRMS…”";
    // const text = "HDD NKWGT, GFNF KT WQFY. SHG. XGHT XQZDJ K YHL? K BQZDJ NFHDDL WFT KS TNQZMDF. KT'Y H MFF DHX LQZ'NF SQT YZIIQYFJ TQ THDU TQ H GZCHS. K BHS'T MFDKFEF K'C JQKSW TGKY. K'EF WQT TQ. QG, K BHS'T JQ KT. BQCF QS! SQ. LFY. SQ. JQ KT. K BHS'T. GQX YGQZDJ K YTHNT KT?  'LQZ DKUF VHRR?' SQ, TGHT'Y SQ WQQJ. GFNF YGF BQCFY! YIFHU, LQZ AQQD! K'C YQNNL. LQZ'NF THDUKSW. LFY, K USQX. LQZ'NF THDUKSW! K'C YQ YQNNL. SQ, KT'Y QU. KT'Y AKSF. K USQX K'C JNFHCKSW MZT K JQS'T NFBHDD WQKSW TQ MFJ.";
    const letterBank = ref(
        {
            'A': { 'count': 0 }, 'B': { 'count': 0 }, 'C': { 'count': 0 }, 'D': { 'count': 0 }, 'E': { 'count': 0 }, 'F': { 'count': 0 }, 'G': { 'count': 0 }, 'H': { 'count': 0 }, 'I': { 'count': 0 }, 'J': { 'count': 0 }, 'K': { 'count': 0 }, 'L': { 'count': 0 }, 'M': { 'count': 0 }, 'N': { 'count': 0 }, 'O': { 'count': 0 }, 'P': { 'count': 0 }, 'Q': { 'count': 0 }, 'R': { 'count': 0 }, 'S': { 'count': 0 }, 'T': { 'count': 0 }, 'U': { 'count': 0 }, 'V': { 'count': 0 }, 'W': { 'count': 0 }, 'X': { 'count': 0 }, 'Y': { 'count': 0 }, 'Z': { 'count': 0 }, 
        }
    );
    document.addEventListener('keyup', keypress);

    function keypress(event) {
        if (!textUtil.selectedLetter.value)
            return;
        const letter = event.key.toUpperCase();
        if (textUtil.isLetter(letter)) {
            letterBank.value[letter].count++;
            var letterObject = textUtil.lettersState.value[textUtil.selectedLetter.value];
            if (letterObject.isGuessed)
                letterBank.value[letterObject.display].count--;
            letterObject.display = letter;
            letterObject.isGuessed = true;

            let originLetter = textUtil.selectedLetter.value
            emit("letterChange", originLetter, letter)
        }
        else if (letter == 'BACKSPACE') {
            let originLetter = textUtil.selectedLetter.value
            var letterObject = textUtil.lettersState.value[originLetter]
            if (letterObject.isGuessed)
                letterBank.value[letterObject.display].count--;
            letterObject.display = originLetter;
            letterObject.isGuessed = false;
            emit("letterChange", originLetter, originLetter)
        }
        else if (letter == 'ESCAPE')
            textUtil.selectedLetter.value = '';
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

    .selected {
        @apply bg-pink-500 text-primary-color rounded-sm font-normal;
    }

</style>