<template>
    <footer >
    <div class="row row-cols-1 row-cols-sm-2 row-cols-md-4 py-4 mt-5 border-top">
      <div class="col mb-3 ps-4">
        <RouterLink class="d-flex align-items-center mb-1 link-body-emphasis text-decoration-none" to="/">
          <img :src="EasyLibLogo" height="70" width="70" alt="EasyLib logo" />
          <h4 class="ms-2">EasyLMS</h4>
        </RouterLink>
        <p class=" text-body-secondary">© 2024 
            <a href="https://github.com/jesse-tong/intro-se_21-22_group1" class="text-decoration-none"><span>Group 1</span></a>
        </p>
      </div>
      <div class="col mb-3"></div>
      <div class="col mb-3">
        <h5 class="ms-2">About EasyLMS</h5>
        <ul class="col">
            <li class="nav-item"><RouterLink to="/" class="nav-link"><span>Home</span></RouterLink></li>
            <li class="nav-item"><RouterLink to="/library-policies" class="nav-link"><span>Library policies</span></RouterLink></li>
            <li class="nav-item"><RouterLink to="/about" class="nav-link"><span>About</span></RouterLink></li>
        </ul>    
      </div>
      <div class="col mb-3 pe-3">
        <h5 class="ms-2">Books</h5>
        <ul class="col">
            <li class="nav-item"><RouterLink class="nav-link" to="/book/by-genre">By genres/categories</RouterLink></li>
            <li class="nav-item"><RouterLink class="nav-link" to="/book/by-author">By authors</RouterLink></li>
            <li class="nav-item"><RouterLink class="nav-link" to="/book/advanced-search">Advanced search</RouterLink></li>
        </ul>
      </div>
    </div>
  </footer>
</template>
<script setup>
import { RouterLink } from 'vue-router';
import EasyLibLogo from '../../assets/EasyLib.svg';
</script>