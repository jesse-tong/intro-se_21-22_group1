<template>
<div class="container my-auto mt-4">
    <div class="row">
      <div class="col-lg-4 col-md-8 col-12 mx-auto">
        <div class="card z-index-0 fadeIn3 fadeInBottom" id="loginTab">
          <div class="card-header p-0 position-relative mt-n4 mx-3 z-index-2">
            <div class="bg-gradient-primary shadow-primary rounded-4 py-3 pe-1">
              <h4 class="text-white font-weight-bolder text-center mt-2 mb-0">Sign in</h4>
              <div class="row mt-3">
                <div class="col-2 text-center ms-auto">
                  <RouterLink class="btn btn-link px-3" to="/login/facebook">
                    <i class="bi bi-facebook text-white text-lg"></i>
                  </RouterLink>
                </div>
                <div class="col-2 text-center px-1">
                  <a class="btn btn-link px-3" href="/login/github">
                    <i class="bi bi-github text-white text-lg"></i>
                  </a>
                </div>
                <div class="col-2 text-center me-auto">
                  <a class="btn btn-link px-3" href="/login/google">
                    <i class="bi bi-google text-white text-lg"></i>
                  </a>
                </div>
              </div>
            </div>
          </div>
          <div class="card-body">
            <form role="form" class="text-start">
              <div class="input-group  my-3">
                <label class=" input-group-text" for="emailInput">Email: </label>
                <input type="email" class="form-control" id="emailInput" v-model="email">
              </div>
              <div class="input-group mb-3">
                <label class="input-group-text" for="passwordInput" >Password: </label>
                <input type="password" class="form-control" id="passwordInput" v-model="password">
              </div>
              <div class="form-check form-switch d-flex align-items-center mb-3">
                <input class="form-check-input" type="checkbox" id="rememberMe" checked v-model="rememberMe">
                <label class="form-check-label mb-0 ms-3" for="rememberMe">Remember me</label>
              </div>
              <div class="text-center">
                <button id="loginSubmitButton" type="button" class="btn bg-gradient-primary w-100 my-4 mb-2 text-white" @click="event => login()">Sign in</button>
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
import gsap from 'gsap';
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
        mounted(){
          if (this.$route.query.verify_success && this.$route.query.verify_success == 'true'){
            this.$notify({
              title: 'Verify account successfully!',
              text: 'Verify account successfully!',
              type: 'success'
            })
          }else if (this.$route.query.verify_success && this.$route.query.error &&this.$route.query.error != 'null'){
            this.$notify({
              title: 'Verify account failed with error: ' + this.$route.query.error,
              text: 'Verify account failed with error: ' + this.$route.query.error,
              type: 'error'
            })
          };
          document.title = "EasyLib - Login";
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

                try{
                  accountStore.setAccountInfo(response.data.result.id, response.data.result.name,
                   response.data.result.role, response.data.result.isRestricted);
                }catch(e){
                  
                }
                this.$notify({
                  title: 'Login successfully!',
                  text: 'Login successfully!',
                  type: 'success'
                });
                
                if (this.rememberMe !== '' && this.rememberMe !== null){
                  //Since remember user = true, store logged in user info to localStorage
                  accountStore.setLocalStorage();
                  accountStore.clearSessionStorage();
                }else {
                  accountStore.setSessionStorage();
                  accountStore.clearLocalStorage();
                }
                this.$router.push('/');
              }else if (response.data.error) {
                this.$notify({
                  title: "Login error",
                  text: "Login with error: " + response.data.error,
                  type: "error"
                })
              }
            }).catch(err=>{
              if (err.response && err.response.data){
                this.$notify({
                  title: "Login error",
                  text: "Login with error: "+ err.response.data.error,
                  type: "error"
                });
              }
              
            }).finally(()=> {
                axios.post('/analytics', {
                  referer: document.referrer,
                }).then(response => {}).catch(()=>{})
              });
          }
        }
    }
</script>