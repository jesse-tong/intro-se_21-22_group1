<template>
<nav class="navbar bg-body-tertiary">
    <div class="container-fluid">
      
      <RouterLink class="navbar-brand" to="/"><img :src="EasyLibLogo" width="50" height="50" alt="EasyLib logo" />EasyLib</RouterLink>
      <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasNavigation" aria-controls="offcanvasNavigation" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasNavigation" aria-labelledby="offcanvasNavbarLabel">
        <div class="offcanvas-header">
          <h5 class="offcanvas-title" id="offcanvasNavbarLabel">Menu</h5>
          <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
          <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">      
            <form class="d-flex mt-3" role="search">
              <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
              <button class="btn btn-outline-success" type="submit">Search</button>
            </form>
            <li class="nav-item">
              <RouterLink class="nav-link active" aria-current="page" to="#">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/books/category">Categories</RouterLink>
            </li>
            
            <hr class="hr" v-if="accountStore.isAdmin"/>

            <li class="nav-item" v-if="accountStore.isAdmin"><RouterLink class="nav-link" to="/admin/manage-books">Manage books</RouterLink></li>
            <li class="nav-item" v-if="accountStore.isAdmin"><RouterLink class="nav-link" to="/admin/manage-borrow">Manage borrow</RouterLink></li>
            <li class="nav-item" v-if="accountStore.isAdmin"><RouterLink class="nav-link" to="/admin/reports">Reports</RouterLink></li>
            
            <hr class="hr" />

            <li class="nav-item"><RouterLink class="nav-link" to="/book/by-genre">Genres/categories</RouterLink></li>
            <li class="nav-item"><RouterLink class="nav-link" to="/book/by-author">Authors</RouterLink></li>
            <li class="nav-item"><RouterLink class="nav-link" to="/book/advanced-search">Advanced search</RouterLink></li>
            
            <hr class="hr" v-if="accountStore.loggedIn"/>

            <li class="nav-item" v-if="accountStore.loggedIn"><RouterLink class="nav-link" to="/user/borrows">Your borrows/return book</RouterLink></li>
            <li class="nav-item" v-if="accountStore.loggedIn"><RouterLink class="nav-link" to="/user/profile">User profile</RouterLink></li>
            <li class="nav-item" v-if="accountStore.loggedIn"><RouterLink class="nav-link" to="/user/settings">User settings</RouterLink></li>
            
            <hr class="hr" />
            
            <li class="nav-item" v-if="accountStore.notLoggedIn"><RouterLink class="nav-link" to="/login">Log in</RouterLink></li>
            <li class="nav-item" v-if="accountStore.notLoggedIn"><RouterLink class="nav-link" to="/register">Register</RouterLink></li>
            <li class="nav-item" v-if="accountStore.loggedIn" @click="logoutUser"><a class="nav-link" href="#">Log out</a></li>

          </ul>
        </div>
      </div>
      
    </div>
  </nav>
</template>

<script setup>
    import EasyLibLogo from './../../assets/EasyLib.svg';
    import { useAccountStore } from '../stores/LoginInfoStore';
    import { onBeforeMount } from 'vue';
    import { useRouter, useRoute } from 'vue-router';
    import { useNotification } from '@kyvg/vue3-notification';

    const router = useRouter();
    const route = useRoute();
    const notify = useNotification();
    import axios from 'axios';
    onBeforeMount(()=>{

    });
    const accountStore = useAccountStore();
    console.log('Role of account: ', accountStore.role);
    const logoutUser = function(){
      axios.get('/auth/logout').then(response => {
                  if (response.data.success === undefined){
                    notify({
                      title: "Logout with unknown error",
                      text: "Logout with unknown error",
                    }) 
                  }
                  if (response.data.success === true){  
                    notify({
                      title: "Logout successfully",
                      text: "Logout successfully"
                    }) 
                    router.push('/login');
                  }else {
                    notify({
                      title: "Logout error",
                      text: "Logout failed with error: " + response.data.error
                    })
                  }
                }).catch(err=>{
                  notify({
                    title: "Logout error",
                    text: "Logout failed with error: "+ err.response.data.error,
                    type: "error"
                  }) 
                }).finally(()=>{
                  accountStore.clearLocalStorage();
                  accountStore.clearSessionStorage();
                  router.push('/login');
                })
    }
</script>