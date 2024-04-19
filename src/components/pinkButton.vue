<template>
    <a :href="href" :draggable="draggable" :onclick="handleClick">
        <button class="uppercase  px-4 h-16 text-3xl bg-pink-500 text-white font-semibold content-center rounded-xl border-4 border-pink-600 shadow-lg shadow-pink-400 active:shaow-pink-50 hover:border-pink-400 active:bg-pink-300 duration-100 active:text-4xl">
            <slot />
        </button>
    </a>
</template>

<script setup>
    const props = defineProps(
        {
            'draggable': String,
            'href': String,
            'onclick': {type: Function}
        }
    )
    function handleClick(event) {
        playSound();
        if (props.onclick != undefined) {
            props.onclick(event);
        };
    }
    function playSound() {
        new Audio("/api/pop.mp3").play();
    }
</script>