<template>
<span v-if="letter !== ' '" :original-letter="letter" @mouseover="hoverLetter" @mouseleave="changeSelectedLetter('')">
    <span v-if="!isLetter(letter)">{{ letter }}</span>
    <span v-else-if="(!letters[letter].isGuessed) && isHidden" class="duration-300" :class="{'guessed': letters[letter].isGuessed, 'selected': letter == selectedLetter}">*</span>
    <span v-else-if="letter in letters" class="duration-300" :class="{'guessed': letters[letter].isGuessed, 'selected': letter == selectedLetter}">{{ letters[letter].display }}</span>
    <span v-else class="duration-300">{{ letter }}</span>
</span>

</template>

<script setup>
const props = defineProps(['letter', 'selectedLetter', 'letters', 'isHidden'])
const emit = defineEmits(['changeSelectedLetter'])
function isLetter(letter) {
    return /^[A-Z]$/.test(letter);
}

function hoverLetter(event) {
    let letterElement = event.target.parentElement;
    changeSelectedLetter(
        letterElement.getAttribute('original-letter')
    );
}

function changeSelectedLetter(newLetter) {
    if (isLetter(newLetter) || newLetter == '')
        emit("changeSelectedLetter", newLetter);
}
</script>