<template>
    <h5 class="section-title bg-white text-center text-primary px-3 me-3 mt-2 ">Reset Password</h5>
    <div class=" ms-3 me-3">
        <div class="mb-2">
            <label for="currentPassword" class="form-label"><span>Current password: </span></label>
            <input type="password" class="form-control" id="currentPassword" v-model="currentPassword"/>
        </div>
        <div class="mb-2">
            <label for="newPassword" class="form-label"><span>New password: </span></label>
            <input type="password" class="form-control" id="newPassword" v-model="newPassword"/>
        </div>
        <div class="mb-2">
            <label for="newPasswordReenter" class="form-label"><span>Repeat new password: </span></label>
            <input type="password" class="form-control" id="newPasswordReenter" v-model="newPasswordReenter"/>
        </div>
        <button @click="updatePassword" class=" mb-2 btn btn-success"><span>Update password</span></button>
    </div>
</template>
<script>
    import axios from 'axios';
    import { mapStores } from 'pinia';
    import { useAccountStore } from '../../stores/LoginInfoStore';
    export default {
        data(){
            return {
                currentPassword: '',
                newPassword: '',
                newPasswordReenter: ''
            }
        },
        created(){
            if (!this.accountStore.loggedIn){
                this.$router.push({ path: '/login', query: { error: 'You must log in first before update password!' } });
            }
        },
        computed: {
            ...mapStores(useAccountStore)
        },
        
        methods: {
            checkPassword(password){
                if (password.length >= 8 && password.match(/(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}/)){
                    return true;
                }else {
                    return false;
                }
            },
            updatePassword(){
                let updateParams = {};
                if (this.currentPassword === null || this.currentPassword === ''){
                    this.$notify({
                      title: "Current password repeat must not be empty!",
                      text: "Current password repeat must not be empty!",
                      type: "error"
                    });
                    return;
                }
                if (this.newPassword === null || this.newPassword === ''){
                    this.$notify({
                      title: "New password repeat must not be empty!",
                      text: "New password repeat must not be empty!",
                      type: "error"
                    });
                    return;
                }
                if (!this.checkPassword(this.newPassword)){
                    this.$notify({
                      title: "Invalid password!",
                      text: "Password must have at least 8 character, have at least a lowercase, a uppercase and a number character!",
                      type: "error"
                    });
                    return;
                }
                if (this.newPasswordReenter === null || this.newPasswordReenter === ''){
                    this.$notify({
                      title: "New password repeat must not be empty!",
                      text: "New password repeat must not be empty!",
                      type: "error"
                    });
                    return;
                }
                if (this.newPassword !== this.newPasswordReenter){
                    this.$notify({
                      title: "New password and repeat new password do not match!",
                      text: "New password and repeat new password do not match!",
                      type: "error"
                    });
                    return;
                }
                updateParams.old_password = this.currentPassword;
                updateParams.new_password = this.newPassword;
                axios.postForm('/auth/change-password', updateParams).then(response => {
                  if (response.data.success === true){    
                    this.$notify({
                      title: "Update user password successfully!",
                      text: "Update user password successfully!",
                      type: "success"
                    });
                    axios.get('/auth/logout').then(response => {
                        if (response.data.success === undefined){
                            /* this.$notify({
                            title: "Logout with unknown error",
                            text: "Logout with unknown error",
                            }) */
                        }
                        if (response.data.success === true){  
                            /* this.$notify({
                            title: "Logout successfully",
                            text: "Logout successfully"
                            }) */
                            this.$router.push('/login');
                        }else {
                            this.$notify({
                            title: "Logout error",
                            text: "Logout failed with error: " + response.data.error
                            })
                        }
                        }).catch(err=>{
                        /* this.$notify({
                            title: "Logout error",
                            text: "Logout failed with error: "+ err.response.data.error,
                            type: "error"
                        }) */
                        }).finally(()=>{
                            this.accountStore.clearLocalStorage();
                            this.accountStore.clearSessionStorage();
                            this.$router.push('/login');
                        })
                  }else {
                    this.$notify({
                      title: "Update user password failed",
                      text: "Update user password failed with error: " + response.data.error,
                      type: "error"
                    })
                  }
                }).catch(err=>{
                  this.$notify({
                    title: "Update user password failed",
                    text: "Update user password failed with error: "+ err.response.data.error,
                    type: "error"
                  })
                })
            },
            
        }
    }
</script>