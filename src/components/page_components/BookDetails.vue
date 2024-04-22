<template>
  
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
          <img :src="apiSite + '/image/' + $props.bookId" style="max-height: 350px;" :alt="'Image for book: ' + book.title">
            </div>
          <div class="list-group-item">
           <div class="btn-group" role="group" style="width: 100%;">
            <button class="btn btn-secondary me-1">
              <i class="fa-solid fa-headphones"></i>
            </button> 
            <button class="btn btn-primary" @click="$emit('bookBorrow', book.id)">Borrow</button>
            </div>
         </div>
          <div class="list-group-item">
          <button class="btn btn-secondary" style="width: 100%;">Favourite</button>
          </div>
          <div class="list-group-item">
          <span class="d-flex mb-3">
            <i v-for="i in 5" :class="[i < rating ? 'fas fa-star': 'fa-regular fa-star']"></i>
            <span class="mx-2">{{ 'N/A' }} Ratings</span>
            <span class="mx-2">{{  'N/A' }} Favourites</span>
          </span>
            </div>
          </div>
        </div>

        <div class="col">
          <h1 class="mb-3" style="font-family: Calibri;"><b>{{ book.title }}</b></h1>
          <p class="text-muted">by <span v-for="author in book.authors"></span></p>
          <ul class="list-group list-group-horizontal-md">
            <!--<li class="list-group-item">Language: English</li>
            <li class="list-group-item">Pages: 250</li> -->
            <span class="list-group-item">Author(s): 
              <span class="badge bg-primary" v-for="author in book.authors">{{ author }}</span>
            </span>
            <span class="list-group-item">Genres: <span class="badge bg-primary" v-for="genre in book.genres">{{ genre }}</span></span>
          </ul>
          <br class="br"/>
          <h4>Book Description</h4>
          {{ book.description }}

          <div class="mt-5">
            <h2 id="#comments"><b>Comment</b></h2>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
    import axios from 'axios';
    export default {
        data() {
            return {
                apiSite: 'localhost:5000',
                book: null
            }
        },
        props: {
            bookId: {
             type: Number,
             required: true
            },
            
        },
        watch: {
          bookId: {
            getBookData(bookId){
                axios.get('/api/book/' + bookId, {
                params: {

                }
              }).then(response => {
                if (response.status !== 200){
                  this.$notify('Failed book fetching with status' + response.status);
                  return;
                }
                if (response.data.success == true){
                  this.book = response.data.result
                }
              }).catch(err => {
                alert('Unknown error');
                return;
              })
            },
            immediate: true 
          }
        }
    }
</script>