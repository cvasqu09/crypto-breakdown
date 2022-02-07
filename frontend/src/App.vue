<script setup lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import HomePage from './components/HomePage.vue'
import TheNavBar from './components/TheNavBar.vue'
</script>

<template>
  <TheNavBar></TheNavBar>
  <router-view/>
</template>

<style>
body {
  background-color: #1e1e1e;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: white;
  margin-top: 60px;
}
</style>
