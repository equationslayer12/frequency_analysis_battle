<template>
  <router-view/>
</template>

<style>
#app {
  /* font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center; */
  /* color: #2c3e50; */
  /* @apply w-screen; */
}

body {
  @apply bg-gradient-to-b text-center flex justify-center h-screen;
  background: 
              /* radial-gradient(50vh circle at 50% 0px, rgb(0, 72, 83), transparent), */
              linear-gradient(to bottom, theme('colors.background-color') 30%, black)
  ;
}
</style>

<script>
  const a = "hello";
</script>
