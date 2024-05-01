<template>
    <div class="row">
        <div class="col-12 col-lg-6">
            <UpdatePassword />
        </div>
        <div class="col-12 col-lg-6">
            <UpdateProfile />
        </div>
    </div>
</template>
<script>
    import UpdatePassword from './UpdatePassword.vue';
    import UpdateProfile from './UpdateProfile.vue';
    export default {
        components: {
            UpdatePassword: UpdatePassword,
            UpdateProfile: UpdateProfile
        }
    }
</script>