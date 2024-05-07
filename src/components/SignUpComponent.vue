<template>
    <div :id="backgroundId" @click="leave" class="bg-black bg-opacity-70 transition-opacity absolute z-10 h-full w-full top-0 left-0 flex justify-center items-center">
        <div class="bg-primary-color bg-gradient-to-r from-primary-color to-background-color h-5/6 aspect-[7/10] rounded-xl opacity-100 p-5 transition-opacity">
            <span v-if="!isSigningIn" id="log-in" class="h-full flex flex-col justify-between">
                <span id="log-in-section">
                    <TitleComponent class="m-5">Log In</TitleComponent>
                    <hr class="m-5 border-text-color"/>
                    <form @submit.prevent="logInWithEmail" class="flex flex-col">
                        <input type="text" v-model="email" placeholder="Email" class="mx-5 mt-5 p-2 rounded-lg">
                        <input type="password" v-model="password" placeholder="Password" class="mx-5 mt-5 p-2 rounded-lg">
                        <input type="submit" value="Log In" class="m-5 p-2 rounded-lg bg-accent-color cursor-pointer hover:bg-hover-accent-color"/>
                    </form>
                </span>
            
                <span id="sign-up-section" class="mb-5">
                    <hr class="m-5 border-text-color"/>
                    <p class="text-text-color cursor-pointer" @click="toggleSignInScreen">Sign in with email</p>
                </span>
            </span>
            <span v-else id="sign-up" class="h-full flex flex-col justify-between">
                <span id="sign-up-section">
                    <TitleComponent class="m-5">Sign Up</TitleComponent>
                    <hr class="m-5 border-text-color"/>
                    <form @submit.prevent="signUpWithEmail" class="flex flex-col">
                        <input type="text" v-model="username" placeholder="Username" class="mx-5 mt-5 p-2 rounded-lg">
                        <input type="text" v-model="email" placeholder="Email" class="mx-5 mt-3 p-2 rounded-lg">
                        <input type="password" v-model="password" placeholder="Password" class="mx-5 mt-3 p-2 rounded-lg">
                        <input type="password" v-model="confirmPassword" placeholder="Confirm Password" class="mx-5 mt-3 p-2 rounded-lg">
                        <CountryDropdown class="mx-5 mt-3 p-2 rounded-lg" v-model="country"/>
                        <input type="submit" value="Sign Up" class="m-5 mt-5 p-2 rounded-lg bg-accent-color cursor-pointer hover:bg-hover-accent-color"/>
                    </form>
                </span>
            
                <span id="sign-up-section" class="mb-5">
                    <hr class="m-5 border-text-color"/>
                    <p class="text-text-color cursor-pointer" @click="toggleSignInScreen">Log In</p>
                </span>
            </span>
        </div>
    </div>
    </template>
    
    <script setup>
    import TitleComponent from "../components/TitleComponent.vue"
    import CountryDropdown from "../components/CountryDropdown.vue"
    import Protocol from '../webclient/Protocol'
    import {ref} from 'vue'
    import clientUser from '@/user/ClientUser'
    import { webClient } from "@/webclient/WebClient"

    const emit = defineEmits(['leave'])

    var username = ref('donde');
    var email = ref('pablo_my_love@gmail.com');
    var password = ref('1999donde@');
    var confirmPassword = ref('1999donde@');
    var country = ref('');

    var isSigningIn = ref(false);

    const backgroundId = 'sign-up--background';
    
    async function logInWithEmail(event) {
        console.log(email.value);
        console.log(password.value);
    
        const response = await webClient.APIRequestPost("/log-in", {
            email: email.value,
            password: password.value
        })
        console.log(response.success);

        // if login successful, update user, and leave signup
        if (response.success == Protocol.success) {
            clientUser.logIn();
            emit("leave");
        }
        console.log(response);
    }

    async function signUpWithEmail(event) {
        const response = await webClient.APIRequestPost('/sign-up', {
            username: username.value,
            country: country.value,
            email: email.value,
            password: password.value
        });

        if (response.status == Protocol.success)
            emit("leave");
        
        console.log(response);
        
    }

    function toggleSignInScreen() {
        isSigningIn.value = !isSigningIn.value;
    }

    function leave(event) {
        if (event.target.id !== backgroundId) {
            return
        }
        isSigningIn.value = false;
        emit('leave');
    }
    </script>