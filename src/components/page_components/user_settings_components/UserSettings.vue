<template>
    <div class="row">
        <div class="col-12">
            <h5 class="section-title bg-white text-center text-primary px-3 mt-3">User Settings</h5>
        </div>
        <div class="col-12">
            <div class="mt-3 mx-3">
                <h5 class="section-title bg-white text-center text-primary px-3">Your Current Borrows</h5>
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
        },
        mounted(){
            if (this.$route.query.status){
                this.$notify({
                    text: String(this.$route.query.status).includes('failed') 
                    || String(this.$route.query.status).includes('expired') ? 'Payment failed/expired' : 'Payment success',
                    title: this.$route.query.status,
                    error: String(this.$route.query.status).includes('failed') 
                    || String(this.$route.query.status).includes('expired') ? 'error' : 'success'
                });
            }
        }
    }
</script>