<template>

<div class="container mt-3">
    <div class="d-flex justify-content-between mb-2">
        <h4 class="section-title bg-light-subtle text-primary px-3">Session Details</h4>
        <div>
            <button class="btn btn-primary mb-2" @click="editing = !editing">{{ editing ? 'Edit': 'Cancel edit'}}</button>
            <RouterLink class="btn btn-primary ms-2 mb-2" :to="'/admin/library-place/' + session.place.id" v-if="session && session.place"><< Return</RouterLink>
        </div>
        
    </div>
    <hr />
    <div class="shadow-sm mt-3 px-3 py-3">
        <div class="" v-if="session !== null && editing === false">
            <div class="row">
                <div class="col-12 col-md-3 mb-2 mb-lg-0">
                    <div class="input-group">
                        <span class="input-group-text">Session ID: </span>
                        <input type="text" class="form-control" :value="session.id" readonly>
                    </div>
                </div>
                <div class="col-12 col-md-3 mb-2 mb-lg-0">
                    <div class="input-group">
                        <span class="input-group-text">In use: </span>
                        <input type="text" class="form-control" :value="session.inUse ? 'Yes' : 'No'" readonly>
                    </div>
                </div>
                <div class="col">
                    <div class="input-group">
                        <span class="input-group-text">Session start date: </span>
                        <input type="text" class="form-control" :value="session.startDate" readonly>
                    </div>
                </div>
            </div>
            <div class="input-group my-2">
                <span class="input-group-text">Place ID: </span>
                <input type="text" class="form-control" :value="session.place.id" readonly>
                <span class="input-group-text">Room: </span>
                <input type="text" class="form-control" :value="session.place.room" readonly>
            </div>
            <div class="row mb-3">
                <div class="col-12 col-lg-3 mb-2 mb-lg-0">
                    <div class="input-group">
                        <span class="input-group-text">User ID: </span>
                        <input type="text" class="form-control" :value="session.user.id" readonly>
                    </div>
                </div>
                <div class="col-12 col-lg-5 mb-2 mb-lg-0">
                    <div class="input-group">
                        <span class="input-group-text">Username: </span>
                        <input type="text" class="form-control" :value="session.user.name" readonly>
                    </div>
                </div>
                <div class="col">
                    <div class="input-group">
                        <span class="input-group-text">Email: </span>
                        <input type="text" class="form-control" :value="session.user.email" readonly>
                    </div>
                </div>
            </div>
            
            <div class="d-flex justify-content-between mb-2 mt-3 align-items-center" v-for="book in session.books" v-if="session !== null">
                <p>{{book.id }} {{ book.title }} - {{ book.isbn }}</p>
                <button class="btn btn-primary mt-2 mb-3" @click="deleteBookFromSession(book.id)">Remove book from session</button>
            </div>
        </div>
        <div class="" v-if="editing === true && session !== null">
            <h5>Change session place</h5>
            <div class="form-group">
                <label for="userId">Session user ID</label>
                <input type="number" class="form-control" id="userId" v-model="sessionUserId">
            </div>
            <div class="form-group">
                <label for="placeId">Session place ID</label>
                <input type="number" class="form-control" id="placeId" v-model="sessionPlaceId">
            </div>
            <div class="form-group mb-2">
                <label for="startDate">Session start date</label>
                <input type="datetime-local" class="form-control" id="startDate" v-model="sessionStartDate">
            </div>
            <button class="btn btn-primary" @click="updateSession">Update session</button>
            <h5>Search user</h5>
            <SearchUser @search-user="onSearchUserButtonClicked" v-model:searchUserId="searchUserId" v-model:searchUserEmail="searchUserEmail" v-model:searchUserName="searchUserName"/>
            <div class="table-responsive-lg mt-3 rounded">
                <table class="table " v-if="searchResultUser">
                    <thead>
                        <tr>
                            <th scope="col">ID</th>
                            <th scope="col">Name</th>
                            <th scope="col">Email</th>
                            <th scope="col">Action</th>
                        </tr>
                    </thead>
                    <tbody >
                        <tr v-for="user in searchResultUser" v-if="session !== null" >
                            <th class="bg-light-subtle">{{user.id }}</th> 
                            <td class="bg-light-subtle">{{ user.name }}</td>
                            <td class="bg-light-subtle">{{ user.email }}</td>
                            <td class="bg-light-subtle"><button class="btn btn-primary" @click="changeSessionUser(user.id)">Change session user</button></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <div v-if="editing === true && session !== null">
            <h5>Add book to session</h5>
            <SearchBook @search-book="onSearchBookButtonClicked" v-model:searchBookTitle="searchBookTitle" 
            v-model:searchBookId="searchBookId" v-model:searchBookIsbn="searchBookIsbn"/>
            <div class="table-responsive-lg mt-3">
                <table class="table" v-if="bookSearchResult">
                    <thead>
                        <tr>
                            <th scope="col">ID</th>
                            <th scope="col">Title</th>
                            <th scope="col">ISBN</th>
                            <th scope="col">Action</th>
                        </tr>
                    </thead>
                    <tbody >
                        <tr v-for="book in bookSearchResult" v-if="session !== null" >
                            <th class="bg-light-subtle">{{book.id }}</th> 
                            <td class="bg-light-subtle">{{ book.title }}</td>
                            <td class="bg-light-subtle">{{ book.isbn }}</td>
                            <td class="bg-light-subtle"><button class="btn btn-primary" @click="addBookToSession(book.id)">Add book to session</button></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        
    </div>
