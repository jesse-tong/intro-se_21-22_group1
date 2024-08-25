<script setup>

import axios from 'axios';
import { onBeforeMount } from 'vue';
import {useAccountStore} from './components/stores/LoginInfoStore';
import { VueElement } from 'vue';


const setStoredThemeColor = function(){
    var theme = localStorage.getItem("theme");
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.getElementById('htmlMain').setAttribute('data-bs-theme', "dark");
        localStorage.setItem("theme", "dark");
    }
    else if (theme === null || theme === "light"){
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

const getCSRFToken = function(){
  axios.get('/auth/csrf_token').then(response => {
    if (response.data !== null && response.data !== undefined && response.data.csrf_token){
      //For some reasons the csrf token is not being set in the headers but the cookie is being set
      //when using axios.defaults.headers.common["X-CSRFToken"] = response.data.csrf_token;
      axios.defaults.headers.get["X-CSRFToken"] = response.data.csrf_token;
      axios.defaults.headers.post["X-CSRFToken"] = response.data.csrf_token;
      axios.defaults.headers.put["X-CSRFToken"] = response.data.csrf_token;
      axios.defaults.headers.patch["X-CSRFToken"] = response.data.csrf_token;
      axios.defaults.headers.delete["X-CSRFToken"] = response.data.csrf_token;
    }
  }).catch(err => {
    console.error('Failed to get CSRF token: ' + err);
  });
}


onBeforeMount(() => {
  const store = useAccountStore();
  store.setAccountFromLocal();
  setStoredThemeColor();
  getCSRFToken();
});


</script>

<template >
  <!--<KeepAlive>-->
    <Notifications position="bottom right" :duration=9000 :max=1 :closeOnClick=true data-testid="notification" style="font-size: 15px;"/>
    <div :key="componentKey" class="bg-light-subtle">
      <RouterView name="NavBar" @setTheme="setTheme"/>
      <div>
        <RouterView />
      </div>
      <RouterView name="footer" />
    </div>
  <!--</KeepAlive>-->
  
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
