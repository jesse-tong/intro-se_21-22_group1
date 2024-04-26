<template>
  
  <div class="book-detail">
    
    <BorrowModal :showModal="borrowModalShow" @closeModal="borrowModalShow = false" ref="borrowModal" :bookId="$props.bookId"/>
    <div class="container bg-light rounded-3">
      <nav class="navbar navbar-light sticky-top shadow-sm flex-wrap bg-light rounded-3 px-3">
        <a class="nav-link" href="#overview">Overview</a>
        <a class="nav-link" href="#details">Details</a>
        <a class="nav-link" href="#comments">Comments</a>
        <a class="nav-link" href="#related-books">Related Books</a>
      </nav>
      <div class="row row-cols-md-2">
        <div class="col col-12 col-md-4" >
          <div class="list-group">
            <div class="list-group-item d-flex justify-content-between align-items-center">
                <img :src="apiSite + '/image/' + $props.bookId" style="max-height: 350px;" :alt="'Image for book: ' + book.title" class="m-auto">          
            </div>
          <div class="list-group-item">
           <div class="btn-group" role="group" style="width: 100%;">
            <button class="btn btn-secondary me-1">
              <i class="bi bi-book"></i>
            </button> 
            <button class="btn btn-primary" @click="$refs.borrowModal.modalActive()">Borrow</button>
            </div>
         </div>
          <div class="list-group-item">
          <button class="btn btn-secondary" style="width: 100%;">Favourite</button>
          </div>
          <div class="list-group-item">
          <span class="d-flex mb-3">
            
            <span class="mx-2">{{ 'N/A' }} Ratings</span>
            <span class="mx-2">{{  'N/A' }} Favourites</span>
          </span>
            </div>
          </div>
        </div>

        <div class="col-12 col-md-8">
          <h1 class="mb-3" style="font-family: Calibri;"><b>{{ book.title }}</b></h1>
          <p class="text-muted">by <span v-for="author in book.authors">{{ author + ', ' }}</span></p>
          <ul class="list-group list-group-horizontal-md">
            <p class="list-group-item">Languages: 
              <span class="badge text-bg-secondary me-2" v-for="language in book.languages">{{ language }}</span>
            </p>
            <p class="list-group-item">Author(s): 
              <span class="badge bg-secondary me-2" v-for="author in book.authors">{{ author }}</span>
            </p>
            <p class="list-group-item">Genres: <span class="badge text-bg-secondary me-2" v-for="genre in book.genres">{{ genre }}</span></p>
            
          </ul> 
          <br class="br"/>
          <h4>Book Description</h4>
          <span style="white-space: pre-wrap;">
            {{ book.description }}
          </span>
          <div class="mt-5">
            <h2 id="comments"><b>Comment</b></h2>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
    import axios from 'axios';
    import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
    import { faBook, faStar as faStarFull, faStarHalf } from '@fortawesome/free-solid-svg-icons';
    import { faStar } from '@fortawesome/free-regular-svg-icons';
    import BorrowModal from '../user_borrow_components/BorrowModal.vue';
    export default {
        data() {
            return {
                apiSite: 'http://localhost:5000',
                book: {
                  id: 0,
                  title: 'N/A',
                  authors: [],
                  genres: [],
                  description: '',
                  isbn: '',
                  rating: 'N/A'
                },
                borrowModalShow: false
            }
        },
        components: {
          FontAwesomeIcon,
          BorrowModal
        },
        props: {
            bookId: {
             type: [Number, String],
             required: true
            },
            
        },
        watch: {
          
        },
        created(){
          this.getBookData(this.$props.bookId)
        },
        methods: {
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
          }
        },
    }
</script>