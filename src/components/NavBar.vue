<template>
    <SignUp v-if="isSigningUp" @leave="isSigningUp = false"/>
    <div class="w-screen h-14 bg-primary-color flex">
        <PinkButton draggable="false" @click="isSigningUp = true">Login</PinkButton>
        <PinkButton>{{ clientUser.username.value }}</PinkButton>
    </div>
</template>

<script setup>
import PinkButton from '@/components/pinkButton.vue'
import SignUp from '@/components/SignUpComponent.vue'
import clientUser from '@/user/ClientUser'
import { isSigningUp } from '@/tools/PageUtils'


clientUser.updateFromSession();
</script>