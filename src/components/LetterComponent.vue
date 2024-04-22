<template>

<span v-if="letter !== ' '" @mouseover="selectLetter()" @mouseleave="unselectLetter()">
    <!-- letter isn't in alphabet -->
    <span v-if="!isAlphabet">{{ letter }} </span>  
    
    <!-- hidden mode is activated, display a * -->
    <span v-else-if="(!letterState.isGuessed) && hiddenModeActive" class="duration-300" :class="{'guessed': letterState.isGuessed, 'selected': letter == selectedLetter}">*</span>
    <!--  -->
    <span v-else class="duration-300" :class="{
        'guessed': letterState.isGuessed,
        'selected': letter == selectedLetter,
        'duplicate': isDuplicate(letter) && letterState.isGuessed
    }">{{ letterState.displayLetter }}</span>
</span>

</template>

<script setup>
import { LetterState } from '@/game/LetterState';
import { game, lettersState, selectedLetter, hiddenModeActive } from '@/game/Game';

const props = defineProps(['letter'])
const letter = props.letter;

let isAlphabet = true;
const letterState = lettersState[letter];
if (letterState == undefined)
    isAlphabet = false;

function isDuplicate() {
    const guessedLetter = letterState.value.displayLetter;
    const guessedLetterState = lettersState[guessedLetter];
    return guessedLetterState.value.otherLettersGuessedCount > 1;
}

function selectLetter() {
    game.textState.selectLetter(letter, isAlphabet);
}

function unselectLetter() {
    game.textState.unselectLetter();
}
</script>