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
                    <input type="email" class="form-control" v-model="email">
                  </div>
                  <div class="input-group  my-3">
                    <label class=" input-group-text">Name: </label>
                    <input type="email" class="form-control" v-model="name">
                  </div>
                  <div class="input-group mb-3">
                    <label class="input-group-text">Password: </label>
                    <input type="password" class="form-control" v-model="password">
                  </div>
                  <div class="input-group  my-3">
                    <label class=" input-group-text">Reenter password: </label>
                    <input type="password" class="form-control" v-model="passwordRepeat">
                  </div>
                  <div class="text-center">
                    <button type="button" class="btn bg-gradient-primary w-100 my-4 mb-2 text-white" @click="event => register()">Sign up</button>
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
              
              register(){
                if (this.password === null || this.password === ''){
                    this.$notify({
                        title: 'Empty password!',
                        text: 'Empty password!',
                        type: error
                    });
                    return;
                }
                if (this.password.length < 8){
                    this.$notify({
                        title: 'Password should have length >= 8!',
                        text: 'Password should have length >= 8!',
                        type: error
                    });
                    return;
                }
                if (this.password !== this.passwordRepeat){
                    this.$notify({
                        title: 'Incorrect reentering password!',
                        text: 'Incorrect reentering password!',
                        type: error
                    });
                    return;
                }
                axios.postForm('/auth/register', {
                  email: this.email,
                  password: this.password,
                  name: this.name,
                  role: this.$props.role
                }).then(response => {
                  if (response.data.success === true){    
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