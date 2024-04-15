<template>
    <SignUp v-if="isSigningUp" @leave="isSigningUp = false"/>
    <div class="w-screen h-14 bg-primary-color flex">
        <PinkButton draggable="false" @click="isSigningUp = true">Login</PinkButton>
        <PinkButton>{{ username }}</PinkButton>
    </div>
</template>

<script setup>
import PinkButton from '../components/pinkButton.vue'
import SignUp from '../views/SignUpView.vue'
import clientUser from '../tools/User'
import { username } from '../tools/User'
import { isSigningUp } from '../tools/PageUtils'


clientUser.updateFromCookie();
</script>