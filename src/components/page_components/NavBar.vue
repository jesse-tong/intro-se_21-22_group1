<template>
  <!-- Navbar Start -->
  <nav class="navbar navbar-expand-lg bg-white navbar-light shadow sticky-top p-0">
        <RouterLink to="/" class="navbar-brand d-flex align-items-center px-4 px-lg-5">
            <img src="/src/assets/EasyLib.svg" height="50" width="50" alt="EasyLib logo">
            <h3 class="m-0 text-primary">EasyLib</h3>
        </RouterLink>
        <button type="button" class="navbar-toggler me-4" data-bs-toggle="offcanvas" data-bs-target="#navbarOffcanvas">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div id="navbarOffcanvas" class="offcanvas offcanvas-start" tabindex="-1" aria-labelledby="offcanvasNavbarLabel" ref="sidebar" >
          <div class="offcanvas-header">
            <h5 class="offcanvas-title" id="offcanvasNavbarLabel">Menu</h5>
            <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close" ></button>
          </div>
          <div class="offcanvas-body">
            <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">      
              <div class="d-flex d-lg-none mt-3 mt-lg-0" role="search">
                <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search input" v-model="searchQuery" role="searchbox" >
                <button class="btn btn-outline-success" type="submit" @click="searchTitle()" aria-label="Search button" role="search">Search</button>
              </div>
              
              <li class="nav-item my-auto">
                <RouterLink class="nav-link" aria-current="page" to="/" @click="closeSidebar">Home</RouterLink>
              </li>
              <li class="nav-item my-auto">
                <RouterLink class="nav-link" to="/articles" @click="closeSidebar">Library news</RouterLink>
              </li>

              <li class="nav-item dropdown my-auto" v-if="accountStore.isAdmin">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Admin
                </a>
                <ul class="dropdown-menu">
                  <li class="dropdown-item" v-if="accountStore.isAdmin"><RouterLink class="nav-link" to="/admin/manage-books" @click="closeSidebar">Manage books</RouterLink></li>
                  <li class="dropdown-item" v-if="accountStore.isAdmin"><RouterLink class="nav-link" to="/admin/manage-borrow" @click="closeSidebar">Manage borrow</RouterLink></li>
                  <li class="dropdown-item" v-if="accountStore.isAdmin"><RouterLink class="nav-link" to="/admin/reports" @click="closeSidebar">Reports</RouterLink></li>
                  <li class="dropdown-item" v-if="accountStore.isAdmin"><RouterLink class="nav-link" to="/admin/policies-settings" @click="closeSidebar">Policies/contacts settings</RouterLink></li>
                  <li class="dropdown-item" v-if="accountStore.isAdmin"><RouterLink class="nav-link" to="/admin/article-management" @click="closeSidebar">Article management</RouterLink></li>
                </ul>
              </li>

              <li class="nav-item dropdown my-auto">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Books
                </a>
                <ul class="dropdown-menu">
                  <li class="dropdown-item"><RouterLink class="nav-link" to="/book/by-genre" @click="closeSidebar">Genres/categories</RouterLink></li>
                  <li class="dropdown-item"><RouterLink class="nav-link" to="/book/by-author" @click="closeSidebar">Authors</RouterLink></li>
                  <li class="dropdown-item"><RouterLink class="nav-link" to="/book/advanced-search" @click="closeSidebar">Advanced search</RouterLink></li>
                </ul>
              </li>
              
              <li class="nav-item dropdown my-auto" v-if="accountStore.loggedIn">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  User
                </a>
                <ul class="dropdown-menu">
                  <li class="dropdown-item" v-if="accountStore.loggedIn"><RouterLink class="nav-link" to="/user/profile" @click="closeSidebar">User profile</RouterLink></li>
                  <li class="dropdown-item" v-if="accountStore.loggedIn"><RouterLink class="nav-link" to="/user/settings" @click="closeSidebar">User settings</RouterLink></li>
                </ul>
              </li>

              <li class="nav-item mt-0 mt-lg-0 dropdown my-auto" >
                
                <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown" 
                aria-expanded="false" v-if="accountStore.notLoggedIn">Login/Register</a>
                <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown"
                aria-expanded="false" v-else>
                    <img class="rounded-circle border border-2 d-inline me-2" width="48px" height="48px" 
                    :src="apiSite + '/api/profile_image/' + accountStore.userId " />
                    <li class="d-inline" v-if="accountStore.loggedIn">Welcome, {{ accountStore.name }}</li>
                </a>

                <ul class="dropdown-menu">
                  <li class="dropdown-item" v-if="accountStore.loggedIn">Welcome, {{ accountStore.name }}</li>
                  <li class="dropdown-item" ><RouterLink class="nav-link" to="/library-policies">Library's policies</RouterLink></li>
                  <li class="dropdown-item" v-if="accountStore.notLoggedIn" ><RouterLink class="nav-link" to="/login" id="login-link" @click="closeSidebar">Log in</RouterLink></li>
                  <li class="dropdown-item" v-if="accountStore.notLoggedIn"><RouterLink class="nav-link" to="/register" id="register-link" @click="closeSidebar">Register</RouterLink></li>
                  <li class="dropdown-item" v-if="accountStore.loggedIn" @click="logoutUser"><a class="nav-link" href="#" id="logout-link" @click="closeSidebar">Log out</a></li>
                </ul>
              </li>
              
              <li class="nav-item">
                <div class="nav-link" @click="() => { $emit('setTheme', 'light'); theme = 'light' }" style="cursor: pointer;" role="link" v-if="theme == 'dark'">
                  <i class="me-1 bi bi-sun"></i><span class="d-lg-none">Set light theme</span>
                </div>
              </li>
              <li class="nav-item">
                <div class="nav-link" @click="() => { $emit('setTheme', 'dark'); theme = 'dark' }" style="cursor: pointer;" role="link" v-if="theme == 'light'">
                  <i class="me-1 bi bi-moon-stars-fill" ></i><span class="d-lg-none">Set dark theme</span>
                </div>
              </li>

            </ul>
          </div>
        </div>
        
    </nav>


