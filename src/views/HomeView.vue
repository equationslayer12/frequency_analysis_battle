<template>
    <a draggable="false" href="/race">
    <button class="uppercase  px-4 h-16 text-3xl bg-pink-500 text-white font-semibold content-center rounded-xl border-4 border-pink-600 shadow-lg shadow-pink-400 active:shaow-pink-50 hover:border-pink-400 active:bg-pink-300 duration-100 active:text-4xl">race</button>
  </a>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js + TypeScript App"/>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import HelloWorld from '@/components/HelloWorld.vue'; // @ is an alias to /src

export default defineComponent({
  name: 'HomeView',
  components: {
    HelloWorld,
  },
});
</script>
