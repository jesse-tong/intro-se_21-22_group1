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
            <div class="d-flex mt-3" role="search">
              <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search input" v-model="searchQuery">
              <button class="btn btn-outline-success" type="submit" @click="searchTitle()" aria-label="Search button">Search</button>
            </div>
            <li class="nav-item mt-3" v-if="accountStore.loggedIn">
              <span>Welcome, {{ accountStore.name }}</span>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link active" aria-current="page" to="/">Home</RouterLink>
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

            <!--<li class="nav-item" v-if="accountStore.loggedIn"><RouterLink class="nav-link" to="/user/borrows">Your borrows/return book</RouterLink></li> -->
            <li class="nav-item" v-if="accountStore.loggedIn"><RouterLink class="nav-link" to="/user/profile">User profile</RouterLink></li>
            <li class="nav-item" v-if="accountStore.loggedIn"><RouterLink class="nav-link" to="/user/settings">User settings</RouterLink></li>
            
            <hr class="hr" v-if="accountStore.loggedIn"/>
            <li class="nav-item" ><RouterLink class="nav-link" to="/library-policies">Library's policies</RouterLink></li>
            <hr class="hr" />
            
            <li class="nav-item" v-if="accountStore.notLoggedIn" ><RouterLink class="nav-link" to="/login" id="login-link">Log in</RouterLink></li>
            <li class="nav-item" v-if="accountStore.notLoggedIn"><RouterLink class="nav-link" to="/register" id="register-link">Register</RouterLink></li>
            <li class="nav-item" v-if="accountStore.loggedIn" @click="logoutUser"><a class="nav-link" href="#" id="logout-link">Log out</a></li>

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
    onBeforeMount(()=>{

    });
    const accountStore = useAccountStore();
    console.log('Role of account: ', accountStore.role);

    const searchQuery = ref('');
    const searchTitle = function(){
      searchQueryStore.saveSearchQuery(searchQuery.value, '', '');
      router.push('/book/advanced-search');
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