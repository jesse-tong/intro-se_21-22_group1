<template>
  
  <div class="book-detail">
    
    <BorrowModal :showModal="borrowModalShow" @closeModal="borrowModalShow = false" ref="borrowModal" :bookId="$props.bookId"/>
    <EbookModal :showModal="ebookModalShow" @closeEbookModal="ebookModalShow = false" ref="ebookModal" :bookId="$props.bookId" />
    <div class="container rounded-3">
      <nav class="navbar navbar-light sticky-top shadow-sm flex-wrap rounded-3 px-3">
        <a class="nav-link" href="#overview">Overview</a>
        <a class="nav-link" href="#description">Description</a>
        <a class="nav-link" href="#comments">Comments/Reviews</a>
        <a class="nav-link" href="#related-books">Related Books</a>
      </nav>
      <div class="row row-cols-md-2">
        <div class="col col-12 col-md-4" >
          <div class="list-group">
            <div class="list-group-item d-flex justify-content-between align-items-center">
                <img :src="apiSite + '/image/' + $props.bookId + '?id=' + getRandomId" style="max-height: 350px; max-width: 100%" :alt="'Image for book: ' + book.title" class="m-auto book-img">          
            </div>
          <div class="list-group-item">
           <div class="btn-group" role="group" style="width: 100%;">
            <button class="btn btn-secondary me-1" @click="ebookModalShow = !ebookModalShow">
              <i class="bi bi-book"></i>
            </button> 
            <button class="btn btn-primary" @click="$refs.borrowModal.modalActive()" v-if="book.stock !== null && book.stock !== 0">Borrow ({{ book.stock }} left)</button>
            <button class="btn btn-primary" disabled v-else-if="book.stock == 0">Out of stock</button>
            <button class="btn btn-primary" disabled v-else>Not available to borrow</button>
            </div>
         </div>
          <div class="list-group-item">
          <button class="btn btn-secondary" style="width: 100%;" @click="favoriteBook" v-if="doesUserFavoriteBook == false">Favourite</button>
          <button class="btn btn-secondary" style="width: 100%;" @click="unfavoriteBook" v-else>Unfavourite book</button>
          </div>
          <div class="list-group-item">
          <span class="d-flex mb-3 flex-column">
            <div>
              <span class="mx-2">Average rating: {{ rating !== 'N/A' && rating !== null ? Math.round(rating*100)/100 : 'N/A' }} </span>
              <span v-if="getNumberOfStars !== null">
                <i :class="['bi text-warn', i > getNumberOfStars ? 'bi-star' : 'bi-star-fill']" v-for="i in 5"></i>
              </span>
            </div>
            <div>
              <span class="mx-2">{{  favoriteCount !== null ? favoriteCount : 'N/A' }} Favourites</span>
            </div>
            
          </span>
            </div>
          </div>
        </div>

        <div class="col-12 col-md-8" id="overview">
          <h1 class="mb-3" style="font-family: 'Calibri', 'Helvetica';"><b>{{ book.title }}</b></h1>
          <p class="text-muted">by <span v-for="author in book.authors">{{ author + ', ' }}</span></p>
          <div style="max-width: 100%">
            <ul class="list-group list-group-horizontal-lg w-100">
              <p class="list-group-item m-0">Languages: 
                <span class="badge text-bg-secondary me-0 me-lg-2" v-for="language in book.languages" data-testid="languageBadge">{{ language }}</span>
              </p>
              <p class="list-group-item m-0">Author(s): 
                <span class="badge bg-secondary me-0 me-lg-2" v-for="author in book.authors" data-testid="authorBadge">{{ author }}</span>
              </p>
              <p class="list-group-item m-0">Genre(s): 
                <span class="badge text-bg-secondary me-0 me-lg-2" v-for="genre in book.genres" data-testid="genreBadge">{{ genre }}</span>
              </p>
              <p class="list-group-item m-0">ISBN: {{ book.isbn }}</p>
            </ul> 
          </div>
          
          <br class="br"/>
          <h4 id="description"><b>Book Description</b></h4>
          <span style="white-space: pre-wrap;">
            {{ book.description }}
          </span>
          <div class="mt-5">
            <h3 id="comments"><b>Comments/Reviews</b></h3>
            <CommentSection :bookId="parseInt($props.bookId)" />
          </div>
        </div>
        
      </div>
      <div class="">
        <h3 id="related-books"><b>Related books</b></h3>
        <h6 class="mb-3"><i>Related books that other users borrowing this book also borrow</i></h6>
        <BookCarousel :imgHeight=250 :books="relatedBooks" v-if="relatedBooks !== null && relatedBooks.length !== 0"/>
        <h5 v-else><i>Related books not available</i></h5>
      </div>
    </div>
  </div>
