<template>
    <div class="card shadow-sm" style=" height: 27rem; overflow: auto; opacity: 0.92;;">
            <img :src="img_src" class="card-img-top book-img" alt="..." style="height: 100%; width: 100%; object-fit: contain;">
            <div class=" bg-opacity-50 mt-2">
              <div class='row'>
                <div class='col-7'>
                  <h5 class="card-title px-3">{{ title }}</h5>
                  <p class="text-sm px-3"><i>By {{ authors.join(', ') }}</i></p>
                </div>
                <div class='col'>
                  <p>Average rating: {{ avg_rating }}</p>
                </div>
              </div>
              <div class="card-body text-decoration-none bg-opacity-50">
                <p class="card-text">{{  description.length > 60 ? description.substring(0, 60) + '...' : description }}</p>
                <router-link to="{path: 'book', params: {bookId: bookId}}" class="btn btn-success">More information</router-link>
              </div>
            </div>
          </div>
</template>
<script>
    import { RouterLink } from 'vue-router';
    export default {
        data(){
          return {}
        },
        props: {
            authors: Array,
            title: String,
            avg_rating: Number,
            description: String,
            img_src: String,
            bookId: Number,
        },
        methods: {

        }
    }
</script>