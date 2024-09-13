<template>
    <div class="row">
        <AdminSidebar class="d-none d-lg-block col-lg-2 col-xl-2 col-xxl-2" />
        <div class="col-12 col-lg-10 col-xl-10 col-xxl-10">
            <RouterView></RouterView>
        </div>
    </div>
</template>
<script setup>
import AdminSidebar from './AdminSidebar.vue';
</script>