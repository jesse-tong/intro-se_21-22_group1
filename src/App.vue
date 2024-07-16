<script setup>


import { onBeforeMount } from 'vue';
import {useAccountStore} from './components/stores/LoginInfoStore';

const setStoredThemeColor = function(){
    var theme = localStorage.getItem("theme");
    if (theme === null || theme === "light"){
        document.getElementById('htmlMain').setAttribute('data-bs-theme', "light");
        localStorage.setItem("theme", "light");
    }else {
        document.getElementById('htmlMain').setAttribute('data-bs-theme', "dark");
        localStorage.setItem("theme", "dark");
    }
};
const getColorTheme = function(){
    var theme = localStorage.getItem("theme");
    if (theme === null || theme === "light"){
        return "light";
    }else {
        return "dark";
    }
};
    
const setTheme = function(theme){
    
    if (theme === "light" || theme === null){
        document.getElementById('htmlMain').setAttribute('data-bs-theme', "light");
        localStorage.removeItem("theme");
        localStorage.setItem("theme", "light");
    }else {
        document.getElementById('htmlMain').setAttribute('data-bs-theme', "dark");
        localStorage.removeItem("theme");
        localStorage.setItem("theme", "dark");
    }
};

onBeforeMount(() => {
  const store = useAccountStore();
  store.setAccountFromLocal();
  setStoredThemeColor();
});


</script>

<template >
  <Notifications position="bottom right" :duration=7000 :max=1 :closeOnClick=true data-testid="notification"/>
  <div :key="componentKey">
    <RouterView name="NavBar" @setTheme="setTheme"/>
    <RouterView />
    <RouterView name="footer"/>
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
