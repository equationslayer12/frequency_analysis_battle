<template>
    <div @mouseover="isHovering=true" @mouseleave="isHovering=false" class="bg-primary-color p-xl text-xl flex justify-between rounded-md shadow-md transition-shadow" :class="{'shadow-accent-color': isHovering}">
      <slot />
    </div>
</template>
  
<script setup>
  import { ref } from 'vue';
  
  let isHovering = ref(false);
</script>