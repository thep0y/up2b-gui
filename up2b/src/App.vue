<template>
  <div style="display: flex;">
    <BaseSide />
    <router-view />
  </div>
</template>

<script setup lang="ts">
import BaseSide from "./components/layouts/BaseSide.vue"

</script>

<style type="text/css">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.element-plus-logo {
  width: 50%;
}
</style>