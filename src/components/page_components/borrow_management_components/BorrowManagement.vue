<template>
    <div class="card">
      <div class="card-header">
        <ul class="nav nav-tabs card-header-tabs bg-transparent">
          <li class="nav-item">
            <a :class="['nav-link', activeTab=='search' ? 'active': '']" href="#searchTab" @click="activeTab='search'" id="searchTab">Search</a>
          </li>
          <li class="nav-item">
            <a :class="['nav-link', activeTab=='addBorrow' ? 'active': '']" href="#addBorrowTab" @click="activeTab='addBorrow'" id="addBorrowTab">Add Borrow</a>
          </li>
          <li class="nav-item">
            <a :class="['nav-link', activeTab=='editBorrow' ? 'active': '']" href="#editBorrowTab" @click="activeTab='editBorrow'" id="editBorrowTab" ref="editBorrowTab">Edit Borrow</a>
          </li>
        </ul>
      </div>
      <div class="card-body bg-light-subtle">
        <div v-if="activeTab === 'search'">
          <div class="col">
            <SearchUser v-model:searchUserEmail="searchUserEmail" v-model:searchUserName="searchUserName" v-model:searchUserId="searchUserId" @search-user="searchUser" />
            <SearchBook v-model:searchBookTitle="searchBookTitle" v-model:searchBookIsbn="searchBookIsbn" v-model:searchBookId="searchBookId" @search-book="searchBook" class="mt-2" />
          </div>
          <div  class="mt-3">
            <h5 class="section-title bg-light-subtle text-start text-primary pe-3">User Search Result</h5>
            <div class="table-responsive">
              <table class="table table-bordered" v-if="searchResultUser !== null && searchResultUser.length > 0">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="user in searchResultUser" :key="user.id" data-testid="searchUserResultRow">
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
            
          </div>
          <div >
            <h5 class="section-title bg-light-subtle text-start text-primary pe-3 me-3">Book Search Result</h5>
            <div class="table-responsive">
              <table class="table table-bordered" v-if="searchResultBooks !== null && searchResultBooks.length > 0">
                <thead>
                  <tr>
                    <th>Book ID</th>
                    <th>Title</th>
                    <th>Publish Year</th>
                    <th>ISBN</th>
                    <th>Stock</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="book in searchResultBooks" :key="book.id" data-testid="searchBookResultRow">
                    <td>{{ book.id }}</td>
                    <td>{{ book.title }}</td>
                    <td>{{ book.publish_year }}</td>
                    <td>{{ book.isbn }}</td>
                    <td>{{ book.stock }}</td>
                    <td>
                      <button @click="selectBook(book.id, book.title, book.isbn)" class="btn btn-sm btn-success">Select</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            
          </div>
        </div>

        <div v-else-if="activeTab === 'editBorrow'">
          <div class="row">
            <div class="col-md-3 ">
              <div class="form-group">
                <label for="editedBorrowId">Editing Borrow ID:</label>
                <input v-model="editedBorrowId" type="text" class="form-control" id="editedBorrowId" readonly>
              </div>
            </div>
            <div class="col-md-5">
              <div class="form-group">
                <label for="editedUserId">Editing User ID:</label>
                <input v-model="editedUserId" type="text" class="form-control" id="editedUserId" readonly>
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
                <div class="form-check mt-2">
                  <label for="editedIsApproved" class="form-check-label">Is approved</label>
                  <input type="checkbox" v-model="editedIsApproved" class="form-check-input" id="editedIsApproved" value="true">
                </div>
                <div class="form-check mt-2">
                  <label for="editedHasResolved" class="form-check-label">Payment has resolved</label>
                  <input type="checkbox" v-model="editedHasResolved" class="form-check-input" id="editedHasResolved" value="true">
                </div>
                <div class="form-check mt-2">
                  <label for="editedRenewPending" class="form-check-label">Renew pending</label>
                  <input type="checkbox" v-model="editedRenewPending" class="form-check-input" id="editedRenewPending" value="true">
                </div>
              </div>
            </div>
            <div class="col-md-4 mt-4">
              <button @click="editBorrow" class="btn btn-primary" id="editBorrowButton">Submit Edit Borrow</button>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'addBorrow'">
          <div class="row">
            <div class="col-md-3 ">
              <div class="form-group">
                <label for="selectedUserId">Selected User ID:</label>
                <input v-model="selectedUserId" type="text" class="form-control" id="selectedUserId" readonly>
              </div>
            </div>
            <div class="col-md-5">
              <div class="form-group">
                <label for="selectedUserName">Selected User Name:</label>
                <input v-model="selectedUserName" type="text" class="form-control" id="selectedUserName" readonly>
              </div>
            </div>
            <div class="col-md-4">
              <div class="form-group">
                <label for="selectedUserEmail">Selected User Email:</label>
                <input v-model="selectedUserEmail" type="text" class="form-control" id="selectedUserEmail" readonly>
              </div>
            </div>
          </div>
  
          <div class="row">
            <div class="col-md-3">
              <div class="form-group">
                <label for="selectedBookId">Selected Book:</label>
                <input v-model="selectedBookId" type="text" class="form-control" id="selectedBookId" readonly>
              </div>
            </div>
            <div class="col-md-5">
              <div class="form-group">
                <label for="selectedBookTitle">Selected Book title:</label>
                <input v-model="selectedBookTitle" type="text" class="form-control" id="selectedBookTitle" readonly>
              </div>
            </div>
            <div class="col-md-4">
              <div class="form-group">
                <label for="selectedBookIsbn">Selected Book ISBN:</label>
                <input v-model="selectedBookIsbn" type="text" class="form-control" id="selectedBookIsbn" readonly>
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
                <div class="form-check mt-2">
                  <label for="isApproved" class="form-check-label">Is approved</label>
                  <input type="checkbox" v-model="isApproved" class="form-check-input" id="isApproved" value="true">
                </div>
                <div class="form-check mt-2">
                  <label for="hasResolved" class="form-check-label">Borrow payment resolved</label>
                  <input type="checkbox" v-model="hasResolved" class="form-check-input" id="hasResolved" value="true">
                </div>
                <div class="form-check mt-2">
                  <label for="renewPending" class="form-check-label">Renew pending</label>
                  <input type="checkbox" v-model="renewPending" class="form-check-input" id="renewPending" value="true">
                </div>
              </div>
            </div>
            <div class="col-md-4 mt-4">
              <button @click="addBorrow" class="btn btn-primary" id="addBorrowButton">Add Borrow</button>
            </div>
          </div>
        </div>
        <div v-if="borrows">
          <h5 class="section-title bg-light-subtle text-start text-primary pe-3">Borrow list</h5>
          <BorrowTable :borrows="borrows" @editBorrow="(borrow_status) => editBorrowChanged(borrow_status)" @deleteBorrow="(borrow_id)=> deleteBorrowChanged(borrow_id)"/>
            <ul class="component-pagination">
                <li class="pagination-arrow arrow-left me-1">
                    <div style="cursor: pointer;" class="page-link" @click="currentPage =  currentPage > 1 ? currentPage - 1 : 1" id="prevPageButton"><i class="bi bi-chevron-left"></i></div>
                </li>
                <li class="page-item">
                    <li class="pagination-number current-number" ><input type="number" style="margin: 0 5px; max-width: 50px;" 
                        @input="(e)=> {currentPage = e.target.value}" :value="currentPage" min="1"/></li>
                </li>
                <li class="pagination-arrow arrow-left ms-1">
                    <div style="cursor: pointer;" class="page-link" @click="currentPage =  currentPage + 1" id="nextPageButton"><i class="bi bi-chevron-right"></i></div>
                </li>
            </ul>
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
        maxPage: 50,
        
        activeTab: 'addBorrow',
        searchUserEmail: '',
        searchUserName: '',
        searchUserId: null,
        
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
        damagedOrLost: null,
        isApproved: null,
        otherBookStatus: '',
        additionalFees: 0.0,
        hasResolved: null,
        renewPending: null,
  
        editedBorrowId: null,
        editedUserId: null,
        editedBookId: null,
        editedStartedBorrow: null,
        editedEndBorrow: null,
        editedReturnDate: null,
        editedDamagedOrLost: null,
        editedIsApproved: null,
        editedHasResolved: null,
        editedRenewPending: null,
  
        deletedBorrowId: null,
        
        borrows: [],
      };
    },
    created() {
      this.fetchBorrow(this.currentPage);
      document.title = "Borrow Management";
    },
    methods: {
      fetchBorrow(page){
        let postParams = {};
        postParams.page = page; postParams.limit = this.limitPerPage;
        if (this.selectedBookId !== '' && this.selectedBookId !== null){
          postParams.book_id = this.selectedBookId;
        }
        if (this.selectedUserId !== '' && this.selectedUserId !== null){
          postParams.user_id = this.selectedUserId;
        }
        axios.get(
          '/api/manage-borrow-admin', {
            params: postParams
          }).then(response => {

          if (response.data.success === true){
            this.borrows = response.data.result;
          }else {
            this.borrows = [];
            this.currentPage = 1;
            this.$notify('Failed to fetch borrow list with error' + response.data.error);
          }
          
          }).catch(err=> {
            this.$notify('Fetch borrow with error: ' + err.response.data.error);
          })
      },
      convertLocalDatetimeToISOString(localDatetimeString){
          //Since the value of <input type="datetime-local" /> is always YYYY-mm-ddThh:ss
          //and does not denotes any timezone, so parse it with new Date() and use toISOString() method will not work correctly
          let timeWithTimezone = new Date(localDatetimeString);
          return timeWithTimezone.toISOString();
      },
      convertISODatetimeToLocalInputString(localDatetimeString){
          //Since input="local-datetime" only accept YYYY-mm-ddThh:ss, not YYYY-mm-ddThh:ssZ of ISO string
          let currentLocalDate = new Date();
          let localTimeOffset = currentLocalDate.getTimezoneOffset() * 60 * 1000; //Get local timezone offset to GMT by milliseconds

          let gmtTime = new Date(localDatetimeString); 
          let localTime = gmtTime - localTimeOffset; localTime = new Date(localTime);
          let localISOString = localTime.toISOString();

          return localISOString.slice(0, -1); //Remove the last character of local string in ISO format
      },
      searchUser() {
        // Implement API call to search user with email and username
        if ((this.searchUserId === '' || this.searchUserId === null) 
        && (this.searchUserEmail === '' || this.searchUserEmail === null)
        && (this.searchUserName === '' || this.searchUserName === null)) {
          this.$notify({
            title: "No search query",
            text: "No user ID, email or name to search for",
            type: "warn"
          })
          return;
        }
        let searchParams = {};
        if (this.searchUserId !== '' && this.searchUserId !== null){
          searchParams.user_id = this.searchUserId;
        }

        if (this.searchUserName !== '' && this.searchUserName !== null){
          searchParams.name = this.searchUserName;
        }

        if (this.searchUserEmail !== '' && this.searchUserEmail !== null){
          searchParams.email = this.searchUserEmail;
        }

        // Update searchResultUser and clear searchResultBooks
        axios.get('/api/search-user', {
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
            this.searchResultUser = response.data.result;
          }else {
            this.$notify({
              title: "Search user error",
              text: "Search user with error: " + response.data.error,
              type: "error"
            });
            return;
          }
        }).catch(err=>{
          this.$notify({
              title: "Search user error",
              text: "Search user with error: " + err.response.data.error,
              type: "error"
          });
          return;
        }).finally(()=>{
          //this.searchResultBooks = [];
        })
        
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
            if (!response.data || response.data == undefined || !response.data.success){
              this.$notify({
                title: "Search failed",
                text: "Search failed with unknown error, this can be from network or server",
                type: "error"
              });
            }
            if (response.data.success === true){
                this.searchResultBooks = response.data.result;
            }else{
              this.$notify({
                title: "Search failed",
                text: "Search failed with error: " + response.data.error,
                type: "error"
            });
            }
        }).catch(err=>{
            this.$notify({
                title: "Search book failed",
                text: "Search book failed with error: " + err.response.data.error,
                type: "error"
            })
        }).finally(()=>{
            //this.searchResultUser = [];
        })   
        
      },
      selectUser(id, name, email) {
        this.selectedUserId = id;
        this.selectedUserName = name;
        this.selectedUserEmail = email;
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
        const isDamagedOrLost = this.damagedOrLost === "true" ? true : false;
        const isApproved = this.isApproved === "true" ? true : false;
        const hasResolved = this.hasResolved !== "" && this.hasResolved !== null 
                            && this.hasResolved !== false ? true : false;
        const renewPending = this.renewPending !== "" && this.renewPending !== null 
                            && this.renewPending !== false ? true : false;
        axios.postForm('/api/manage-borrow-admin', {
            book_id: bookID,
            user_id: userID,
            start_borrow: this.convertLocalDatetimeToISOString(this.startBorrow),
            end_borrow: this.convertLocalDatetimeToISOString(this.endBorrow),
            return_date: returnDate,
            damaged_or_lost: isDamagedOrLost,
            is_approved: isApproved,
            has_resolved: hasResolved,
            renew_pending: renewPending
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
            this.selectedUserEmail = '';
            this.selectedUserName = '';
            this.selectedBookId = '';
            this.selectedBookIsbn = '';
            this.selectedBookTitle = '';
            this.startBorrow = '';
            this.endBorrow = '';
        })
      },
      editBorrowChanged(borrow_status){
        this.editedBorrowId = borrow_status.id;
        this.editedUserId = borrow_status.userId;
        this.editedBookId = borrow_status.bookId;

        this.editedStartedBorrow = borrow_status.startBorrow !== '' && borrow_status.startBorrow !== null 
        ? this.convertISODatetimeToLocalInputString(borrow_status.startBorrow) : borrow_status.startBorrow;
        
        this.editedEndBorrow = borrow_status.endBorrow !== '' && borrow_status.endBorrow !== null
        ? this.convertISODatetimeToLocalInputString(borrow_status.endBorrow): borrow_status.endBorrow;

        this.editedReturnDate = borrow_status.returnDate !== '' && borrow_status.returnDate !== null ? 
        this.convertISODatetimeToLocalInputString(borrow_status.returnDate): borrow_status.returnDate;

        this.editedDamagedOrLost = borrow_status.isDamagedOrLost;
        this.editedIsApproved = borrow_status.isApproved;
        this.editedHasResolved = borrow_status.hasResolved;
        this.editedRenewPending = borrow_status.renewPending;
  
        this.activeTab = 'editBorrow';
        this.$refs.editBorrowTab.focus();
      },
      deleteBorrowChanged(borrow_id){
        this.deletedBorrowId = borrow_id;

        this.deleteBorrow(); //There should be a modal to give a warning first before this
        
      },
      editBorrow(){
        axios.putForm('/api/manage-borrow-admin', {
            borrow_id: this.editedBorrowId,
            book_id: this.editedBookId,
            user_id: this.editedUserId,
            start_borrow: this.convertLocalDatetimeToISOString(this.editedStartedBorrow),
            end_borrow: this.convertLocalDatetimeToISOString(this.editedEndBorrow),
            return_date: (this.editedReturnDate === null || this.editedReturnDate === '') ? null :this.convertLocalDatetimeToISOString(this.editedReturnDate),
            damaged_or_lost: (this.editedDamagedOrLost !== null || this.editedDamagedOrLost !== '') ? this.editedDamagedOrLost : false,
            is_approved: (this.editedIsApproved !== null || this.editedIsApproved !== '') ? this.editedIsApproved : false,
            has_resolved: (this.editedHasResolved !== null || this.editedHasResolved !== '') ? this.editedHasResolved : false,
            renew_pending: (this.editedRenewPending !== null || this.editedRenewPending !== '') ? this.editedRenewPending : false,
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
            this.editedHasResolved = null;
            this.editedRenewPending = null;
            this.fetchBorrow(this.currentPage);
        })
        
      },
      deleteBorrow(){
        if (this.deletedBorrowId == null || this.deletedBorrowId == ''){
          this.$notify({
            title: 'No ID selected to delete!',
            text: 'No borrow ID selected to delete!',
            type: 'error'
          });
          return;
        }
  
        axios.delete(
          '/api/manage-borrow-admin/' + this.deletedBorrowId,{
            data: {
              borrow_id: this.deletedBorrowId
            }
          }).then((response)=>{
              const response_data = response.data;
              if (response.success == true) {
                this.$notify({
                  title: 'Borrow deleted successfully!',
                  text: 'Borrow instance with ID ' + this.deletedBorrowId + ' has been deleted successfully',
                  type: 'success'
                });
                
              }
          }).catch((err)=> {

            this.$notify("Borrow deleted with error:" + err.response.data.error);
          }).finally(()=>{
            this.deletedBorrowId = null;
            this.fetchBorrow(this.currentPage);
          });
  
        
      },
      convertDateToUTC(date){
        let utcDate = new Date(date).toISOString();
      }
    },
    watch: {
      currentPage: {
        handler(newCurrentPage){
          this.fetchBorrow(newCurrentPage);
        }
      },
      selectedBookId: {
        handler(newBookId){
          this.fetchBorrow(this.currentPage);
        }
      },
      selectedUserId: {
        handler(newUserId){
          this.fetchBorrow(this.currentPage);
        }
      }
    }
  };
  </script>

  