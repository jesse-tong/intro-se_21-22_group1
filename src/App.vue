<script setup>

import LoginPage from './components/views/LoginPage.vue';
import NavBar from './components/page_components/NavBar.vue';
import EasyLibLogo from './assets/EasyLib.svg';
import { onBeforeMount } from 'vue';
import {useAccountStore} from './components/stores/LoginInfoStore';

onBeforeMount(() => {
  const store = useAccountStore();
  store.setAccountFromLocal();
});


</script>

<template>
  <Notifications position="bottom right" :duration=7000 :max=1 :closeOnClick=true data-testid="notification"/>
  <div>
    <RouterView name="NavBar" />
    <RouterView />
    <RouterView name="footer" />
  </div>
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
