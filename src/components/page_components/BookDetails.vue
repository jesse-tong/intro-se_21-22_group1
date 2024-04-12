<template>
    <div style="max-width: 1200px;">
  <div class="book-detail">
    <nav class="navbar navbar-light sticky-top shadow-sm flex-wrap bg-light">
      <a class="nav-link" href="#overview">Overview</a>
      <a class="nav-link" href="#details">Details</a>
      <a class="nav-link" href="#comments">Comments</a>
      <a class="nav-link" href="#related-books">Related Books</a>
    </nav>

    <div class="container">
      
      <div class="row row-cols-md-2">
        <div class="col col-12 col-md-4" >
          <div class="list-group">
            <div class="list-group-item">
          <img :src="image" style="max-height: 350px;">
            </div>
          <div class="list-group-item">
           <div class="btn-group" role="group" style="width: 100%;">
            <button class="btn btn-secondary me-1">
              <i class="fa-solid fa-headphones"></i>
            </button> 
            <button class="btn btn-primary" @click="">Borrow</button>
            </div>
         </div>
          <div class="list-group-item">
          <button class="btn btn-secondary" style="width: 100%;">Favourite</button>
          </div>
          <div class="list-group-item">
          <span class="d-flex mb-3">
            <i v-for="i in 5" :class="[i < rating ? 'fas fa-star': 'fa-regular fa-star']"></i>
            <span class="mx-2">{{ rating }} Ratings</span>
            <span class="mx-2">{{  favorites }} Favourites</span>
          </span>
            </div>
          </div>
        </div>

        <div class="col">
          <h1 class="mb-3" style="font-family: Calibri;"><b>Book Title</b></h1>
          <p class="text-muted">by Author Name</p>
          <ul class="list-group list-group-horizontal-md">
            <li class="list-group-item">Language: English</li>
            <li class="list-group-item">Pages: 250</li>
            <span class="list-group-item">Author(s): <span class="badge bg-primary">Author 1 </span>
              <span class="badge bg-primary">Author 2 </span>
              
            </span>
            <span class="list-group-item">Genres: Genre 1, Genre 2, ...</span>
          </ul>
          <br class="br"/>
          <h4>Book Description</h4>
          

          <div class="mt-5">
            <h2 id="#comments"><b>Book Details</b></h2>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>
<script>
    export default {
        data() {
            return {
                image: "",
                description: "",
                rating: 0,
                favorites: 0,
                borrowed
            }
        },
        props: {
            bookId: String,

        },
        watch: {
            fetchBookDetails: {
                getBookDetails(){

                },
                immediate: true
            }
            
        },
        methods: {
            borrow(){
                
            }
        }
    }
</script>