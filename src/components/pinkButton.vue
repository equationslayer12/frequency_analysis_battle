<template>
    <a :href="href" :draggable="draggable" :onclick="onclick">
        <button class="uppercase  px-4 h-16 text-3xl bg-pink-500 text-white font-semibold content-center rounded-xl border-4 border-pink-600 shadow-lg shadow-pink-400 active:shaow-pink-50 hover:border-pink-400 active:bg-pink-300 duration-100 active:text-4xl">
            <slot />
        </button>
    </a>
</template>

<script setup>
    defineProps(
        [
            'draggable',
            'href',
            'onclick'
        ]
    )
</script>