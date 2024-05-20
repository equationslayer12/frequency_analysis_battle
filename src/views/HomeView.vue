<template>
  <!-- <div id="top" @mousemove="setTopSpotlightPosition" class="relative bg-primary-color h-96 w-full flex flex-col justify-center items-center overflow-hidden rounded-b-full shadow-lg shadow-black border-solid">
    <h1 id="title" class="text-white text-8xl">SPAN RACER</h1>
  </div> -->
  <h1 class="mb-5">SPAN RACER</h1>
  <div class="mb-xl max-w-2xl bg-primary-color p-lg text-xl flex justify-between rounded-md shadow-md shadow-accent-color">
    <span class="flex flex-col">
      <span class="text-text-color text-2xl font-bold">MULTIPLAYER</span>
      <span class="text-text-color">Race against others to see who can decipher faster!</span>
    </span>
    <PinkButton draggable="false" href="/race" class="ml-xl">Race</PinkButton>
  </div>
  <div class="mb-xl max-w-2xl bg-primary-color p-lg text-xl flex justify-between rounded-md shadow-md shadow-accent-color">
    <span class="flex flex-col">
      <span class="text-text-color text-2xl font-bold">PRACTICE MODE</span>
      <span class="text-text-color">Practice deciphering to become faster!</span>
    </span>
    <PinkButton draggable="false" href="/practice">Practice</PinkButton>
  </div>
  <button @click="test" class="bg-cyan-500 font-bold text-3xl rounded-md p-10">TEST: {{ counter }}</button>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import PinkButton from '../components/pinkButton.vue'
import clientUser from '../user/ClientUser'

let isHovered = ref(false);
let counter = ref('Loading..');
let username = ref('Guest');

setupCounter();
setupUsername();

async function setupCounter() {
  const count = await getCount();
  counter.value = count;
}
function setupUsername() {
  clientUser.updateFromSession();
}

function test() {
  try {
    counter.value += 1;
  } catch(error) {
    console.log(error);
  }
  console.log("Sending request..")
  axios.post('/api/test')
  .then(response => {
    console.log('Response: ', response.data);
    // counter.value = response.data;
  });
}

async function getCount() {
  try {
    const response = await axios.get('/api/test');
    return response.data;
  } catch (error) {
    console.error(`Error: ${error}`)
    return null
  }
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
      /* @apply flex justify-center items-center bg-background-color; */
    /* } */


</style>
