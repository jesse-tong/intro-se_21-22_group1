<template>
    <div>
      <div class="">
        <div v-if="accountStore.loggedIn">
          <div class="input-group">
              <label for="addCommentBookId" class="input-group-text"><span>Book ID: </span></label>
              <input id="addCommentBookId" :value="$props.bookId" disabled class="form-control" />
          </div>
          <div class="input-group my-2">
              <label for="addCommentRating" class="input-group-text" ><span>Rating:</span></label>
              <input class="form-control" type="number" min="0" max="10" v-model.number="commentRating" id="addCommentRating"/>
          </div>
          <div class="form-floating">
              <textarea class="form-control" v-model="commentContent" id="addCommentContent" style="min-width: 175px;"></textarea>
              <label for="commentContent">Comment text (max 3000 characters):</label>
          </div>
          <button class="btn btn-primary mt-2" @click="addComment" id="addCommentButton"><span>Add comment</span></button>
          <hr class="hr" />
        </div>
        <div class="col">
          
          <CommentCard v-for="comment in comments" :comment="comment" @updateCommentList="()=>fetchComments(currentPage)" />
          
          <ul class="pagination">
                <li class="page-item">
                    <a href="#prevPageButton" class="page-link" @click="currentPage =  currentPage > 1 ? currentPage - 1 : 1" id="prevPageButton"><span>Previous page</span></a>
                </li>
                <li class="page-item">
                    <input @input="(e)=> {currentPage = e.target.value}" type="number" min="1"  class="page-link" style="max-width: 95px" :value="currentPage">
                </li>
                <li class="page-item">
                    <a href="#nextPageButton" class="page-link" @click="currentPage =  currentPage + 1" id="nextPageButton"><span >Next page</span></a>
                </li>
            </ul>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { useAccountStore } from '../../stores/LoginInfoStore';
  import {  mapStores } from 'pinia';
  import CommentCard from './CommentCard.vue';
  import axios from 'axios';
  export default {
    props: {
      bookId: {
        type: Number,
        required: true
      },
      perPage: {
        type: Number,
        default: 10,
      },
    },
    data() {
      return {
        currentPage: 1,
        comments: [],
        commentRating: null,
        commentContent: '',
      }
    },
    computed: {
      ...mapStores(useAccountStore)
    },
    watch: {
      
      currentPage: {
        handler(newCurrentPage, oldCurrentPage){
          this.fetchComments(newCurrentPage);
        },
        immediate: true
      }
    },
    methods: {
      changePage(page) {
        this.currentPage = Math.max(1, page)
      },
      fetchComments(page){
        axios.get('/api/comment/' + this.$props.bookId, {
            params: {
              page: page,
              limit: this.$props.perPage
            }
          }).then(response=> {
                if (!response.data || response.data == undefined || !response.data.success){
                    this.$notify({
                        title: "Fetch comments failed",
                        text: "Fetch comments failed with unknown error, this can be from network or server",
                        type: "error"
                    });

                    return;
                }
                if (response.data.success === true){
                    
                    this.comments = response.data.result;
                }else{
                    this.$notify({
                        title: "Fetch comments failed",
                        text: "Fetch comments failed with error: " + response.data.error,
                        type: "error"
                    });
                    
                }   
            }).catch(err=>{
                this.$notify({
                    title: "Fetch comments failed",
                    text: "Fetch comments failed with error: " + err.response.data.error,
                    type: "error"
                })
            }).finally(()=>{
                
            });
      },
      addComment(){
        if (this.commentRating === null || this.commentRating < 0 || this.commentRating > 10){
          this.$notify({
            title: "No rating or invalid comment rating!",
            text: "No rating or invalid comment rating",
            type: "error"
          });
          return;
        }
        if (this.commentContent.length > 3000){
          this.$notify({
            title: "Comment's length is too much!",
            text: "Comment's length is too much!",
            type: "error"
          });
          return;
        }
        axios.postForm("/api/comment", {
          book_id: this.$props.bookId,
          comment: this.commentContent,
          rating: this.commentRating
        }).then(response=> {
                if (!response.data || response.data == undefined || !response.data.success){
                    this.$notify({
                        title: "Add comment failed",
                        text: "Fetch comments failed with unknown error, this can be from network or server",
                        type: "error"
                    });

                    return;
                }
                if (response.data.success === true){
                    
                  this.$notify({
                    title: "Add comment successfully!",
                    text: "Add comment successfully with comment ID: "+ response.data.result.id,
                    type: "success"
                  });
                  this.fetchComments(this.currentPage);
                }else{
                    this.$notify({
                        title: "Fetch comments failed",
                        text: "Fetch comments failed with error: " + response.data.error,
                        type: "error"
                    });
                    
                }   
            }).catch(err=>{
                this.$notify({
                    title: "Fetch comments failed",
                    text: "Fetch comments failed with error: " + err.response.data.error,
                    type: "error"
                })
            }).finally(()=>{
                
            });
      }
    },
    components: {
      CommentCard: CommentCard
    }
  }
  </script>
  
  <style scoped>
  /* Add any specific styling for the component here */
  </style>
  