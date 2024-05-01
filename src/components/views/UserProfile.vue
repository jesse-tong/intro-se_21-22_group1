<template>
    <h3 class="mt-2 ms-3 me-3">User profile:</h3>
    <div class="row ms-3 me-3">
        <div class=" col-12 col-md-5">
            <div class="input-group mb-2">
                <label for="userId" class="input-group-text"><span>User ID: </span></label>
                <input type="text" disabled :value="userInfo.id" class="form-control" id="userId"/>
            </div>
            <div class="input-group mb-2">
                <label for="userEmail" class="input-group-text"><span>Email: </span></label>
                <input type="text" disabled :value="userInfo.id" class="form-control" id="userEmail"/>
            </div>
            <div class="input-group mb-2">
                <label for="userName" class="input-group-text"><span>Username: </span></label>
                <input type="text" disabled :value="userInfo.name" class="form-control" id="userName"/>
            </div>
            <div class="input-group mb-2">
                <label for="userAddress" class="input-group-text"><span>Address: </span></label>
                <input type="text" disabled :value="userInfo.address" class="form-control" id="userAddress"/>
            </div>
            
            <div class="input-group mb-2">
                <label for="userRole" class="input-group-text"><span>Account role: </span></label>
                <input type="text" disabled :value="userInfo.role" class="form-control" id="userRole"/>
            </div>
            
        </div>
        <div class="col-12 col-md-6">
            <div class="input-group mb-2">
                <label for="userAge" class="input-group-text"><span>Age: </span></label>
                <input type="text" disabled :value="userInfo.age" class="form-control" id="userAge"/>
            </div>
            <div class="input-group mb-2">
                <label for="userGender" class="input-group-text"><span>Gender: </span></label>
                <input type="text" disabled :value="userInfo.gender ? userInfo.gender : 'Prefer not to say'" class="form-control" id="userGender"/>
            </div>
            <div class="input-group mb-2">
                <label for="userPhoneNumber" class="input-group-text"><span>Phone number: </span></label>
                <input type="text" disabled :value="userInfo.phone" class="form-control" id="userPhoneNumber"/>
            </div>
            <div class="input-group mb-2">
                <label for="userBorrowCount" class="input-group-text"><span>Borrow: </span></label>
                <input type="text" disabled :value="userInfo.borrowLeft + ' / ' + userInfo.maxBorrow" class="form-control" id="userBorrowCount"/>
            </div>
        </div>
    </div>
    
</template>
<script>
    import axios from 'axios';
    import { mapStores } from 'pinia';
    import { useAccountStore } from '../stores/LoginInfoStore';
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