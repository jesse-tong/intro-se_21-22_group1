<template>
    <h4 class="ms-3 me-3 mt-2 ">Update user information</h4>
    <div class=" ms-3 me-3">
        <div class=" mb-2">
            <label for="userId" class="form-label"><span>User ID: </span></label>
            <input type="text" disabled :value="accountStore.userId" class="form-control" id="userId"/>
        </div>
        <div class=" mb-2">
            <label for="userAge" class="form-label"><span>Age: </span></label>
            <input type="number" v-model.number="age" class="form-control" id="userAge" min="0" max="124"/>
        </div>
        <div class=" mb-2">
            <label for="userAddress" class="form-label"><span>Address: </span></label>
            <input type="text" v-model="address" class="form-control" id="userAddress"/>
        </div>
        <div class=" mb-2">
            <label for="userPhone" class="form-label"><span>Phone number: </span></label>
            <input type="text" v-model="phoneNumber" class="form-control" id="userPhone"/>
        </div>
        <div class=" mb-2">
            <label for="userGender" class="form-label"><span>Gender: </span></label>
            <select v-model="gender" class="form-control" id="userGender">
                <option value="male" >Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
                <option value="">Prefer not to say</option>
            </select>
        </div>
        <button @click="updateUserInfo" class=" mb-2 btn btn-success"><span>Update user info</span></button>
    </div>
</template>
<script>
    import axios from 'axios';
    import { mapStores } from 'pinia';
    import { useAccountStore } from '../stores/LoginInfoStore';
    export default {
        data(){
            return {
                gender: '',
                age: null,
                phoneNumber: '',
                address: '',
                phoneNumber: '',
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
            this.getUserProfile()
        },
        methods: {
            updateUserInfo(){
                let updateParams = {};
                if (this.age !== null && this.age !== ''){
                    updateParams.age = this.age;
                }
                if (this.address !== null && this.address !== ''){
                    updateParams.address = this.address;
                }
                if (this.gender !== null && this.gender !== ''){
                    updateParams.gender = this.gender;
                }
                if (this.phoneNumber !== null && this.phone !== ''){
                    updateParams.phone_number = this.phoneNumber;
                }
                axios.putForm('/auth/update-user-info', updateParams).then(response => {
                  if (response.data.success === true){    
                    this.$notify({
                      title: "Update user information successfully!",
                      text: "Update user information successfully!",
                      type: "success"
                    })
                  }else {
                    this.$notify({
                      title: "Update user information failed",
                      text: "Update user information failed with error: " + response.data.error,
                      type: "error"
                    })
                  }
                }).catch(err=>{
                  this.$notify({
                    title: "Update user information failed",
                    text: "Update user information failed with error: "+ err.response.data.error,
                    type: "error"
                  })
                })
            },
            getUserProfile(){
                
                axios.get('/auth/profile').then(response => {
                  if (response.data.success === true){    
                    let profile = response.data.result;
                    this.gender = profile.gender;
                    this.age = profile.age;
                    this.phoneNumber = profile.phone;
                    this.address = profile.address;
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