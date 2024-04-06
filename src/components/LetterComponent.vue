<template>
<span v-if="letter !== ' '" :original-letter="letter" @mouseover="hoverLetter" @mouseleave="textUtil.changeSelectedLetter('')">
    <!-- letter isn't in alphabet -->
    <span v-if="!textUtil.isLetter(letter)">{{ letter }} </span>  
    
    <!-- hidden mode is activated, display a * -->
    <span v-else-if="(!lettersState[letter].isGuessed) && hiddenModeActive" class="duration-300" :class="{'guessed': lettersState[letter].isGuessed, 'selected': letter == textUtil.selectedLetter.value}">*</span>
    <!--  -->
    <span v-else-if="letter in lettersState" class="duration-300" :class="{
        'guessed': lettersState[letter].isGuessed,
        'selected': letter == selectedLetter,
        'duplicate': isDuplicate(letter)
    }">{{ lettersState[letter].display }}</span>
    <span v-else class="duration-300">{{ letter }}</span>
</span>

</template>

<script setup>
import textUtil from '../tools/TextUtil'
import { letterBank, lettersState, selectedLetter, hiddenModeActive } from '../tools/TextUtil';

const props = defineProps(['letter'])

function hoverLetter(event) {
    let letterElement = event.target.parentElement;
    textUtil.changeSelectedLetter(
        letterElement.getAttribute('original-letter')
    );
}
function isDuplicate(originalLetter) {
    let displayLetter = lettersState.value[originalLetter].display
    return letterBank.value[displayLetter].count > 1;
}
</script>