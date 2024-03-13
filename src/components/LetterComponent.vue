<template>
<span v-if="letter !== ' '" :original-letter="letter" @mouseover="hoverLetter" @mouseleave="textUtil.changeSelectedLetter('')">
    <!-- {{ console.log((!textUtil.lettersState.value[letter].isGuessed) && textUtil.hiddenModeActive) }} -->
    <span v-if="!textUtil.isLetter(letter)">{{ letter }}</span>
    <span v-else-if="(!textUtil.lettersState.value[letter].isGuessed) && textUtil.hiddenModeActive.value" class="duration-300" :class="{'guessed': textUtil.lettersState.value[letter].isGuessed, 'selected': letter == textUtil.selectedLetter.value}">*</span>
    <span v-else-if="letter in textUtil.lettersState.value" class="duration-300" :class="{'guessed': textUtil.lettersState.value[letter].isGuessed, 'selected': letter == textUtil.selectedLetter.value}">{{ textUtil.lettersState.value[letter].display }}</span>
    <span v-else class="duration-300">{{ letter }}</span>
</span>

</template>

<script setup>
import textUtil from '../tools/TextUtil'

// const props = defineProps(['letter', 'selectedLetter', 'letters', 'isHidden'])
const props = defineProps(['letter'])
// const emit = defineEmits(['changeSelectedLetter'])

function hoverLetter(event) {
    let letterElement = event.target.parentElement;
    textUtil.changeSelectedLetter(
        letterElement.getAttribute('original-letter')
    );
}
</script>