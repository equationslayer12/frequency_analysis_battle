<template>
  <NavBar></NavBar>
  <router-view/>
</template>

<style>
body {
  @apply bg-gradient-to-b h-screen;
  background: 
              /* radial-gradient(50vh circle at 50% 0px, rgb(0, 72, 83), transparent), */
              linear-gradient(to bottom, theme('colors.background-color') 30%, black)
  ;
}
</style>

<script setup>
  import NavBar from './components/NavBar.vue';
  const a = "hello";
</script>
