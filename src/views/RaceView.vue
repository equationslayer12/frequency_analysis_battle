<template>
    <h1 class="text-4xl font-semibold my-14 hover:scale-125 duration-150 text-accent-color">FREQUENCY ANALYSIS BATTLE</h1>
    <div id="textbox" class="flex-wrap bg-secondary-color text-ignore-color flex justify-between gap-x-2 text-xl font-mono h-96 aspect-video p-8 rounded-xl shadow-lg shadow-slate-900 py-0">
        <div class="w-full flex justify-center items-center text-xs underline">
            <p>SHOW</p>
            <label class="switch scale-75" id="hiddenSwitch">
                <input type="checkbox">
                <span class="slider round">

                </span>
            </label>
            <p>HIDE</p>
        </div>
        <!-- <span v-for="word in text.split(' ')">
            <span v-for="letter in word" v-if="letter !== ' '" :original-letter="letter" @mouseover="hoverLetter" @mouseleave="selectedLetter = ''" class="duration-300" :class="{'guessed': letters[letter].isGuessed, 'selected': letter == selectedLetter}">
                <span v-if="letter == letters[letter].display && isHidden">*</span>
                <span v-else-if="letter in letters">{{ letters[letter].display }}</span>
                <span v-else>{{ letter }}</span>
            </span>
        </span> -->
        <span v-for="word in text.split(' ')">
            <span v-for="letter in word" v-if="letter !== ' '" :original-letter="letter" @mouseover="hoverLetter" @mouseleave="selectedLetter = ''" class="duration-300">
                <span v-if="!isLetter(letter)">{{ letter }}</span>
                <span v-else-if="(!letters[letter].isGuessed) && isHidden" :class="{'guessed': letters[letter].isGuessed, 'selected': letter == selectedLetter}">*</span>
                <span v-else-if="letter in letters" :class="{'guessed': letters[letter].isGuessed, 'selected': letter == selectedLetter}">{{ letters[letter].display }}</span>
                <span v-else>{{ letter }}</span>
            </span>

        </span>
            <!-- <span v-for="letter in word" v-if="letter !== ' '" :original-letter="letter" @mouseover="hoverLetter" @mouseleave="selectedLetter = ''" class="duration-300" :class="{'guessed': letters[letter].isGuessed, 'selected': letter == selectedLetter}">
                <span v-if="letter == letters[letter].display && isHidden">*</span>
                <span v-else-if="letter in letters">{{ letters[letter].display }}</span>
                <span v-else>{{ letter }}</span>
            </span> -->

        <!-- onmouseover="selected" onmouseleave="endHoverLetter" -->
    </div>
</template>

<script setup>
    import {ref, reactive} from 'vue'
    var letter = '';
    const text = "DJ DK C QLXDWI WF SDGDU PCX. XLRLU KQCSLKBDQK, KJXDHDET FXWZ C BDIILE RCKL, BCGL PWE JBLDX FDXKJ GDSJWXO CTCDEKJ JBL LGDU TCUCSJDS LZQDXL. IYXDET JBL RCJJUL, XLRLU KQDLK ZCECTLI JW KJLCU KLSXLJ QUCEK JW JBL LZQDXL’K YUJDZCJL PLCQWE, JBL ILCJB KJCX, CE CXZWXLI KQCSL KJCJDWE PDJB LEWYTB QWPLX JW ILKJXWO CE LEJDXL QUCELJ. QYXKYLI RO JBL LZQDXL’K KDEDKJLX CTLEJK, QXDESLKK ULDC XCSLK BWZL CRWCXI BLX KJCXKBDQ, SYKJWIDCE WF JBL KJWULE QUCEK JBCJ SCE KCGL BLX QLWQUL CEI XLKJWXL FXLLIWZ JW JBL TCUCVO…";
    const letters = ref(
        {
            'A': { 'display': 'A', 'isGuessed': false }, 'B': { 'display': 'B', 'isGuessed': false }, 'C': { 'display': 'C', 'isGuessed': false }, 'D': { 'display': 'D', 'isGuessed': false }, 'E': { 'display': 'E', 'isGuessed': false }, 'F': { 'display': 'F', 'isGuessed': false }, 'G': { 'display': 'G', 'isGuessed': false }, 'H': { 'display': 'H', 'isGuessed': false }, 'I': { 'display': 'I', 'isGuessed': false }, 'J': { 'display': 'J', 'isGuessed': false }, 'K': { 'display': 'K', 'isGuessed': false }, 'L': { 'display': 'L', 'isGuessed': false }, 'M': { 'display': 'M', 'isGuessed': false }, 'N': { 'display': 'N', 'isGuessed': false }, 'O': { 'display': 'O', 'isGuessed': false }, 'P': { 'display': 'P', 'isGuessed': false }, 'Q': { 'display': 'Q', 'isGuessed': false }, 'R': { 'display': 'R', 'isGuessed': false }, 'S': { 'display': 'S', 'isGuessed': false }, 'T': { 'display': 'T', 'isGuessed': false }, 'U': { 'display': 'U', 'isGuessed': false }, 'V': { 'display': 'V', 'isGuessed': false }, 'W': { 'display': 'W', 'isGuessed': false }, 'X': { 'display': 'X', 'isGuessed': false }, 'Y': { 'display': 'Y', 'isGuessed': false }, 'Z': { 'display': 'Z', 'isGuessed': false }, 
        }
    );
    var selectedLetter = ref('');
    var isHidden = true;

    document.addEventListener('keyup', keypress);

    function isLetter(letter) {
        return /^[A-Z]$/.test(letter);
    }

    function hoverLetter(event) {
        let letterElement = event.target.parentElement;
        console.log(letterElement);
        selectedLetter.value = letterElement.getAttribute('original-letter');
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

<style>
    body {
        @apply flex justify-center items-center bg-primary-color;
    }

    .guessed {
        @apply text-green-500 font-semibold;
    }

    .selected {
        @apply bg-pink-500 text-primary-color rounded-sm font-normal;
    }

</style>