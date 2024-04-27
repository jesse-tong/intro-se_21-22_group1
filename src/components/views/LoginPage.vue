<template>
<div class="container my-auto mt-4">
    <div class="row">
      <div class="col-lg-4 col-md-8 col-12 mx-auto">
        <div class="card z-index-0 fadeIn3 fadeInBottom">
          <div class="card-header p-0 position-relative mt-n4 mx-3 z-index-2">
            <div class="bg-gradient-primary shadow-primary rounded-4 py-3 pe-1">
              <h4 class="text-white font-weight-bolder text-center mt-2 mb-0">Sign in</h4>
              <div class="row mt-3">
                <div class="col-2 text-center ms-auto">
                  <RouterLink class="btn btn-link px-3" to="/login/facebook">
                    <i class="fa fa-facebook text-white text-lg"></i>
                  </RouterLink>
                </div>
                <div class="col-2 text-center px-1">
                  <RouterLink class="btn btn-link px-3" to="/login/github">
                    <i class="fa fa-github text-white text-lg"></i>
                  </RouterLink>
                </div>
                <div class="col-2 text-center me-auto">
                  <RouterLink class="btn btn-link px-3" to="/login/google">
                    <i class="fa fa-google text-white text-lg"></i>
                  </RouterLink>
                </div>
              </div>
            </div>
          </div>
          <div class="card-body">
            <form role="form" class="text-start">
              <div class="input-group  my-3">
                <label class=" input-group-text">Email: </label>
                <input type="email" class="form-control" v-model="email">
              </div>
              <div class="input-group mb-3">
                <label class="input-group-text">Password: </label>
                <input type="password" class="form-control" v-model="password">
              </div>
              <div class="form-check form-switch d-flex align-items-center mb-3">
                <input class="form-check-input" type="checkbox" id="rememberMe" checked v-model="rememberMe">
                <label class="form-check-label mb-0 ms-3" for="rememberMe">Remember me</label>
              </div>
              <div class="text-center">
                <button type="button" class="btn bg-gradient-primary w-100 my-4 mb-2 text-white" @click="event => login()">Sign in</button>
              </div>
              <p class="mt-4 text-sm text-center">
                Don't have an account? <RouterLink to="/register" class="text-decoration-none" style="color: #ec407a;">Sign up</RouterLink>
              </p>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useAccountStore } from '../stores/LoginInfoStore';

    export default {
        data(){
            return {
                email: '',
                password: '', 
                rememberMe: '',
            }
        },
        props: {
          role: {
            type: String,
            default: 'user'
          }
        },
        watch: {

        },
        methods: {
          storeLocal(userId, email, role){
            localStorage.setItem('userId', userId);
            localStorage.setItem('email', email);
            localStorage.setItem('role', role);
          },
          storeSession(userId, email, role){
            sessionStorage.setItem('userId', userId);
            sessionStorage.setItem('email', email);
            sessionStorage.setItem('role', role);
          },
          login(){
            const accountStore = useAccountStore();
            axios.postForm('/auth/login', {
              email: this.email,
              password: this.password,
              remember: (this.rememberMe !== '' && this.rememberMe !== null) ? true : false
            }).then(response => {
              if (response.data.success === true){
                console.log(response.data.result);
                try{
                  accountStore.setAccountInfo(response.data.result.id, response.data.result.name, response.data.result.role);
                }catch(e){
                  
                }
                
                
                if (this.rememberMe !== '' && this.rememberMe !== null){
                  //Since remember user = true, store logged in user info to localStorage
                  accountStore.setLocalStorage();
                }
                this.$router.push('/');
              }else {
                this.$notify({
                  title: "Login error",
                  text: "Login with error: " + response.data.error
                })
              }
            }).catch(err=>{
              this.$notify({
                title: "Login error",
                text: "Login with error: "+ err.response.data.error,
                type: "error"
              })
            })
          }
        }
    }
</script>