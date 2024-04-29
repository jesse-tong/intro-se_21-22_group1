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
          <span class="d-flex mb-3 flex-column">
            <div>
              <span class="mx-2">Average rating: {{ rating }} </span>
              <span v-if="getNumberOfStars !== null">
                <i :class="['bi', i > getNumberOfStars ? 'bi-star' : 'bi-star-fill']" v-for="i in 5"></i>
              </span>
            </div>
            <div>
              <span class="mx-2">{{  'N/A' }} Favourites</span>
            </div>
            
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
            <CommentSection :bookId="parseInt($props.bookId)" />
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
    import CommentSection from '../comment_components/CommentSection.vue';
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
          BorrowModal,
          CommentSection
        },
        props: {
            bookId: {
             type: [Number, String],
             required: true
            },
            
        },
        computed: {
            getNumberOfStars(){
              if (this.rating === 'N/A' || this.rating === '' || this.rating === null){
                return null;
              }else {
                return Math.max(Math.round(this.rating / 2), 5);
              }
            }
        },
        created(){
          this.getBookData(this.$props.bookId);
          this.getRating(this.$props.bookId);
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
          },
          getRating(bookId){

            axios.get('/api/book-average-rating/' + bookId, {
                params: {

                }
              }).then(response => {
                if (response.status !== 200 || !response.data || response.data.success === false){
                  this.$notify({
                    title: 'Failed to get average rating',
                    text: 'Failed to get average rating',
                    type: 'error'
                  });
                  return;
                }
                if (response.data.success == true){
                  this.rating = response.data.result;
                }
              }).catch(err => {
                this.$notify({
                    title: 'Failed to get average rating',
                    text: 'Failed to get average rating',
                    type: 'error'
                });
                return;
              })
          }
        },
    }
</script>