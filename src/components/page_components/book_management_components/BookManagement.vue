<template>
    <div class="card">
      <div class="card-header">
        <ul class="nav nav-tabs card-header-tabs">
          <li class="nav-item">
            <a :class="['nav-link', activeTab=='addBook' ? 'active': '']" href="#" @click="activeTab='addBook'" id="addBookTab">Add Book</a>
          </li>
          <li class="nav-item">
            <a :class="['nav-link', activeTab=='editBook' ? 'active': '']" href="#" @click="activeTab='editBook'" id="editBookTab">Edit Book</a>
          </li>
          <li class="nav-item">
            <a :class="['nav-link', activeTab=='importBook' ? 'active': '']" href="#" @click="activeTab='importBook'" id="editBookTab">Import books</a>
          </li>
        </ul>
      </div>
      <div class="card-body">
        <div v-if="activeTab == 'addBook'" >
          <AddUpdateBook @addUpdateBookCallback="addUpdateBookCallback()"/>
        </div>
        <div v-else-if="activeTab == 'editBook'" >
          <SearchBook v-model:searchBookTitle="searchBookTitle" v-model:searchBookIsbn="searchBookIsbn" v-model:searchBookId="searchBookId" @search-book="searchBook(currentPage)"/>
          <AddUpdateBook :bookId="editBookId" :isEditPage="true" @addUpdateBookCallback="addUpdateBookCallback()" ref="editBookSubtab"/>
          <BookTable @update:currentPage="(page)=>onCurrentPageChanged(page)" :books="searchResult" :currentPage="currentPage" @deleteBook="(bookId)=>onSelectDeleteBook(bookId)" @editBook="(bookId)=>{ onSelectEditBook(bookId);}" />
        </div>
        <div v-else-if="activeTab == 'importBook'">
          <ImportBookPage />
        </div>
      </div>
    </div>
</template>
<script>
    import SearchBook from '../borrow_management_components/SearchBook.vue';
    import AddUpdateBook from './AddUpdateBook.vue';
    import ImportBookPage from './ImportBookPage.vue';
    import BookTable from './BookTable.vue';
    import axios from 'axios';

    export default {
        data(){
            return {
                activeTab: 'addBook',
                searchBookTitle: '',
                searchBookIsbn: '',
                searchBookId: null,

                searchResult: [],
                currentPage: 1,

                editBookId: null,
                deleteBookId: null
            }
        },
        methods:{
          addUpdateBookCallback(){
            //Clear states after search
            this.currentPage = 1;
            this.editBookId = null;
            this.deleteBookId = null;
            this.searchResult = [];
            this.searchBookTitle = '';
            this.searchBookIsbn = '';
            this.searchBookId = null;
          },
          searchBook(page){
            //this.currentPage = 1;
            this.editBookId = null;
            this.deleteBookId = null;
            this.searchResult = [];
            
            let searchParams = {};
            if (this.searchBookTitle !== '' && this.searchBookTitle !== null){
              searchParams.title = this.searchBookTitle;
            }
            if (this.searchBookIsbn !== '' && this.searchBookIsbn !== null){
              searchParams.isbn = this.searchBookIsbn;
            }

            if (this.searchBookId !== null && this.searchBookId > 0){
              searchParams.book_id = this.searchBookId;
            }
            
            searchParams.page = this.currentPage; searchParams.limit = 10;

            axios.get('/api/book', {
              params: searchParams
            }).then(response => {
              if (!response.data){
                  this.$notify({
                      title: "Cannot fetch search results",
                      text: "Cannot fetch search results, no response. This may be from your network, server or frontend",
                      type: "error"
                  });
                  return;
              }
              if (response.data.success === true){
                this.searchResult = response.data.result;
              }else {
                this.$notify({
                  title: "Cannot fetch search result",
                  text: "Cannot fetch search result, with error: " + response.data.error,
                  type: "error"
                });
                return;
              }
            }).catch(err => {
              this.$notify({
                  title: "Cannot fetch search result",
                  text: "Cannot fetch search result, with error: " + err.response.data.error,
                  type: "error"
              });
              return;
            })
          },
          onCurrentPageChanged(page){
            if (page === '' || page === null){
              return; 
            }
            try{
              let pageNum = parseInt(page);
              this.currentPage = pageNum;
              this.searchBook(this.currentPage);
            }catch(e){

            }
            
          },
          onSelectEditBook(bookId){
            this.editBookId = bookId;
          },
          onSelectDeleteBook(bookId){
            this.deleteBookId = bookId;
            this.deleteBook();
          },
          deleteBook(){
            if (this.deleteBookId === '' || this.deleteBookId === null){
              this.$notify({
                title: 'Error deleting book',
                text: 'No book ID selected to delete',
                type: 'error'
              });
              return;
            }
            axios.delete('/api/book/' + this.deleteBookId).then(response=>{
              if (!response.data || !response.data.success){
                this.$notify({
                  title: 'Unknown error',
                  text: 'Unknown error, this can be server or network error',
                  type: 'error'
                });
                return;
              }
              if (response.data.success === true){
                this.$notify({
                  title: 'Delete book successfully!',
                  text: 'Delete book successfully!',
                  type: 'success'
                });
                this.searchBook(this.currentPage);
                
              }else {
                this.$notify({
                  title: 'Delete error',
                  text: 'Delete book failed with error: ' + response.data.error,
                  type: 'error'
                });
                return;
              }
            }).catch(err=>{
              this.$notify({
                  title: 'Delete error',
                  text: 'Delete book failed with error: ' + err.response.data.error,
                  type: 'error'
                });
            }).finally(()=>{
              this.deleteBookId = null;
            })
          }
        },
        watch: {
          editBookId: {
            handler(newSelectedBookId, oldSelectedBookId){
              this.$refs.editBookSubtab.fetchInitialEditData(newSelectedBookId);
              
            }
          }
        },
        components: {
          SearchBook: SearchBook,
          BookTable: BookTable,
          AddUpdateBook: AddUpdateBook,
          ImportBookPage: ImportBookPage
        }
    }
</script>