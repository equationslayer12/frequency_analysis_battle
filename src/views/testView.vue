<template>
    <p v-if="text">{{ text }}</p>
    <p v-else>Loading...</p>

    <button @click="testSocket" class="bg-pink-500 p-10 rounded-3xl font-bold hover:bg-pink-300"><p>Connect socket</p></button>
</template>

<script setup>
    import axios from 'axios'
    import {ref} from 'vue'
    var text = ref();
    async function test() {
        const response = axios.get("/api/test_socket")
        text.value = (await response).data
    }

    async function testSocket() {
        var ws = new WebSocket('ws://localhost:8080/api/test_socket_test')
        ws.onopen = (event) => {
            ws.send("hello");
            ws.send("ikappyyyy");
            console.log("heihei")
        };

        ws.onmessage = (event) => {
            text.value = event.data
        }
    }
    test();


</script>

<style scoped>
    p {
        color: white;
        font-size: 5rem;
    }
</style>