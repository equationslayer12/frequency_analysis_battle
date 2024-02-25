<template>
    <div id="analysis-tools" class="bg-primary-color min-h-56 w-full border-secondary-color flex flex-col justify-between border-solid border-4 rounded-md mt-3">
        <nav class="flex justify-around content-stretch border-b-4 border-secondary-color cursor-pointer">
            <div v-for="toolName in tools" @click="selectedTool = toolName" class="bg-secondary-color text-accent-color flex-grow hover:bg-accent-color hover:text-primary-color duration-300"
            :class="{'selected': toolName == selectedTool}"
            :title="toolDescription[toolName]"
            >{{ toolName }}</div>
        </nav>

        <!-- Letters utility -->
        <section v-if="selectedTool == tools[0]">
            <div id="table" class="text-third-color p-2 flex justify-between items-end">
                <span v-for="[letter, count] in Object.entries(lettersCount)">
                    <p>{{ count }}</p>
                    <div class="bg-accent-color w-4 border-solid border-secondary-color border-1" :style="{'height': `${count / maxLetterCount * 6}em`}"></div>
                    <p>{{ letter }}</p>
                    <LetterComponent class="border-b-2 border-secondary-color" @changeSelectedLetter="forwardChangeSelectedLetter" :letter="letter" :selectedLetter="selectedLetter" :letters="letters" :isHidden="isHidden"/>
                </span>
            </div>
        </section>

        <!-- Words utility -->
        <section v-if="selectedTool == tools[1]">
            <nav class="flex justify-center items-center m-1 mb-0 space-x-1">
                <button title="Go back" class="p-2 bg-secondary-color text-accent-color hover:bg-accent-color hover:text-primary-color duration-300 rounded-md" @click="updateWordsPage(-1)">&#60;</button>
                <span class="text-accent-color">{{ currentWordPage + 1 }} / {{ maxWordPage }}</span>
                <button title="Go forward" class="p-2 bg-secondary-color text-accent-color hover:bg-accent-color hover:text-primary-color duration-300 rounded-md" @click="updateWordsPage(1)">&#62;</button>
            </nav>
            <div id="table" class="text-third-color p-2 pt-0 flex justify-between items-end">
                <span v-for="word in mostFrequentWords.slice(currentWordPage * wordsPerPage, currentWordPage * wordsPerPage + wordsPerPage)"
                    class="flex flex-col justify-center items-center"
                >
                    {{ wordsCount[word] }}
                    <div class="bg-accent-color w-8 border-solid border-secondary-color border-1" :style="{'height': `${wordsCount[word] / maxWordCountForPage * 6}em`}"></div>
                    <span>
                        <span v-for="letter in word">
                            <LetterComponent class="" @changeSelectedLetter="forwardChangeSelectedLetter" :letter="letter" :selectedLetter="selectedLetter" :letters="letters" :isHidden="isHidden"/>
                        </span>
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

const tools = ref(["Letters", "Words", "N-Grams"]);
var selectedTool = ref(tools.value[1]);

const toolDescription = ref({
    "N-Grams": "A sequence of n adjacent symbols"
});

const abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

// Letters utility
var lettersCount = ref({})
for (let i = 0; i < abc.length; i++) {
    const letter = abc[i];
    lettersCount.value[letter] = 0;
}
countLetters(text);

// Words utility
var currentWordPage = ref(0);
const wordsPerPage = 6;

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

const maxWordPage = Math.ceil(mostFrequentWords.length / wordsPerPage);

function updateWordsPage(count) {
    currentWordPage.value += count;
    if (currentWordPage.value < 0) {
        currentWordPage.value = maxWordPage - 1;
    }
    else if (maxWordPage <= currentWordPage.value) {
        currentWordPage.value %= maxWordPage;
    }
    maxWordCountForPage = findMaxWordCountForPage();
}


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

var maxLetterCount = 0;

for (let i = 0; i < text.length; i++) {
    const letter = text[i];
    if(isLetter(letter)) {
        maxLetterCount = Math.max(lettersCount.value[letter], maxLetterCount);
    }
}

var maxWordCountForPage = findMaxWordCountForPage();
function findMaxWordCountForPage() {
    
    var maxWordCount = 0;
    for (let i = currentWordPage.value*wordsPerPage; i < currentWordPage.value*wordsPerPage + wordsPerPage; i++) {
        const word = mostFrequentWords[i];
        maxWordCount = Math.max(wordsCount.value[word], maxWordCount);
    }
    return maxWordCount;
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