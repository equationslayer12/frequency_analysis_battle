<template>
    <div id="analysis-tools" class="border-secondary-color flex flex-col justify-center h-fit w-full border-solid border-4 rounded-md mt-3">
        <nav class="flex justify-around content-stretch border-b-4 border-secondary-color cursor-pointer">
            <div v-for="toolName in tools" @click="selectedTool = toolName" class="bg-secondary-color text-accent-color flex-grow hover:bg-accent-color hover:text-primary-color"
            :class="{'selected': toolName == selectedTool}"
            >{{ toolName }}</div>
        </nav>

        <!-- Letters utility -->
        <section v-if="selectedTool == tools[0]">
            <div id="table" class="text-third-color p-2 flex justify-between items-end">
                <span v-for="[letter, count] in Object.entries(lettersCount)">
                    <p>{{ count }}</p>
                    <div class="bg-accent-color w-4 border-solid border-secondary-color border-1" :style="{'height': `${count / maxCount * 6}em`}"></div>
                    <p>{{ letter }}</p>
                    <LetterComponent class="" @changeSelectedLetter="forwardChangeSelectedLetter" :letter="letter" :selectedLetter="selectedLetter" :letters="letters" :isHidden="isHidden"/>
                </span>
            </div>
        </section>

        <!-- Words utility -->
        <section v-if="selectedTool == tools[1]">
            <div id="table" class="text-third-color p-2 flex justify-between items-end">
                <span v-for="word in mostFrequentWords">
                    <span v-for="letter in word">
                        <div class="bg-accent-color w-4 border-solid border-secondary-color border-1" :style="{'height': `${count / maxCount * 6}em`}"></div>
                        <p>{{ letter }}</p>
                        <LetterComponent class="" @changeSelectedLetter="forwardChangeSelectedLetter" :letter="letter" :selectedLetter="selectedLetter" :letters="letters" :isHidden="isHidden"/>
                    </span>
                </span>
            </div>
        </section>
    </div>
    stiol hello
</template>

<script setup>
import LetterComponent from '../components/LetterComponent.vue'
import { ref } from 'vue'

const props = defineProps(['text', 'letters', 'isHidden', 'selectedLetter'])
const emit = defineEmits(['changeSelectedLetter'])
const text = removePunc(props.text);

const tools = ref(["Letters", "Words", "Graphs"]);
var selectedTool = ref(tools.value[1])

const abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

// Letters utility
var lettersCount = ref({})
for (let i = 0; i < abc.length; i++) {
    const letter = abc[i];
    lettersCount.value[letter] = 0;
}
countLetters(text);

// Words utility
var wordsCount = ref({})
const wordsArray = text.split(" ");

for (let i = 0; i < wordsArray.length; i++) {
    const word = wordsArray[i];
    if (wordsCount.value[word])
        wordsCount.value[word] ++;
    else
        wordsCount.value[word] = 1;
}

const mostFrequentWords = Object.keys(wordsCount.value);
mostFrequentWords.sort((a, b) => wordsCount.value[b] - wordsCount.value[a]);




function countLetters(text) {
    for (let i = 0; i < text.length; i++) {
        const letter = text[i];
        if (isLetter(letter)) {
            lettersCount.value[letter]++;
        }
        
    }
}

function isLetter(letter) {
    return /^[A-Z]$/.test(letter);
}

function removePunc(str) {
    return str.replace(/[^\w\s\']|_/g, "")
              .replace(/\s+/g, " ")
}

var maxCount = 0;

for (let i = 0; i < text.length; i++) {
    const letter = text[i];
    if(isLetter(letter)) {
        maxCount = Math.max(lettersCount.value[letter], maxCount);
    }
}

function forwardChangeSelectedLetter(newLetter) {
    emit('changeSelectedLetter', newLetter);
}
</script>

<style scoped>
.selected {
    @apply font-bold bg-third-color
}
</style>