</template>
<script>
    import axios from 'axios';
    import BookCarousel from '../homepage_components/BookCarousel.vue';
    import BorrowModal from '../user_borrow_components/BorrowModal.vue';
    import CommentSection from '../comment_components/CommentSection.vue';
    import EbookModal from '../EbookModal.vue';
    import { v4 as uuidv4 } from 'uuid';
    export default {
        data() {
            return {
                rating: 'N/A',
                book: {
                  id: 0,
                  title: 'N/A',
                  authors: [],
                  genres: [],
                  description: '',
                  isbn: '',
                  rating: 'N/A',
                  stock: null
                },
                borrowModalShow: false,
                ebookModalShow: false,
                relatedBooks: [],
                favoriteCount: null,
                doesUserFavoriteBook: false
            }
        },
        components: {
          BorrowModal,
          CommentSection,
          BookCarousel,
          EbookModal
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
                var stars = Math.round(parseFloat(this.rating) / 2);
                if (stars > 5){ stars = 5; } else if (stars < 0) { stars = 0; }
                return stars;
              }
            },
            getRandomId(){
              //This will generated a random uuid and added to img src as a query 
              //so that Vue will not use the cached image but the updated one instead
                return uuidv4();
            }
        },
        created(){
          this.getBookData(this.$props.bookId);
          this.getRating(this.$props.bookId);
          this.getRelatedBooksByBorrow(this.$props.bookId);
          this.getFavoriteCount();
        },
        methods: {
          getBookData(bookId){
              axios.get('/api/book/' + bookId, {
                params: {

                }
              }).then(response => {
                if (response.status !== 200){
                  this.$notify('Failed book fetching with status' + response.status);
                  this.$router.push({name: 'not-found-inner'});
                  return;
                }
                if (response.data.success == true){
                  this.book = response.data.result
                }else {
                  this.$router.push({name: 'not-found-inner'});
                }
              }).catch(err => {
                
                this.$router.push({name: 'not-found-inner'});
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
          },
          getRelatedBooksByBorrow(bookId){
            axios.get('/api/related-books/' + bookId).then(response => {
                if (response.status !== 200 || !response.data || response.data === undefined 
                || response.data.success === false){
                  this.$notify({
                    title: 'Failed to get related books',
                    text: 'Failed to get related books that other users borrow this book borrows',
                    type: 'error'
                  });
                  return;
                }
                if (response.data.success == true){
                  this.relatedBooks = response.data.result;
                }
              }).catch(err => {
                this.$notify({
                  title: 'Failed to get related books',
                    text: 'Failed to get related books that other users borrow this book borrows',
                    type: 'error'
                });
                return;
              })
          },
          getFavoriteCount(){
            axios.get('/api/favorite/' + this.$props.bookId).then(response => {
              if (response.data !== undefined && response.data !== null 
              && response.status === 200 && response.data.success === true){
                this.favoriteCount = response.data.result.favorite_count;
                this.doesUserFavoriteBook = response.data.result.is_book_favorite_by_user;
              }else {
                this.$notify({
                  title: 'Failed to get favorite counts',
                    text: 'Failed to get favorite counts',
                    type: 'error'
                });
              }
            }).catch(err => {
              this.$notify({
                  title: 'Failed to get favorite counts',
                    text: 'Failed to get favorite counts',
                    type: 'error'
              });
            })
          },
          favoriteBook(){
            axios.post('/api/favorite/' + this.$props.bookId).then(response => {
              if (response.data !== undefined && response.data !== null 
              && response.status === 200 && response.data.success === true){
                this.$notify({
                  title: 'Favorite book successfully!',
                    text: 'Favorite book successfully!',
                    type: 'success'
                });
              }else {
                this.$notify({
                    title: 'Failed to favorite book',
                    text: 'Failed to favorite book.',
                    type: 'error'
                });
              }
            }).catch(err => {
              this.$notify({
                    title: 'Failed to favorite book',
                    text: 'Failed to favorite book.',
                    type: 'error'
                });
            }).finally(() => {
              this.getFavoriteCount();
            });
          },
          unfavoriteBook(){
            axios.delete('/api/favorite/' + this.$props.bookId).then(response => {
              if (response.data !== undefined && response.data !== null 
              && response.status === 200 && response.data.success === true){
                this.$notify({
                  title: 'Unfavorite book successfully!',
                    text: 'Unfavorite book successfully!',
                    type: 'success'
                });
              }else {
                this.$notify({
                    title: 'Failed to unfavorite book',
                    text: 'Failed to unfavorite book.',
                    type: 'error'
                });
              }
            }).catch(err => {
              this.$notify({
                    title: 'Failed to unfavorite book',
                    text: 'Failed to unfavorite book.',
                    type: 'error'
                });
            }).finally(() => {
              this.getFavoriteCount();
            });
          }

        },
    }
</script>