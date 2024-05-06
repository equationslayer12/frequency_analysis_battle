<template>
    <div id="analysis-tools" class="bg-background-color w-full border-primary-color flex flex-col border-solid border-4 rounded-md">
        <nav class="mb-md flex justify-around content-stretch border-b-4 border-primary-color cursor-pointer">
            <div v-for="toolName in toolNames" @click="selectedTool = toolName" class="bg-primary-color text-text-color flex-grow hover:bg-text-color hover:text-background-color duration-300"
            :class="{'selected': toolName == selectedTool}"
            :title="toolDescriptions[toolName]"
            >{{ toolName }}</div>
        </nav>
        
        <!-- Letters utility -->
        <section v-if="selectedTool == toolNames[LETTERS_TOOL]">
            <div id="table" class="text-secondary-color mx-md mb-lg flex justify-between items-end">
                <span v-for="[letter, count] in Object.entries(lettersCount)">
                    <p>{{ count }}</p>
                    <div class="bg-text-color w-4 border-solid border-primary-color border-1" :style="{'height': `${Math.max(0.1, count / maxLetterCount * 6)}em`}"></div>
                    <p>{{ letter }}</p>
                    <LetterComponent class="border-b-2 border-primary-color" :letter="letter"/>
                </span>
            </div>
        </section>

        <!-- Words utility -->
        <section v-if="selectedTool == toolNames[WORDS_TOOL]">
            <nav class="mb-sm flex justify-center items-center space-x-sm">
                <button title="Go back" class="p-2 bg-primary-color text-text-color hover:bg-text-color hover:text-background-color duration-300 rounded-md" @click="updateWordsPage(-1)">&#60;</button>
                <span class="text-text-color">{{ currentWordPage + 1 }} / {{ maxWordPage }}</span>
                <button title="Go forward" class="p-2 bg-primary-color text-text-color hover:bg-text-color hover:text-background-color duration-300 rounded-md" @click="updateWordsPage(1)">&#62;</button>
            </nav>
            <div id="table" class="text-secondary-color mx-md mb-lg flex justify-between items-end">
                <span v-for="word in mostFrequentWords.slice(currentWordPage * wordsPerPage, currentWordPage * wordsPerPage + wordsPerPage)"
                    class="flex flex-col justify-center items-center"
                >
                    {{ wordsCount[word] }}
                    <div class="bg-text-color w-14 rounded-sm border-solid border-primary-color border-1" :style="{'height': `${wordsCount[word] / maxWordCountForPage * 6}em`}"></div>
                    <span>
                        <span v-for="letter in word">
                            <LetterComponent :letter="letter"/>
                        </span>
                    </span>
                </span>
            </div>
        </section>

        <!-- Ngrams utility -->
        <section v-if="selectedTool == toolNames[NGRAMS_TOOL]">
            <nav class="mb-sm flex justify-center items-center space-x-sm">
                <button title="Decrease N size" class="p-2 bg-primary-color text-text-color hover:bg-text-color hover:text-background-color duration-300 rounded-md" @click="ngramAnalysis.changeNSize(-1)">&#60;</button>
                <div class="inline-flex flex-col">
                    <span class="text-text-color font-bold">{{ ngramAnalysis.Nsize }}</span>
                    <p class="text-text-color">N Size</p>
                </div>
                <button title="Increase N Size" class="p-2 bg-primary-color text-text-color hover:bg-text-color hover:text-background-color duration-300 rounded-md" @click="ngramAnalysis.changeNSize(1)">&#62;</button>
            </nav>
            
            
            <div id="table" class="mx-md mb-lg text-secondary-color flex justify-between items-end">
                <span v-for="nGram in ngramAnalysis.mostFrequentNgrams.value.slice(ngramAnalysis.currentPage.value * ngramAnalysis.nGramsPerPage.value, ngramAnalysis.currentPage.value * ngramAnalysis.nGramsPerPage.value + ngramAnalysis.nGramsPerPage.value)"
                    class="flex flex-col justify-center items-center"
                >
                    {{ ngramAnalysis.NgramsCount.value[nGram] }}
                    <div class="bg-text-color w-8 border-solid border-primary-color border-1" :style="{'height': `${ngramAnalysis.NgramsCount.value[nGram] / ngramAnalysis.maxNgramPerCurrentPage.value * 6}em`}"></div>
                    <span>
                        <span v-for="letter in nGram">
                            <LetterComponent :letter="letter"/>
                        </span>
                    </span>
                </span>
            </div>
        </section>
    </div>
    stiol hello
</template>

<script setup>
import { alphabet } from '@/Constants';
import LetterComponent from '../components/LetterComponent.vue'
import nGramAnalysis from '../tools/nGramAnalysis'
import { game } from '@/game/Game'
import { ref } from 'vue'

const LETTERS_TOOL = 0;
const WORDS_TOOL = 1;
const NGRAMS_TOOL = 2;

const toolDescriptions = {
    "Letters": "Letter frequency",
    "Words": "Word frequency",    
    "N-Grams": "A sequence of n adjacent symbols"
};
const toolNames = ref(Object.keys(toolDescriptions));
var selectedTool = ref(toolNames.value[LETTERS_TOOL]);

// Letters utility
var lettersCount = ref({})
for (let i = 0; i < alphabet.length; i++) {
    const letter = alphabet[i];
    lettersCount.value[letter] = 0;
}
countLetters(game.cleanText);

// Words utility
let currentWordPage = ref(0);
const wordsPerPage = 6;

let wordsCount = ref({})

for (let i = 0; i < game.wordsArray.length; i++) {
    const word = game.wordsArray[i];
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

// Ngrams utility
const ngramAnalysis = new nGramAnalysis(3);

function countLetters(text) {
    for (let i = 0; i < text.length; i++) {
        const letter = text[i];
        if (game.textState.isLetter(letter))
            lettersCount.value[letter]++;
    }
}

function isLetter(letter) {
    return /^[A-Z]$/.test(letter);
}


var maxLetterCount = 0;

for (let i = 0; i < game.cleanText.length; i++) {
    const letter = game.cleanText[i];
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

</script>

<style scoped>
.selected {
    @apply font-bold bg-secondary-color
}
</style> 