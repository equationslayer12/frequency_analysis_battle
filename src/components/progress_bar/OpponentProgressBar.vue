<!-- 
    A regular progress bar, but with Evil color.
    takes in the current value (Number), and the end goal value (Number).
    current / end
 -->
<template>
    <div>
        <ProgressBar class="bg-evil-color" :current="current" :end="end"/>
    </div>
</template>

<script setup>
import ProgressBar from './ProgressBar.vue';

const props = defineProps({
    current: Number,
    end: Number
});

</script>