</template>

<script setup>
    import EasyLibLogo from './../../assets/EasyLib.svg';
    import { useAccountStore } from '../stores/LoginInfoStore';
    import { onBeforeMount, ref } from 'vue';
    import { useRouter, useRoute } from 'vue-router';
    import { useNotification } from '@kyvg/vue3-notification';
    import { useSearchQueryStore } from '../stores/SearchQueryStore';

    const router = useRouter();
    const route = useRoute();
    const notify = useNotification();
    const searchQueryStore = useSearchQueryStore();
    import axios from 'axios';
    
    const accountStore = useAccountStore();
    const sidebarToggler = ref(null);

    const searchQuery = ref('');
    const theme = ref('');

    const searchTitle = function(){
      searchQueryStore.saveSearchQuery(searchQuery.value, '', '');
      router.push('/book/advanced-search');
    }

    var getColorTheme = function(){
        var theme = localStorage.getItem("theme");
        if (theme === null || theme === "light"){
            return "light";
        }else {
            return theme;
        }
    }

    const closeSidebar = function(){
      if (window.innerWidth <= 768){
        //sidebarToggler.value.click();
      }
      
    }

    onBeforeMount: () => {
      theme.value = getColorTheme();
    }

    //Logout callback method
    const logoutUser = function(){
      axios.get('/auth/logout').then(response => {
                  if (response.data === null || response.data === undefined ||
                  response.data.success === undefined){
                    notify.notify({
                      title: "Logout with unknown error",
                      text: "Logout with unknown error",
                    });
                    return;
                  }
                  if (response.data.success === true){  
                    notify.notify({
                      title: "Logout successfully!",
                      text: "Logout successfully!",
                      type: 'primary'
                    }) 
                    return;
                  }else {
                    notify({
                      title: "Logout error",
                      text: "Logout failed with error: " + response.data.error,
                      type: 'error'
                    })
                    return;
                  }
                }).catch(err=>{
                  notify.notify({
                    title: "Logout error",
                    text: "Logout failed with error",
                    type: "error"
                  });
                  return;
                }).finally(()=>{
                  accountStore.clearLocalStorage();
                  accountStore.clearSessionStorage();
                  accountStore.clearStoredData();
                  router.push('/login');
                })
    }
</script>