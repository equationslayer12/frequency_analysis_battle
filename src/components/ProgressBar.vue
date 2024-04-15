<template>
    <div class="bg-background-color w-full rounded-lg border-solid border-text-color border-2 border-opacity-20 m-2 flex content-start overflow-hidden">
        <!-- <div class="bg-accent-color h-full" :style="{width: `${current / end * 100}%`}"> -->
            <span class="text-text-color">{{ current }} / {{ end }}</span>

        <!-- </div> -->
    </div>
</template>

<script setup>
import { ref } from 'vue';
const props = defineProps({
    current: Number,
    end: Number
});

</script>