</div>

</template>
<script setup>
import axios from 'axios';
import { ref, onBeforeMount, defineProps, watch} from 'vue';
import SearchUser from '@page_components/borrow_management_components/SearchUser.vue';
import SearchBook from '@page_components/borrow_management_components/SearchBook.vue';
import { useNotification } from '@kyvg/vue3-notification';

const editing = ref(false);

const notify = useNotification();
const session = ref(null);
const bookSearchResult = ref([]);
const searchResultUser = ref([]);

const searchBookTitle = ref('');
const searchBookIsbn = ref('');
const searchBookId = ref(null);

const searchUserId = ref(null);
const searchUserEmail = ref('');
const searchUserName = ref('');

const sessionUserId = ref(null);
const sessionPlaceId = ref(null);
const sessionStartDate = ref(null);

const props = defineProps({
    sessionId: {
        type: [Number, null],
        required: true,
        default: null,
    },
});

onBeforeMount(() => {
    getSessionDetails();
});
const changeSessionUser = (userId) => {
    sessionUserId.value = userId;
}
const getSessionDetails = () => {
    axios.get('/library/session/' + props.sessionId).then((response) => {
        if (response.data && response.data.success && response.data.success == true){
            session.value = response.data.result;
            sessionUserId.value = response.data.result.userId;
            sessionPlaceId.value = response.data.result.placeId;
            sessionStartDate.value = convertISODatetimeToLocalInputString(response.data.result.startDate);
        }else{
            notify.notify({
                type: 'error',
                title: 'Error',
                text: 'Failed to get session details with error: ' + response.data.error,
            });
        }
    }).catch(err => {
        if (err.response && err.response.data && err.response.data.error){
            notify.notify({
                type: 'error',
                title: 'Error',
                text: 'Failed to get session details with error: ' + err.response.data.error,
            });
            return;
        }else {
            notify.notify({
                type: 'error',
                title: 'Error',
                text: 'Failed to get session details with unknown error',
            });
        }
    });
}
const addBookToSession = (bookId) => {
    axios.post('/library/session/' + session.value.id + '/book/' + bookId).then((response) => {
        if (response.data && response.data.success && response.data.success == true){
            notify.notify({
                type: 'success',
                title: 'Success',
                text: 'Book added to session',
            });
        }else{
            notify.notify({
                type: 'error',
                title: 'Error',
                text: 'Failed to add book to session with error: ' + response.data.error,
            });
        }
    }).catch(err => {
        if (err.response && err.response.data && err.response.data.error){
            notify.notify({
                type: 'error',
                title: 'Error',
                text: 'Failed to add book to session with error: ' + err.response.data.error,
            });
            return;
        }else {
            notify.notify({
                type: 'error',
                title: 'Error',
                text: 'Failed to add book to session with unknown error',
            });
        }
    }).finally(() => {
        getSessionDetails();
    });
}
const deleteBookFromSession = (bookId) => {
    axios.delete('/library/session/' + session.value.id + '/book/' + bookId).then((response) => {
        if (response.data && response.data.success && response.data.success == true){
            notify.notify({
                type: 'success',
                title: 'Success',
                text: 'Book removed from session',
            });
        }else{
            notify.notify({
                type: 'error',
                title: 'Error',
                text: 'Failed to remove book from session with error: ' + response.data.error,
            });
        }
    }).catch(err => {
        if (err.response && err.response.data && err.response.data.error){
            notify.notify({
                type: 'error',
                title: 'Error',
                text: 'Failed to remove book from session with error: ' + err.response.data.error,
            });
            return;
        }else {
            notify.notify({
                type: 'error',
                title: 'Error',
                text: 'Failed to remove book from session with unknown error',
            });
        }
    }).finally(() => {
        getSessionDetails();
    });
}
const searchUser = (searchUserId, searchUserEmail, searchUserName) => {
        // Implement API call to search user with email and username
        if ((searchUserId === '' || searchUserId === null) 
        && (searchUserEmail === '' || searchUserEmail === null)
        && (searchUserName === '' || searchUserName === null)) {
          notify.notify({
            title: "No search query",
            text: "No user ID, email or name to search for",
            type: "warn"
          })
          return;
        }
        let searchParams = {};
        if (searchUserId !== '' && searchUserId !== null){
          searchParams.user_id = searchUserId;
        }

        if (searchUserName !== '' && searchUserName !== null){
          searchParams.name = searchUserName;
        }

        if (searchUserEmail !== '' && searchUserEmail !== null){
          searchParams.email = searchUserEmail;
        }

        // Update searchResultUser and clear searchResultBooks
        axios.get('/api/search-user', {
          params: searchParams
        }).then(response => {
          if (!response.data || !response.data.success){
            notify.notify({
              title: "Unknown error",
              text: "Unknown error, this can be server or network error.",
              type: "error"
            });
            return;
          }
          if (response.data.success === true){
            searchResultUser.value = response.data.result;
          }else {
            notify.notify({
              title: "Search user error",
              text: "Search user with error: " + response.data.error,
              type: "error"
            });
            return;
          }
        }).catch(err=>{
          notify.notify({
              title: "Search user error",
              text: "Search user with error: " + err.response.data.error,
              type: "error"
          });
          return;
        });
        
}
const convertLocalDatetimeToISOString = (localDatetimeString)=>{
    //Since the value of <input type="datetime-local" /> is always YYYY-mm-ddThh:ss
    //and does not denotes any timezone, so parse it with new Date() and use toISOString() method will not work correctly
    let timeWithTimezone = new Date(localDatetimeString);
    return timeWithTimezone.toISOString();
}
const convertISODatetimeToLocalInputString = (localDatetimeString)=>{
    //Since input="local-datetime" only accept YYYY-mm-ddThh:ss, not YYYY-mm-ddThh:ssZ of ISO string
    let currentLocalDate = new Date();
    let localTimeOffset = currentLocalDate.getTimezoneOffset() * 60 * 1000; //Get local timezone offset to GMT by milliseconds

    let gmtTime = new Date(localDatetimeString); 
    let localTime = gmtTime - localTimeOffset; localTime = new Date(localTime);
    let localISOString = localTime.toISOString();

    return localISOString.slice(0, -1); //Remove the last character of local string in ISO format
}

