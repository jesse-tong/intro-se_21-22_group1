<template>
  <div class="table-responsive">
    <table class="table table-striped">
      <thead>
        <tr>
          <th>User ID</th>
          <th>Book Title</th>
          <th>Start Borrow</th>
          <th>End Borrow</th>
          <th>Returned</th>
          <th>Return Date</th>
          <th>Damaged/Lost</th>
          <th>Is Approved</th>
          <th>Borrow fees</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="borrow in borrows" :key="borrow.id" >
          <td>{{ borrow.userId }}</td>
          <td>{{ borrow.bookId }}</td> 
          <td>{{ getDateString(borrow.startBorrow) }}</td>
          <td>{{ getDateString(borrow.endBorrow) }}</td>
          <td>{{ borrow.hasReturned ? 'Yes' : 'No' }}</td>
          <td>{{ borrow.returnDate ? getDateString(borrow.returnDate) : 'N/A'}}</td>
          <td>{{ borrow.isDamagedOrLost ? 'Yes' : 'No' }}</td>
          <td>{{ borrow.isApproved ? 'Yes' : 'No' }}</td>
          <td>{{ borrow.fee }}</td>
          <td>
            <button v-if="borrow.isApproved == true && !borrow.hasReturned " class="btn btn-sm btn-primary" @click="onReturnBook(borrow.id)" data-bs-toggle="modal" data-bs-target="#returnModal">Return</button>
          </td>
        </tr>
        <tr v-if="borrows == null || borrows.length === 0" >
          <td colspan="10" ><p class="text-center"><i>Currently no borrow status data</i></p></td>
        </tr>
      </tbody>
    </table>
    <ul class="pagination">
        <li class="page-item">
            <a href="#prevPage" id="prevPage" class="page-link" @click="currentPage = currentPage > 1 ? currentPage - 1 : 1"><span>Previous page</span></a>
        </li>
        <li class="page-item">
            <input class="page-link" v-model.number="currentPage" type="number" min="1" :max="maxPage" style="max-width: 75px"/>
        </li>
        <li class="page-item">
            <a href="#mextPage" id="nextPage" class="page-link" @click="currentPage = currentPage < maxPage ? currentPage + 1 : 1"><span>Next page</span></a>
        </li>
    </ul>
  </div>
  <ReturnModal ref="returnModal" :borrowId="returnBorrowId" @update:borrowList="currentPage = 1"/>
</template>
  
<script>
import axios from 'axios';
import ReturnModal from './ReturnModal.vue';
  export default {
    components: {
        ReturnModal: ReturnModal
    },
    props: {
      bookId: {
        type: [Number, null],
        default: null,
        required: false
      },
      pageLimit: {
        type: Number,
        default: 10,
        required: false
      },
      maxPage: {
        type: Number,
        default: 50
      }
    },
    data(){
        return {
            currentPage: 1,
            addUserId: null,
            addBookId: null,
            addStartBorrow: null,
            addEndBorrow: null,

            borrows: [],
            returnBorrowId: null,
            isDamagedOrLost: null,
        }
    },
    methods: {
      getDateString(date){
        return Date(date).toLocaleString();
      },
      onReturnBook(borrowId){
        this.returnBorrowId = borrowId;
        
      },
      fetchBorrow(newCurrentPage){
        let searchParams = {};
                if (this.$props.bookId !== null){
                    searchParams.book_id = this.$props.bookId;
                }
                searchParams.page = newCurrentPage; searchParams.limit = this.$props.pageLimit;
                axios.get('/api/borrow', {
                    params: searchParams
                }).then(response => {
                    if (!response.data || !response.data.success){
                        this.$notify({
                        title: "Unknown error",
                        text: "Unknown error, this can be server or network error.",
                        type: "error"
                        });
                        return;
                    }
                    if (response.data.success === true){
                        this.borrows = response.data.result;
                    }else {
                        this.$notify({
                        title: "Fetch borrow your borrow list error",
                        text: "Fetch borrow your borrow list error: " + response.data.error,
                        type: "error"
                        });
                        return;
                    }
                }).catch(err=>{
                    this.$notify({
                        title: "Fetch borrow your borrow list error",
                        text: "Fetch borrow your borrow list error: " + err.response.data.error,
                        type: "error"
                    });
                    return;
                }).finally(()=>{
                    
                })
      }
    },
    watch: {
        currentPage: {
            handler(newCurrentPage, oldCurrentPage){
                this.fetchBorrow(newCurrentPage);
            },
            immediate: true
        }
    },
    
  };
  </script>