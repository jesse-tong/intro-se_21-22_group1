<template>
    <div class="card">
      <div class="card-header">
        <ul class="nav nav-tabs card-header-tabs">
          <li class="nav-item">
            <a :class="['nav-link', activeTab=='search' ? 'active': '']" href="#" @click="activeTab='search'">Search</a>
          </li>
          <li class="nav-item">
            <a :class="['nav-link', activeTab=='addBorrow' ? 'active': '']" href="#" @click="activeTab='addBorrow'">Add Borrow</a>
          </li>
          <li class="nav-item">
            <a :class="['nav-link', activeTab=='editBorrow' ? 'active': '']" href="#" @click="activeTab='editBorrow'">Add Borrow</a>
          </li>
        </ul>
      </div>
      <div class="card-body">
        <div v-if="activeTab === 'search'">
          <div class="col">
            <SearchUser v-model:searchUserEmail="searchUserEmail" v-model:searchUserName="searchUserName" v-model:searchUserId="searchUserId" @search-user="searchUser" />
            <SearchBook v-model:searchBookTitle="searchBookTitle" v-model:searchBookIsbn="searchBookIsbn" @search-book="searchBook" />
          </div>
          <div v-if="searchResultUser">
            <h3>User Search Result</h3>
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in searchResultUser" :key="user.id">
                  <td>{{ user.id }}</td>
                  <td>{{ user.name }}</td>
                  <td>{{ user.email }}</td>
                  <td>{{ user.role }}</td>
                  <td>
                    <button @click="selectUser(user.id, user.name, user.email)" class="btn btn-sm btn-success">Select</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-if="searchResultBooks">
            <h3>Book Search Results</h3>
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Publish Year</th>
                  <th>ISBN</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="book in searchResultBooks" :key="book.id">
                  <td>{{ book.title }}</td>
                  <td>{{ book.publish_year }}</td>
                  <td>{{ book.isbn }}</td>
                  <td>
                    <button @click="selectBook(book.id, book.title, book.isbn)" class="btn btn-sm btn-success">Select</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div v-else-if="activeTab === 'editBorrow'">
          <div class="row">
            <div class="col-md-3 ">
              <div class="form-group">
                <label for="editedBorrowId">Editing Borrow ID:</label>
                <input v-model="editedBorrowId" type="text" class="form-control" id="editedBorrowId" disabled>
              </div>
            </div>
            <div class="col-md-5">
              <div class="form-group">
                <label for="editedUserId">Editing User ID:</label>
                <input v-model="editedUserId" type="text" class="form-control" id="editedUserId" disabled>
              </div>
            </div>
            <div class="col-md-4">
              <div class="form-group">
                <label for="editedBookId">Editing Book ID:</label>
                <input v-model="editedBookId" type="text" class="form-control" id="editedBookId">
              </div>
            </div>
          </div>
  
          <div class="row">
            <div class="col-md-4">
              <div class="form-group">
                <label for="editStartBorrow">Start Borrow Date:</label>
                <input type="datetime-local" v-model="editedStartedBorrow" class="form-control" id="editStartBorrow">
              </div>
              <div class="form-group">
                <label for="editEndBorrow">End Borrow Date:</label>
                <input type="datetime-local" v-model="editedEndBorrow" class="form-control" id="editEndBorrow">
              </div>
              <div class="form-group">
                <label for="editReturnDate">Edit Return Date:</label>
                <input type="datetime-local" v-model="editedReturnDate" class="form-control" id="editReturnDate">
              </div>
            </div>
            <div class="col-md-4">
              <div class="mt-4">
                <div class="form-check ">
                  <label for="editedIsDamaged" class="form-check-label">Is damaged or lost</label>
                  <input type="checkbox" v-model="editedDamagedOrLost" class="form-check-input" id="editedIsDamaged" value="true">
                </div>
                <div class="form-check mt-3">
                  <label for="editedIsApproved" class="form-check-label">Is approved</label>
                  <input type="checkbox" v-model="editedIsApproved" class="form-check-input" id="editedIsApproved" value="true">
                </div>
              </div>
            </div>
            <div class="col-md-4 mt-4">
              <button @click="editBorrow" class="btn btn-primary">Submit Edit Borrow</button>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'addBorrow'">
          <div class="row">
            <div class="col-md-3 ">
              <div class="form-group">
                <label for="selectedUserId">Selected User ID:</label>
                <input v-model="selectedUserId" type="text" class="form-control" id="selectedUserId" disabled>
              </div>
            </div>
            <div class="col-md-5">
              <div class="form-group">
                <label for="selectedUserName">Selected User Name:</label>
                <input v-model="selectedUserName" type="text" class="form-control" id="selectedUserName" disabled>
              </div>
            </div>
            <div class="col-md-4">
              <div class="form-group">
                <label for="selectedUserEmail">Selected User Email:</label>
                <input v-model="selectedUserEmail" type="text" class="form-control" id="selectedUserEmail" disabled>
              </div>
            </div>
          </div>
  
          <div class="row">
            <div class="col-md-3">
              <div class="form-group">
                <label for="selectedBookId">Selected Book:</label>
                <input v-model="selectedBookId" type="text" class="form-control" id="selectedBookId" disabled>
              </div>
            </div>
            <div class="col-md-5">
              <div class="form-group">
                <label for="selectedBookTitle">Selected Book title:</label>
                <input v-model="selectedBookTitle" type="text" class="form-control" id="selectedBookTitle" disabled>
              </div>
            </div>
            <div class="col-md-4">
              <div class="form-group">
                <label for="selectedBookIsbn">Selected Book ISBN:</label>
                <input v-model="selectedBookIsbn" type="text" class="form-control" id="selectedBookIsbn" disabled>
              </div>
            </div>
            
          </div>
          <div class="row">
            <div class="col-md-4">
              <div class="form-group">
                <label for="startBorrow">Start Borrow Date:</label>
                <input type="datetime-local" v-model="startBorrow" class="form-control" id="startBorrow">
              </div>
              <div class="form-group">
                <label for="endBorrow">End Borrow Date:</label>
                <input type="datetime-local" v-model="endBorrow" class="form-control" id="endBorrow">
              </div>
            </div>
            <div class="col-md-4">
              <div class="mt-4">
                <div class="form-check ">
                  <label for="isDamaged" class="form-check-label">Is damaged or lost</label>
                  <input type="checkbox" v-model="damagedOrLost" class="form-check-input" id="isDamaged" value="true">
                </div>
                <div class="form-check mt-3">
                  <label for="isApproved" class="form-check-label">Is approved</label>
                  <input type="checkbox" v-model="isApproved" class="form-check-input" id="isApproved" value="true">
                </div>
              </div>
            </div>
            <div class="col-md-4 mt-4">
              <button @click="addBorrow" class="btn btn-primary">Add Borrow</button>
            </div>
          </div>
        </div>
        <div v-if="borrows">
          <h3>Borrow List</h3>
          <BorrowTable :borrows="borrows" @editBorrow="(borrow_status) => editBorrowChanged(borrow_status)" @deleteBorrow="(borrow_id)=> deleteBorrowChanged(borrow_id)"/>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import SearchUser from './SearchUser.vue';
  import SearchBook from './SearchBook.vue';
  import BorrowTable from './BorrowTable.vue';
  import axios from 'axios';
  
  export default {
    components: {
      SearchUser,
      SearchBook,
      BorrowTable,
    },
    data() {
      return {
        limitPerPage: 10,
        currentPage: 1,
        maxPage: 1,
        
        activeTab: 'addBorrow',
        searchUserEmail: '',
        searchUserName: '',
        searchUserId: 1,
        
        searchBookTitle: '',
        searchBookIsbn: '',
        searchBookId: null,
        
        searchResultUser: [],
        searchResultBooks: [],
        selectedUserId: '',
        selectedUserEmail: '',
        selectedUserName: '',
        selectedBookId: '',
        selectedBookTitle: '',
        selectedBookIsbn: '',
        
        startBorrow: '',
        endBorrow: '',
        returnDate: '',
        damagedOrLost: '',
        isApproved: '',
        otherBookStatus: '',
        additionalFees: 0.0,
  
        editedBorrowId: null,
        editedUserId: null,
        editedBookId: null,
        editedStartedBorrow: null,
        editedEndBorrow: null,
        editedReturnDate: null,
        editedDamagedOrLost: '',
        editedIsApproved: '',
  
        deletedBorrowId: null,
        
        borrows: [],
      };
    },
    created() {
      this.fetchBorrow(this.currentPage);
    },
    methods: {
      fetchBorrow(page){
        let postParams = {};
        postParams.page = page; postParams.limit = this.limitPerPage;
        if (this.selectedBookId !== '' || this.selectedBookId !== null){
          postParams.book_id = this.selectedBookId;
        }
        if (this.selectedUserId !== '' || this.selectedUserId !== null){
          postParams.user_id = this.selectedUserId;
        }
        axios.postForm(
          '/api/manage-borrow-admin', postParams).then(response => {
          console.log(response.data);
          if (response.data.success === true){
            this.borrows = response.data.result;
          }else {
            this.borrows = [];
            this.currentPage = 1;
            alert('Failed to fetch borrow list with error' + response.data.error);
          }
          
          }).catch(err=> {
            alert(err.responseText);
          })
      },
      
      searchUser() {
        // Implement API call to search user with email and username
        if (this.searchUserId === '' || this.searchUserId === null) {
          
        }
        // Update searchResultUser and clear searchResultBooks
        this.searchResultUser = [{
          // Update with user data from API response
          id: 2,
          name: 'John Doe',
          email: 'ejeyd@example.com',
          role: 'admin',
        }];
        this.searchResultBooks = [];
      },
      searchBook() {
        // Implement API call to search book with title and isbn
        // Update searchResultBooks and clear searchResultUser
        let search_params = {}, has_search_params = false;
        if (this.searchBookId !== '' && this.searchBookId !== null){
            search_params.book_id = this.searchBookId;
            has_search_params = true;
        }
        if (this.searchBookTitle !== '' && this.searchBookTitle !== null){
            search_params.title = this.searchBookTitle;
            has_search_params = true;
        }
        if (this.searchBookIsbn !== '' && this.searchBookIsbn !== null){
            search_params.isbn = this.searchBookIsbn;
            has_search_params = true;
        }

        if (has_search_params === false){
            this.$notify({
                title: "No parameter to search",
                text: "No book ID, title or ISBN to search",
                type: "warn"
            });
            return;
        }
        axios.get('/api/book', {
            params: search_params
        }).then(response =>{
            if (response.data.success === true){
                this.searchResultBooks = response.data.result;
            }else{

            }
        }).catch(err=>{
            this.$notify({
                title: "Search book failed",
                text: "Search book failed with error: " + err.response.data.error,
                type: "error"
            })
        }).finally(()=>{
            this.searchResultUser = [];
        })   
        
      },
      selectUser(id, name, email) {
        this.selectedUserId = id;
        this.selectedUserName = name;
        this.selectedUserEmail = email;
        //this.selectedUserId = this.searchUserId;
  
      },
      selectBook(id, book_title, isbn) {
        this.selectedBookId = id;
        this.selectedBookTitle = book_title;
        this.selectedBookIsbn = isbn;
        //this.searchResultBooks = []; // Clear search result after selecting
      },
      addBorrow() {
        // Implement API call to create a new borrow record
        // Update borrows data and clear selected user/book and dates
        console.log(this.startBorrow); console.log(this.endBorrow);
        const startBorrow = Date.parse(this.startBorrow);
        const endBorrow = Date.parse(this.endBorrow);
        const bookID = parseInt(this.selectedBookId);
        const userID = parseInt(this.selectedUserId);
        const returnDate = !isNaN(Date.parse(this.returnDate)) ? Date.parse(this.returnDate) : null;
        if (isNaN(startBorrow) || isNaN(endBorrow)){
          this.$notify("No start date or end date selected");
          return;
        }
        if (isNaN(bookID)){
          this.$notify("No book ID selected or invalid book ID");
          return;
        }
        if (isNaN(userID)){
          this.$notify('No user ID selected or invalid user ID');
          return;
        }
        const isDamagedOrLost = this.damagedOrLost != "" ? true : false;
        const isApproved = this.isApproved != "" ? true : false;

        axios.postForm('/api/manage-borrow-admin', {
            book_id: bookID,
            user_id: userID,
            start_borrow: this.startBorrow,
            end_borrow: this.endBorrow,
            return_date: returnDate,
            damaged_or_lost: isDamagedOrLost,
            is_approved: isApproved
        }).then(response => {
            if (response.data.success !== true){
                this.$notify({
                    title: "Add failed",
                    text: "Add borrow information failed with error: " + response.data.error,
                    type: "error"
                })
            }else {
                this.$notify({
                    title: "Add success",
                    text: "Add borrow information successfully!",
                    type: "success"
                })
            }
        }).catch(err => {
            this.$notify({
                    title: "Add borrow info error",
                    text: "Add borrow information failed with error: " + err.response.data.error,
                    type: "error"
                })
        }).finally(()=> {
            this.fetchBorrow(this.currentPage);
            
            this.selectedUserId = '';
            this.selectedBookId = '';
            this.startBorrow = '';
            this.endBorrow = '';
        })
      },
      editBorrowChanged(borrow_status){
        this.editedBorrowId = borrow_status.id;
        this.editedUserId = borrow_status.userId;
        this.editedBookId = borrow_status.bookId;
        this.editedStartedBorrow = borrow_status.startBorrow;
        this.editedEndBorrow = borrow_status.endBorrow;
        this.editedReturnDate = borrow_status.returnDate;
        this.editedDamagedOrLost = borrow_status.isDamagedOrLost;
        this.editedIsApproved = borrow_status.isApproved;
  
        
      },
      deleteBorrowChanged(borrow_id){
        this.deleteBorrowId = borrow_id;
      },
      editBorrow(){
        axios.putForm('/api/manage-borrow-admin', {
            id: this.editedBorrowId,
            book_id: this.editedBorrowId,
            user_id: this.editedUserId,
            start_borrow: this.editedStartedBorrow,
            end_borrow: this.editedEndBorrow,
            return_date: (this.editedReturnDate === null || this.editedReturnDate === '') ? null : this.editedReturnDate,
            damaged_or_lost: (this.damagedOrLost !== null || this.damagedOrLost !== '') ? true : false,
            is_approved: (this.isApproved !== null || this.isApproved !== '') ? true : false
        }).then(response => {
            if (response.data.success !== true){
                this.$notify({
                    title: "Edit failed",
                    text: "Edit borrow information failed with error: " + response.data.error,
                    type: "error"
                })
            }else {
                this.$notify({
                    title: "Edit success",
                    text: "Edit borrow information successfully!",
                    type: "success"
                })
            }
        }).catch(err => {
            this.$notify({
                    title: "Edit error",
                    text: "Edit borrow information failed with error: " + err.response.data.error,
                    type: "error"
                })
        }).finally(()=> {
            this.editedBorrowId = null;
            this.editedUserId = null;
            this.editedBookId = null;
            this.editedStartedBorrow = null;
            this.editedEndBorrow = null;
            this.editedReturnDate = null;
            this.editedDamagedOrLost = null;
            this.editedIsApproved = '';
        })
        
      },
      deleteBorrow(){
        if (this.deletedBorrowId == null){
          alert('No borrow ID selected to delete!');
          return;
        }
  
        axios.delete(
          '/api/delete',{
            data: {
              'borrow_id': this.deletedBorrowId
            }
          }).then((response)=>{
              const response_data = response.data;
              if (response.success == true) {
                this.$notify('Borrow deleted successfully!');
                
              }
          }).catch((err)=> {
            console.log(err);
            this.$notify("Borrow deleted with error:" + err.response.data.error);
          }).finally(()=>{
            this.deletedBorrowId = null;
          });
  
        
      },
      convertDateToUTC(date){
        let utcDate = new Date(date).toISOString();
      }
    },
  };
  </script>
  <!--
  **Explanation:**
  
  - The component imports the `SearchUser`, `SearchBook`, and `BorrowTable` components for reusability.
  - The `data` section holds properties for the active tab, search parameters, search results, selected user/book IDs, borrow dates, and borrow list.
  - The `methods` section defines functions for searching users, searching books, selecting users/books, adding borrows, and updating the borrow list.
  - Implement the logic for API calls within `searchUser`, `searchBook`, and `addBorrow` methods to interact with your backend API using libraries like Axios. Update the data accordingly based on the API responses.
    - Remember to handle errors appropriately during API calls.
  
  **Note:** This is a basic implementation, and you'll need to fill in the API call logic and error handling based on your specific backend API.*/ -->
  