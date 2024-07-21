<template>
    <div class="container my-auto mt-4">
        <div class="row">
          <div class="col-lg-4 col-md-8 col-12 mx-auto">
            <div class="card z-index-0 fadeIn3 fadeInBottom">
              <div class="card-header p-0 position-relative mt-n4 mx-3 z-index-2">
                <div class="bg-gradient-primary shadow-primary rounded-4 py-3 pe-1">
                  <h4 class="text-white font-weight-bolder text-center mt-2 mb-0">Register {{ $props.role === 'admin' ? ' for admin' : '' }}</h4>
                  <div class="row mt-3">
                    <div class="col-2 text-center ms-auto">
                      <RouterLink class="btn btn-link px-3" to="/register/facebook">
                        <i class="fa fa-facebook text-white text-lg"></i>
                      </RouterLink>
                    </div>
                    <div class="col-2 text-center px-1">
                      <RouterLink class="btn btn-link px-3" to="/register/github">
                        <i class="fa fa-github text-white text-lg"></i>
                      </RouterLink>
                    </div>
                    <div class="col-2 text-center me-auto">
                      <RouterLink class="btn btn-link px-3" to="/register/google">
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
                    <input type="email" class="form-control" v-model="email" id="emailInput">
                  </div>
                  <div class="input-group  my-3">
                    <label class=" input-group-text">Name: </label>
                    <input type="email" class="form-control" v-model="name" id="usernameInput">
                  </div>
                  <div class="input-group mb-3">
                    <label class="input-group-text">Password: </label>
                    <input type="password" class="form-control" v-model="password" id="passwordInput">
                  </div>
                  <div class="input-group  my-3">
                    <label class=" input-group-text">Reenter password: </label>
                    <input type="password" class="form-control" v-model="passwordRepeat" id="passwordRepeatInput">
                  </div>
                  <div class="text-center">
                    <button type="button" class="btn bg-gradient-primary w-100 my-4 mb-2 text-white" @click="event => register(false)" data-testid="registerButton" id="registerButton">Sign up</button>
                  </div>
                  <div class="text-center" v-if="waitVerification === true">
                    <button type="button" class="btn bg-gradient-primary w-100 my-4 mb-2 text-white" @click="event => register(true)" data-testid="registerButton" id="registerButton">Resend verification email</button>
                  </div>
                  <p class="mt-4 text-sm text-center">
                     Already have an account? <RouterLink to="/login" class="text-decoration-none" style="color: #ec407a;">Login</RouterLink>
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

    
        export default {
            data(){
                return {
                    email: '',
                    password: '', 
                    name: '',
                    passwordRepeat: '',
                    waitVerification: false
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
              
              register(resend_verification){
                if (this.email === null || this.email === ''){
                  this.$notify({
                        title: 'Empty email!',
                        text: 'Empty email!',
                        type: 'error'
                    });
                    return;
                }
                if (this.password === null || this.password === ''){
                    this.$notify({
                        title: 'Empty password!',
                        text: 'Empty password!',
                        type: 'error'
                    });
                    return;
                }
                if (this.password.length < 8){
                    this.$notify({
                        title: 'Password should have length >= 8!',
                        text: 'Password should have length >= 8!',
                        type: 'error'
                    });
                    return;
                }
                if (this.password !== this.passwordRepeat){
                    this.$notify({
                        title: 'Incorrect reentering password!',
                        text: 'Incorrect reentering password!',
                        type: 'error'
                    });
                    return;
                }
                axios.postForm('/auth/register', {
                  email: this.email,
                  password: this.password,
                  name: this.name,
                  role: this.$props.role,
                  resend_verification: resend_verification
                }).then(response => {
                  if (response.data.success === true){ 
                    this.$notify({
                      title: "Register successfully!",
                      text: "Register successfully! Please check verification email at: " + this.email,
                      type: "success"
                    });
                    //this.$router.push('/login');
                  }else {
                    this.$notify({
                      title: "Register error",
                      text: "Register failed with error: " + response.data.error,
                      type: "error"
                    })
                  }
                }).catch(err=>{
                  this.$notify({
                    title: "Register error",
                    text: "Register failed with error: "+ err.response.data.error,
                    type: "error"
                  })
                }).finally(() => {
                  if (resend_verification === false){
                    this.waitVerification = true;
                  }
                });
              }
            }
        }
    </script>