<template>
    <h1 class="text-4xl font-semibold my-14 hover:scale-125 duration-150 text-accent-color">Span Racer</h1>
    <main class="flex flex-col items-center w-fit">
    <div id="textbox" class="bg-secondary-color text-ignore-color flex flex-wrap justify-between gap-x-2 text-xl font-mono h-96 aspect-video p-8 rounded-xl shadow-lg shadow-slate-900 py-0">
        <Switch @toggle="isHidden = !isHidden" />
        <span v-for="word in text.split(' ')">
            <span v-for="letter in word">
                <LetterComponent @changeSelectedLetter="(newLetter) => selectedLetter = newLetter" :letter="letter" :selectedLetter="selectedLetter" :letters="letters" :isHidden="isHidden"/>
            </span>
        </span>
    </div>
    <AnalysisTools :text="text" :letters="letters" @changeSelectedLetter="(newLetter) => selectedLetter = newLetter" :selectedLetter="selectedLetter" :isHidden="isHidden"/>
    </main>
</template>

<script setup>
    import {ref, reactive} from 'vue'
    import Switch from '../components/Switch.vue'
    import AnalysisTools from '../components/AnalysisTools.vue'
    import LetterComponent from '../components/LetterComponent.vue'

    var letter = '';
    const text = "DJ DK C QLXDWI WF SDGDU PCX. XLRLU KQCSLKBDQK, KJXDHDET FXWZ C BDIILE RCKL, BCGL PWE JBLDX FDXKJ GDSJWXO CTCDEKJ JBL LGDU TCUCSJDS LZQDXL. IYXDET JBL RCJJUL, XLRLU KQDLK ZCECTLI JW KJLCU KLSXLJ QUCEK JW JBL LZQDXL’K YUJDZCJL PLCQWE, JBL ILCJB KJCX, CE CXZWXLI KQCSL KJCJDWE PDJB LEWYTB QWPLX JW ILKJXWO CE LEJDXL QUCELJ. QYXKYLI RO JBL LZQDXL’K KDEDKJLX CTLEJK, QXDESLKK ULDC XCSLK BWZL CRWCXI BLX KJCXKBDQ, SYKJWIDCE WF JBL KJWULE QUCEK JBCJ SCE KCGL BLX QLWQUL CEI XLKJWXL FXLLIWZ JW JBL TCUCVO…";
    // const text = "JVUI LUMNCJUIG KCL GIXVGEIS XO KPL KOYI AJCEIX OQ XCXOOPEI PE CE CXXIYAX XO GILWVI KPL QGPIES KCE LOJO QGOY XKI WJVXWKIL OQ XKI DPJI TCETLXIG BCHHC XKI KVXX. JPXXJI SOIL JVUI UEON XKCX XKI TCJCWXPW IYAPGI KCL LIWGIXJM HITVE WOELXGVWXPOE OE C EIN CGYOGIS LACWI LXCXPOE IDIE YOGI AONIGQVJ XKCE XKI QPGLX SGICSIS SICXK LXCG. NKIE WOYAJIXIS, XKPL VJXPYCXI NICAOE NPJJ LAIJJ WIGXCPE SOOY QOG XKI LYCJJ HCES OQ GIHIJL LXGVTTJPET XO GILXOGI QGIISOY XO XKI TCJCZM…";
    // const text = "“OK OH R WRFD KOIS QPF KNS FSTSJJOPX. RJKNPAGN KNS WSRKN HKRF NRH TSSX WSHKFPCSW, OIBSFORJ KFPPBH NRYS WFOYSX KNS FSTSJ QPFMSH QFPI KNSOF NOWWSX TRHS RXW BAFHASW KNSI RMFPHH KNS GRJREC. SYRWOXG KNS WFSRWSW OIBSFORJ HKRFQJSSK, R GFPAB PQ QFSSWPI QOGNKSFH JSW TC JADS HDCVRJDSF NRH SHKRTJOHNSW R XSV HSMFSK TRHS PX KNS FSIPKS OMS VPFJW PQ NPKN. KNS SYOJ JPFW WRFKN YRWSF, PTHSHHSW VOKN QOXWOXG CPAXG HDCVRJDSF, NRH WOHBRKMNSW KNPAHRXWH PQ FSIPKS BFPTSH OXKP KNS QRF FSRMNSH PQ HBRMS…”";
    // const text = "HDD NKWGT, GFNF KT WQFY. SHG. XGHT XQZDJ K YHL? K BQZDJ NFHDDL WFT KS TNQZMDF. KT'Y H MFF DHX LQZ'NF SQT YZIIQYFJ TQ THDU TQ H GZCHS. K BHS'T MFDKFEF K'C JQKSW TGKY. K'EF WQT TQ. QG, K BHS'T JQ KT. BQCF QS! SQ. LFY. SQ. JQ KT. K BHS'T. GQX YGQZDJ K YTHNT KT?  'LQZ DKUF VHRR?' SQ, TGHT'Y SQ WQQJ. GFNF YGF BQCFY! YIFHU, LQZ AQQD! K'C YQNNL. LQZ'NF THDUKSW. LFY, K USQX. LQZ'NF THDUKSW! K'C YQ YQNNL. SQ, KT'Y QU. KT'Y AKSF. K USQX K'C JNFHCKSW MZT K JQS'T NFBHDD WQKSW TQ MFJ.";
    const letters = ref(
        {
            'A': { 'display': 'A', 'isGuessed': false }, 'B': { 'display': 'B', 'isGuessed': false }, 'C': { 'display': 'C', 'isGuessed': false }, 'D': { 'display': 'D', 'isGuessed': false }, 'E': { 'display': 'E', 'isGuessed': false }, 'F': { 'display': 'F', 'isGuessed': false }, 'G': { 'display': 'G', 'isGuessed': false }, 'H': { 'display': 'H', 'isGuessed': false }, 'I': { 'display': 'I', 'isGuessed': false }, 'J': { 'display': 'J', 'isGuessed': false }, 'K': { 'display': 'K', 'isGuessed': false }, 'L': { 'display': 'L', 'isGuessed': false }, 'M': { 'display': 'M', 'isGuessed': false }, 'N': { 'display': 'N', 'isGuessed': false }, 'O': { 'display': 'O', 'isGuessed': false }, 'P': { 'display': 'P', 'isGuessed': false }, 'Q': { 'display': 'Q', 'isGuessed': false }, 'R': { 'display': 'R', 'isGuessed': false }, 'S': { 'display': 'S', 'isGuessed': false }, 'T': { 'display': 'T', 'isGuessed': false }, 'U': { 'display': 'U', 'isGuessed': false }, 'V': { 'display': 'V', 'isGuessed': false }, 'W': { 'display': 'W', 'isGuessed': false }, 'X': { 'display': 'X', 'isGuessed': false }, 'Y': { 'display': 'Y', 'isGuessed': false }, 'Z': { 'display': 'Z', 'isGuessed': false }, 
        }
    );
    var selectedLetter = ref('');
    var isHidden = ref(false);

    document.addEventListener('keyup', keypress);

    function isLetter(letter) {
        return /^[A-Z]$/.test(letter);
    }

    function keypress(event) {
        if (!selectedLetter.value)
            return;
        const letter = event.key.toUpperCase();
        if (isLetter(letter)) {
            var letterObject = letters.value[selectedLetter.value];
            letterObject.display = letter;
            letterObject.isGuessed = true;
        }
        else if (letter == 'BACKSPACE') {
            var letterObject = letters.value[selectedLetter.value]
            letterObject.display = selectedLetter.value;
            letterObject.isGuessed = false;
        }
        else if (letter == 'ESCAPE')
            selectedLetter.value = '';
    }


</script>

<style scoped>

</style>

<style>
    .guessed {
        @apply text-green-500 font-semibold;
    }

    .selected {
        @apply bg-pink-500 text-primary-color rounded-sm font-normal;
    }

</style>