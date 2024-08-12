<template>
<nav class="navbar fixed-top bg-body-tertiary">
    <div class="container-fluid">
      
      <RouterLink class="navbar-brand" to="/"><img :src="EasyLibLogo" width="40" height="40" alt="EasyLib logo" />EasyLib</RouterLink>

      <button class="navbar-toggler" ref="sidebarToggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasNavigation" 
      aria-controls="offcanvasNavigation" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasNavigation" aria-labelledby="offcanvasNavbarLabel" ref="sidebar" >
        <div class="offcanvas-header">
          <h5 class="offcanvas-title" id="offcanvasNavbarLabel">Menu</h5>
          <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
          <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">      
            <div class="d-flex mt-3" role="search">
              <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search input" v-model="searchQuery" role="searchbox">
              <button class="btn btn-outline-success" type="submit" @click="searchTitle()" aria-label="Search button" role="search">Search</button>
            </div>
            <li class="nav-item mt-3" v-if="accountStore.loggedIn">
              <span>Welcome, {{ accountStore.name }}</span>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" aria-current="page" to="/" @click="closeSidebar"><i class="me-1 bi bi-house-fill"></i>Home</RouterLink>
              <RouterLink class="nav-link" to="/articles" @click="closeSidebar"><i class="me-1 bi bi-newspaper"></i>Library news</RouterLink>
            </li>
            
            <hr class="hr" v-if="accountStore.isAdmin"/>

            <li class="nav-item" v-if="accountStore.isAdmin"><RouterLink class="nav-link" to="/admin/manage-books" @click="closeSidebar"><i class="me-1 bi bi-journals"></i>Manage books</RouterLink></li>
            <li class="nav-item" v-if="accountStore.isAdmin"><RouterLink class="nav-link" to="/admin/manage-borrow" @click="closeSidebar"><i class="me-1 bi bi-database"></i>Manage borrow</RouterLink></li>
            <li class="nav-item" v-if="accountStore.isAdmin"><RouterLink class="nav-link" to="/admin/reports" @click="closeSidebar"><i class="me-1 bi bi-bar-chart"></i>Reports</RouterLink></li>
            <li class="nav-item" v-if="accountStore.isAdmin"><RouterLink class="nav-link" to="/admin/policies-settings" @click="closeSidebar"><i class="me-1 bi bi-journal-check"></i>Policies/contacts settings</RouterLink></li>
            <li class="nav-item" v-if="accountStore.isAdmin"><RouterLink class="nav-link" to="/admin/article-management" @click="closeSidebar"><i class="me-1 bi bi-newspaper"></i>Article management</RouterLink></li>
            <hr class="hr" />

            <li class="nav-item"><RouterLink class="nav-link" to="/book/by-genre" @click="closeSidebar"><i class="me-1 bi bi-collection-play"></i>Genres/categories</RouterLink></li>
            <li class="nav-item"><RouterLink class="nav-link" to="/book/by-author" @click="closeSidebar"><i class="me-1 bi bi-people"></i>Authors</RouterLink></li>
            <li class="nav-item"><RouterLink class="nav-link" to="/book/advanced-search" @click="closeSidebar"><i class="me-1 bi bi-search"></i>Advanced search</RouterLink></li>
            
            <hr class="hr" v-if="accountStore.loggedIn"/>

            <!--<li class="nav-item" v-if="accountStore.loggedIn"><RouterLink class="nav-link" to="/user/borrows">Your borrows/return book</RouterLink></li> -->
            <li class="nav-item" v-if="accountStore.loggedIn"><RouterLink class="nav-link" to="/user/profile" @click="closeSidebar"><i class="me-1 bi bi-person"></i>User profile</RouterLink></li>
            <li class="nav-item" v-if="accountStore.loggedIn"><RouterLink class="nav-link" to="/user/settings" @click="closeSidebar"><i class="me-1 bi bi-gear-fill"></i>User settings</RouterLink></li>
            
            <hr class="hr" v-if="accountStore.loggedIn"/>
            <li class="nav-item" ><RouterLink class="nav-link" to="/library-policies">Library's policies</RouterLink></li>
            <hr class="hr" />
            
            <li class="nav-item" v-if="accountStore.notLoggedIn" ><RouterLink class="nav-link" to="/login" id="login-link" @click="closeSidebar"><i class="me-1 bi bi-door-open"></i>Log in</RouterLink></li>
            <li class="nav-item" v-if="accountStore.notLoggedIn"><RouterLink class="nav-link" to="/register" id="register-link" @click="closeSidebar"><i class="me-1 bi bi-person-add"></i>Register</RouterLink></li>
            <li class="nav-item" v-if="accountStore.loggedIn" @click="logoutUser"><a class="nav-link" href="#" id="logout-link" @click="closeSidebar"><i class="me-1 bi bi-box-arrow-right"></i>Log out</a></li>
            <hr class="hr" />
            
            <li class="nav-item">
              <div class="nav-link" @click="() => { $emit('setTheme', 'light'); closeSidebar(); }" style="cursor: pointer;" role="link">
                <i class="me-1 bi bi-sun"></i><span>Set light theme</span>
              </div>
            </li>
            <li class="nav-item">
              <div class="nav-link" @click="() => { $emit('setTheme', 'dark'); closeSidebar(); }" style="cursor: pointer;" role="link">
                <i class="me-1 bi bi-moon-stars-fill" ></i><span>Set dark theme</span>
              </div>
            </li>
          </ul>
        </div>
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
      sidebarToggler.value.click();
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