<template>
    <div class="w-full rounded-lg border-solid border-text-color border-2 border-opacity-20 flex content-start overflow-hidden">
        <!-- <div class="h-full" :style="{width: `${current / end * 100}%`}"> -->
        <span class="ml-md">{{ username }} {{ current }} / {{ end }}</span>
        <!-- </div> -->
    </div>
</template>

<script setup>
const props = defineProps({
    username: String,
    current: Number,
    end: Number
});

</script>