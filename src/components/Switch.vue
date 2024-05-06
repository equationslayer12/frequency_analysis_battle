<template>
    <div class="w-full flex justify-center gap-x-sm items-center text-xs underline h-min">
        <p>SHOW</p>
        <label class="switch scale" id="hiddenSwitch">
            <input type="checkbox" @change="$emit('toggle')">
            <span class="slider round">

            </span>
        </label>
        <p>HIDE</p>
    </div>
</template>

<script>
    export default {
        name: "Switch"
    }
</script>
<style>
/* The switch - the box around the slider */
.switch {
  z-index: 0;
  position: relative;
  display: inline-block;
  width: 45px;
  height: 25.5px;
}

/* Hide default HTML checkbox */
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

/* The slider */
.slider {
  @apply bg-background-color;
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  @apply bg-text-color;
  position: absolute;
  content: "";
  height: 19.5px;
  width: 19.5px;
  left: 3px;
  bottom: 3px;
  -webkit-transition: .4s;
  transition: .4s;
}

input:checked + .slider:before {
  -webkit-transform: translateX(19.5px);
  -ms-transform: translateX(19.5px);
  transform: translateX(19.5px);
}

/* Rounded sliders */
.slider.round {
  border-radius: 25.5px;
}

.slider.round:before {
  border-radius: 50%;
}
</style>