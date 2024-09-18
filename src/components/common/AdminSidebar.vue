<template>
<div class="d-flex flex-column flex-shrink-0 p-3 text-bg-dark admin-sidebar" >
    <RouterLink to="/" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-white text-decoration-none">
        <h4>Dashboard</h4>
    </RouterLink>
    <hr>
    <ul class="nav nav-pills flex-column mb-auto">
        <li class="nav-item" :class="[route.fullPath.includes('/admin/manage-borrow') ? 'active' : '']">
            <li class="nav-link" v-if="accountStore.isAdmin">
                <RouterLink class="nav-link text-white text-decoration-none" to="/admin/manage-borrow" @click="closeSidebar">Manage borrow</RouterLink>
            </li>
        </li>
        <li class="nav-item" :class="[route.fullPath.includes('/admin/manage-books') ? 'active' : '']">
            <li class="nav-link" v-if="accountStore.isAdmin">
                <RouterLink class="nav-link text-white text-decoration-none" to="/admin/manage-books" @click="closeSidebar">Manage books</RouterLink>
            </li>
        </li>
        <li class="nav-item" :class="[route.fullPath.includes('/admin/reports') ? 'active' : '']">
            <li class="nav-link" v-if="accountStore.isAdmin">
                <RouterLink class="nav-link text-white text-decoration-none" to="/admin/reports" @click="closeSidebar">Reports</RouterLink>
            </li>
        </li>
        <li class="nav-item" :class="[route.fullPath.includes('/admin/policies-settings') ? 'active' : '']">
            <li class="nav-link" v-if="accountStore.isAdmin">
                <RouterLink class="nav-link text-white text-decoration-none" to="/admin/policies-settings" @click="closeSidebar">Policies/contacts settings</RouterLink>
            </li>
        </li>   
        <li class="nav-item" :class="[route.fullPath.includes('/admin/article-management') ? 'active' : '']">
            <li class="nav-link" v-if="accountStore.isAdmin">
                <RouterLink class="nav-link text-white text-decoration-none" to="/admin/article-management" @click="closeSidebar">Article management</RouterLink>
            </li>
        </li>
        <li class="nav-item" :class="[route.fullPath.includes('/admin/user-management') ? 'active' : '']">
            <li class="nav-link" v-if="accountStore.isAdmin">
                <RouterLink class="nav-link text-white text-decoration-none" to="/admin/user-management" @click="closeSidebar">User management</RouterLink>
            </li>
        </li>
        <li class="nav-item"  :class="[route.fullPath.includes('/admin/library-place') ? 'active' : '']">
            <li class="nav-link" v-if="accountStore.isAdmin">
                <RouterLink class="nav-link text-white text-decoration-none" to="/admin/library-place" @click="closeSidebar">Library location/session management</RouterLink>
            </li>
        </li>
    </ul>
    <hr />
    
</div>
</template>
<script setup>
import { useAccountStore } from '../stores/LoginInfoStore';
import { RouterLink, useRoute } from 'vue-router';

const accountStore = useAccountStore();
const route = useRoute();
const closeSidebar = () => {}
</script>

<style lang="css" scoped>
.nav-item.active {
    background-color: #007bff;
    border-radius: 10px;
    backdrop-filter: blur(10px);
    opacity: 0.85;
}
</style>