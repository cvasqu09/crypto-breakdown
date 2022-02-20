<script setup lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import TheNavBar from './components/TheNavBar.vue'
</script>

<template>
  <TheNavBar></TheNavBar>
  <router-view/>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Rubik&display=swap');

body {
  background-color: #141414;
}

* {
  font-family: 'Rubik', Avenir, Helvetica, Arial, sans-serif;
}

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: white;
  margin-top: 60px;
}
</style>
