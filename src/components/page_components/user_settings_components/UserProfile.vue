<template>
    <h3 class="mt-2 ms-3 me-3">User profile:</h3>
    <div class="row ms-3 me-3">
        <div class="col-md-3 border-right">
            <div class="d-flex flex-column align-items-center text-center p-3 py-5">
                <img class="rounded-circle mt-5" width="150px" :src="apiSite + '/api/profile_image/' + userInfo.id || 'https://st3.depositphotos.com/15648834/17930/v/600/depositphotos_179308454-stock-illustration-unknown-person-silhouette-glasses-profile.jpg'">
                <span class="font-weight-bold">{{ userInfo !== null ? userInfo.name : 'N/A' }}</span>
                <span class="text-black-50">{{ userInfo !== null ? (userInfo.email !== null ? userInfo.email : 'N/A') : 'N/A' }}</span>
                <router-link class="btn btn-secondary mt-3 " role="button" to="/user/settings"><span>User settings</span></router-link>
            </div>
        </div>
        <div class="col-12 col-md-4">
            <div class=" mb-2">
                <label for="userId" class="form-label"><span>User ID: </span></label>
                <input type="text" disabled :value="userInfo !== null ? userInfo.id : 'N/A' " class="form-control" id="userId"/>
            </div>
            <div class=" mb-2">
                <label for="userEmail" class="form-label"><span>Email: </span></label>
                <input type="text" disabled :value="userInfo !== null ? userInfo.email : 'N/A'" class="form-control" id="userEmail"/>
            </div>
            <div class=" mb-2">
                <label for="userName" class="form-label"><span>Username: </span></label>
                <input type="text" disabled :value="userInfo !== null ? userInfo.name : 'N/A'" class="form-control" id="userName"/>
            </div>
            <div class=" mb-2">
                <label for="userAddress" class="form-label"><span>Address: </span></label>
                <input type="text" disabled :value="userInfo !== null ? userInfo.address : 'N/A'" class="form-control" id="userAddress"/>
            </div>
            
            <div class=" mb-2">
                <label for="userRole" class="form-label"><span>Account role: </span></label>
                <input type="text" disabled :value="userInfo !== null ? userInfo.role : 'N/A'" class="form-control" id="userRole"/>
            </div>
            
        </div>
        <div class="col-12 col-md-4">
            <div class=" mb-2">
                <label for="userAge" class="form-label"><span>Age: </span></label>
                <input type="text" disabled :value="userInfo !== null ? userInfo.age : 'N/A'" class="form-control" id="userAge"/>
            </div>
            <div class="mb-2">
                <label for="userGender" class="form-label"><span>Gender: </span></label>
                <input type="text" disabled :value="userInfo !== null ? (userInfo.gender ? userInfo.gender : 'Prefer not to say') : 'N/A' " class="form-control" id="userGender"/>
            </div>
            <div class=" mb-2">
                <label for="userPhoneNumber" class="form-label"><span>Phone number: </span></label>
                <input type="text" disabled :value="userInfo !== null ? userInfo.phone: 'N/A'" class="form-control" id="userPhoneNumber"/>
            </div>
            <!--<div class=" mb-2">
                <label for="userBorrowCount" class="form-label"><span>Borrow: </span></label>
                <input type="text" disabled :value="userInfo !== null ? (userInfo.borrowLeft + ' / ' + userInfo.maxBorrow) : 'N/A'" class="form-control" id="userBorrowCount"/>
            </div> -->
        </div>
    </div>
    
</template>
<script>
    import axios from 'axios';
    import { mapStores } from 'pinia';
    import { useAccountStore } from '../../stores/LoginInfoStore';
    export default {
        data(){
            return {
                userInfo: {
                    address: 'N/A',
                    age: 'N/A',
                    borrowLeft: 'N/A',
                    email: 'N/A',
                    gender: 'N/A',
                    email: 'N/A',
                    id: 'N/A',
                    maxBorrow: 'N/A',
                    name: 'N/A',
                    phone: 'N/A',
                    role: 'N/A'
                }
            }
        },
        created(){
            if (!this.accountStore.loggedIn){
                this.$router.push({ path: '/login', query: { error: 'You must log in first before update profile!' } });
            }
        },
        computed: {
            ...mapStores(useAccountStore)
        },
        created(){
            this.getUserProfile();
        },
        methods: {
            getUserProfile(){
                
                axios.get('/auth/profile').then(response => {
                  if (response.data.success === true){    
                    this.userInfo = response.data.result;
                  }else {
                    this.$notify({
                      title: "Fetch user information failed",
                      text: "Fetch user information failed with error: " + response.data.error,
                      type: "error"
                    })
                  }
                }).catch(err=>{
                  this.$notify({
                    title: "Fetch user information failed",
                    text: "Fetch user information failed with error: "+ err.response.data.error,
                    type: "error"
                  })
                })
            }
        }
    }
</script>