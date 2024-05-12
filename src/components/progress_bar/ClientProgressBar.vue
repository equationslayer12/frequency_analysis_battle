<!-- 
    A client-specific progress bar.
    display with accent color, and display with client-specific values.
 -->
<template>
    <div>
        <ProgressBar class="bg-guessed-color" :username="username" :current="totalLettersGuessed" :end="cipheredLettersCount"/>
    </div>
</template>

<script setup>
import { totalLettersGuessed, cipheredLettersCount } from '@/game/Game';
import client from "@/user/ClientUser"
import ProgressBar from './ProgressBar.vue';

const username = client.username;
</script>
