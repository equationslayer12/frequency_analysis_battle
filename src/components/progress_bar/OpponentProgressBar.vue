<!-- 
    A regular progress bar, but with Evil color.
    takes in the opponent player
 -->
<template>
    <div>
        <ProgressBar class="bg-evil-color" :username="opponent?.username" :current="opponent?.progress?.current" :end="opponent?.progress?.end"/>
    </div>
</template>

<script setup>
import { Player } from '@/user/OpponentPlayer';
import ProgressBar from './ProgressBar.vue';

const props = defineProps({
    opponent: Player
});

</script>
