<script setup>
import PaginatedPage from './components/page_components/PaginatedPage.vue';
import LoginPage from './components/views/LoginPage.vue';
import NavBar from './components/page_components/NavBar.vue';


</script>

<template>
  <Notifications position="top right" duration="7000"/>
  <NavBar />
  <PaginatedPage />
  <LoginPage />
  

</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
