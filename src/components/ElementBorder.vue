<template>
    <div class="w-fit h-fit rounded-xl">
        <slot class="rounded-inherit"/>
    </div>
</template>

<style scoped>
.rounded-inherit {
    border-radius: inherit;
}
</style>