const searchBook = (searchBookTitle, searchBookIsbn, searchBookId, currentPage)=>{
            
    let searchParams = {};
    if (searchBookTitle !== '' && searchBookTitle !== null){
        searchParams.title = searchBookTitle;
    }
    if (searchBookIsbn !== '' && searchBookIsbn !== null){
        searchParams.isbn = searchBookIsbn;
    }

    if (searchBookId !== null && searchBookId > 0){
        searchParams.book_id = searchBookId;
    }
    
    searchParams.page = currentPage; searchParams.limit = 10;

    axios.get('/api/book', {
        params: searchParams
    }).then(response => {
        if (!response.data){
            notify.notify({
                title: "Cannot fetch search results",
                text: "Cannot fetch search results, no response. This may be from your network, server or frontend",
                type: "error"
            });
            return;
        }
        if (response.data.success === true){
            bookSearchResult.value = response.data.result;
        }else {
            notify.notify({
                title: "Cannot fetch search result",
                text: "Cannot fetch search result, with error: " + response.data.error,
                type: "error"
            });
            return;
        }
    }).catch(err => {
        notify.notify({
            title: "Cannot fetch search result",
            text: "Cannot fetch search result, with error: " + err.response.data.error,
            type: "error"
        });
    })
}
const updateSession = () => {
    axios.putForm('/library/session/' + session.value.id, 
        {
            userId: sessionUserId.value,
            placeId: sessionPlaceId.value,
            startDate: convertLocalDatetimeToISOString(sessionStartDate.value),
        }
    ).then((response) => {
        if (response.data && response.data.success && response.data.success == true){
            notify.notify({
                type: 'success',
                title: 'Success',
                text: 'Session edited successfully',
            });
        }else{
            notify.notify({
                type: 'error',
                title: 'Error',
                text: 'Failed to edit session with error: ' + response.data.error,
            });
        }
    }).catch(err => {
        if (err.response && err.response.data && err.response.data.error){
            notify.notify({
                type: 'error',
                title: 'Error',
                text: 'Fail to edit session with error: ' + err.response.data.error,
            });
            return;
        }else {
            notify.notify({
                type: 'error',
                title: 'Error',
                text: 'Failed to edit session with unknown error',
            });
        }
    }).finally(() => {
        getSessionDetails();
    });
}

const onSearchBookButtonClicked = () => {
    searchBook(searchBookTitle.value, searchBookIsbn.value, searchBookId.value, 1);
}
const onSearchUserButtonClicked = () => {
    searchUser(searchUserId.value, searchUserEmail.value, searchUserName.value);
}
</script>