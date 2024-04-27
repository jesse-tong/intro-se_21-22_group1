<template>
    <div>
      <div class="">
        <div class="col">
          
          
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
  
  export default {
    props: {
      comments: Array,
      perPage: {
        type: Number,
        default: 5,
      },
    },
    data() {
      return {
        currentPage: 1,
        selectedCommentId: null,

      }
    },
    computed: {
      store() {
        return useAccountStore();
      },
      paginatedComments() {
        const start = (this.currentPage - 1) * this.perPage
        return this.comments.slice(start, start + this.perPage)
      },
    },
    watch: {
      comments: {
        immediate: true,
        handler(val) {
          this.totalPages = Math.ceil(val.length / this.perPage)
        },
      },
    },
    methods: {
      changePage(page) {
        this.currentPage = Math.max(1, Math.min(this.totalPages, page))
      },
      onConfirmEditComment(commentId){

        this.selectedCommentId = null;
      },
    },
  }
  </script>
  
  <style scoped>
  /* Add any specific styling for the component here */
  </style>
  