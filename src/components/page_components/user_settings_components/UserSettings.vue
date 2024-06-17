<template>
    <div class="row">
        <div class="col-12">
            <h3 class="ms-3 mt-2">User settings</h3>
        </div>
        <div class="col-12">
            <div class="mt-3 mx-3">
                <h4>Your current borrows</h4>
                <BorrowTableUser />
            </div>
        </div>
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
    import BorrowTableUser from '../user_borrow_components/BorrowTableUser.vue';
    export default {
        components: {
            UpdatePassword: UpdatePassword,
            UpdateProfile: UpdateProfile,
            BorrowTableUser: BorrowTableUser
        }
    }
</script>