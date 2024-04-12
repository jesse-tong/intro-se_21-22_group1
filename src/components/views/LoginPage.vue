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
                  <a class="btn btn-link px-3" href="/login/facebook">
                    <i class="fa fa-facebook text-white text-lg"></i>
                  </a>
                </div>
                <div class="col-2 text-center px-1">
                  <a class="btn btn-link px-3" href="/login/github">
                    <i class="fa fa-github text-white text-lg"></i>
                  </a>
                </div>
                <div class="col-2 text-center me-auto">
                  <a class="btn btn-link px-3" href="/login/google">
                    <i class="fa fa-google text-white text-lg"></i>
                  </a>
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
                <button type="button" class="btn bg-gradient-primary w-100 my-4 mb-2 text-white">Sign in</button>
              </div>
              <p class="mt-4 text-sm text-center">
                Don't have an account? <a href="/register" class="text-decoration-none" style="color: #ec407a;">Sign up</a>
              </p>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
    export default {
        data(){
            return {
                email: '',
                password: '', 
                rememberMe: '',
            }
        },
        watch: {

        },
        methods: {

        }
    }
</script>