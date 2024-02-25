<template>
  <div id="top" @mousemove="setTopSpotlightPosition" class="relative bg-secondary-color h-96 w-full flex flex-col justify-center items-center overflow-hidden rounded-b-full shadow-lg shadow-black border-solid">
    <h1 id="title" class="text-white text-8xl">SPAN RACER</h1>
  </div>
  <PinkButton draggable="false" href="/race">Race</PinkButton>
</template>

<script setup lang="ts">
import {ref} from 'vue';
import PinkButton from '../components/pinkButton.vue'

var isHovered = ref(false);

function test() {
  console.log("test");
}

function setTopSpotlightPosition(event: any) {
  const top = document.getElementById("top");
  if (top) {
    const rect = top.getBoundingClientRect(),
          x = event.x - rect.x,
          y = event.y - rect.y;
    top.style.setProperty("--mouse-x", `${x}px`);
    top.style.setProperty("--mouse-y", `${y}px`);
  }

}
</script>

<script lang="ts">
</script>

<style scoped>
#top-container {
  height: 150%;
  width: 100vw;
  display: flex;
  justify-content: center;
}

#top {
  width: 80vw;
}
#top::before {  /* spotlight */
  content: "";
  width: 100%;
  height: 100%;
  background: radial-gradient(1000px circle at var(--mouse-x) var(--mouse-y), rgba(255, 255, 255, 0.2), transparent 50%);
  opacity: 0;
  transition: opacity 500ms;
  position: absolute;
  top: 0;
  left: 0;
}
#top:hover::before {
  opacity: 1;
}

#title {
  font-family: 'JetBrains Mono', monospace;
}
    /* #app {
      @apply w-screen h-screen;
      /* @apply flex justify-center items-center bg-primary-color; */
    /* } */


</style>
