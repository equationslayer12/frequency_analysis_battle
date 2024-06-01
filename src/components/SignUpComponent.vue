<template>
    <div :id="backgroundId" @click="leave" class="bg-black bg-opacity-70 transition-opacity absolute z-10 h-full w-full top-0 left-0 flex justify-center items-center">
        <div class="bg-primary-color bg-gradient-to-r from-primary-color to-background-color h-5/6 aspect-[7/10] rounded-xl opacity-100 p-5 transition-opacity">
            <span v-if="!isSigningIn" id="log-in" class="h-full flex flex-col justify-between">
                <span class="log-in-section justify-center items-center">
                    <TitleComponent class="m-5">Log In</TitleComponent>
                    <hr class="m-5 border-text-color"/>
                    <p class="text-accent-color flex justify-center items-center">{{ loginError }}</p>
                    <form @submit.prevent="logInWithEmail" class="flex flex-col">
                        <input type="text" v-model="email" placeholder="Email" class="mx-5 mt-5 p-2 rounded-lg">
                        <input type="password" v-model="password" placeholder="Password" class="mx-5 mt-5 p-2 rounded-lg">
                        <input type="submit" value="Log In" class="m-5 p-2 rounded-lg bg-accent-color cursor-pointer hover:bg-hover-accent-color"/>
                    </form>
                </span>
            
                <span id="sign-up-section" class="mb-5">
                    <hr class="m-5 border-text-color"/>
                    <p class="text-text-color cursor-pointer flex justify-center items-center" @click="toggleSignInScreen">Create an account</p>
                </span>
            </span>
            <span v-else id="sign-up" class="h-full flex flex-col justify-between">
                <span id="sign-up-section">
                    <TitleComponent class="m-5">Create an account</TitleComponent>
                    <hr class="m-5 border-text-color"/>
                    <p class="text-accent-color flex justify-center items-center">{{ signUpError }}</p>
                    <form @submit.prevent="signUpWithEmail" class="flex flex-col">
                        <input type="text" v-model="username" placeholder="Username" class="mx-5 mt-5 p-2 rounded-lg">
                        <input type="text" v-model="email" placeholder="Email" class="mx-5 mt-3 p-2 rounded-lg">
                        <input type="password" v-model="password" placeholder="Password" class="mx-5 mt-3 p-2 rounded-lg">
                        <input type="password" v-model="confirmPassword" placeholder="Confirm Password" class="mx-5 mt-3 p-2 rounded-lg">
                        <CountryDropdown class="mx-5 mt-3 p-2 rounded-lg" v-model="country"/>
                        <input type="submit" value="Create an account" class="m-5 mt-5 p-2 rounded-lg bg-accent-color cursor-pointer hover:bg-hover-accent-color"/>
                    </form>
                </span>
            
                <span id="sign-up-section" class="mb-5">
                    <hr class="m-5 border-text-color"/>
                    <p class="text-text-color cursor-pointer flex justify-center items-center" @click="toggleSignInScreen">Log in</p>
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
    import { validateUsername, validatePassword, validateEmail } from "@/lib/inputValidation"
    import { MIN_USERNAME_LENGTH, MIN_PASSWORD_LENGTH } from "@/Constants"
    
    // Emit definition
    const emit = defineEmits(['leave'])

    // Reactive variables
    let username = ref('');
    let email = ref('');
    let password = ref('');
    let confirmPassword = ref('');
    let country = ref('');

    let isSigningIn = ref(false);
    let loginError = ref('')
    let signUpError = ref('');

    // Background element ID
    const backgroundId = 'sign-up--background';
    
    // Log in with email function
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
        else {
            loginError.value = "Incorrect email or password"
        }
        console.log(response);
    }

    // Sign up with email function
    async function signUpWithEmail(event) {
        if (!validateCreds(username.value, email.value, password.value, confirmPassword.value))
            return

        const response = await webClient.APIRequestPost('/sign-up', {
            username: username.value,
            country: country.value,
            email: email.value,
            password: password.value
        });

        if (response.status == Protocol.success)
            emit("leave");
        else {
            signUpError.value = response.status;
        }
        console.log(response);
        
    }

    // Validate credentials function
    function validateCreds(username, email, password, confirmPassword) {
        signUpError.value = '';
        const isUsernameValid = validateUsername(username);
        if (!isUsernameValid) {
            signUpError.value =
                `Username must include only english letters and numbers, and must have at least ${MIN_USERNAME_LENGTH} characters`;
            console.error("invalid username");
            return false;
        }
        const isEmailValid = validateEmail(email);
        if (!isEmailValid) {
            signUpError.value = `Invalid email format`
            console.error("invalid email");
            return false;
        }
        const isPasswordValid = validatePassword(password);
        if (!isPasswordValid) {
            signUpError.value =
                `Password must include only english letters, numbers and symbols, and must have at least ${MIN_PASSWORD_LENGTH} characters`;
            console.error("invalid password");
            return false;
        }
        if (password != confirmPassword) {
            signUpError.value = "Passwords don't match"
            console.error("passwords don't match");
            return false;
        }
        return true;
    }

    // Function to toggle sign-in screen
    function toggleSignInScreen() {
        isSigningIn.value = !isSigningIn.value;
    }

    // Function to leave signup
    function leave(event) {
        if (event.target.id !== backgroundId) {
            return
        }
        isSigningIn.value = false;
        emit('leave');
    }
</script>
