<script setup>

import LoginPage from './components/views/LoginPage.vue';
import NavBar from './components/page_components/NavBar.vue';
import { onBeforeMount } from 'vue';
import {useAccountStore} from './components/stores/LoginInfoStore';

onBeforeMount(() => {
  const store = useAccountStore();
  store.setAccountFromLocal();
});


</script>

<template>
  <Notifications position="top right" />
  <RouterView name="NavBar" />
  <RouterView />
  
  <footer>
    
  </footer>

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
