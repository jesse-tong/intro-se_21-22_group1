<template>
    <Modal :title="'Create Session'" ref="createSessionModal" id="createSessionModal">
        <template #body>
            <h5>Search User</h5>
            <SearchUser v-model:searchUserId="searchUserId" v-model:searchUserName="searchUserName" v-model:searchUserEmail="searchUserEmail" 
            @search-user="searchUser" class="mb-2"/>
            <div class="d-flex justify-content-between mb-2 align-items-center" v-for="user in searchResultUser">
                <p>{{user.id }} {{ user.name }} - {{ user.email }}</p>
                <button class="btn btn-primary" @click="selectedUserId = user.id">Select</button>
            </div>
            <h5>Create session</h5>
            <div class="form-group">
                <label for="sessionName">Session Place ID</label>
                <input type="text" class="form-control" id="sessionName" v-model="selectedPlace" />
            </div>
            
            <div class="form-group">
                <label for="sessionDescription">Session User ID</label>
                <input type="number" class="form-control" id="sessionDescription" v-model="selectedUserId" />
            </div>
            <div class="form-group">
                <label for="sessionStartTime">Session Start Time</label>
                <input type="datetime-local" class="form-control" id="sessionStartTime" v-model="sessionStartTime" />
            </div>
            
        </template>
        <template #footer>
            <button type="button" class="btn btn-primary" @click="createSession">Create Session</button>
        </template>
    </Modal>
    <Modal :title="'Delete place'" ref="deleteModal" id="deleteModal">
        <template #body>
            <p>Are you sure you want to delete place with ID {{ deletePlaceId }}?</p>
        </template>
        <template #footer>
            <button type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="onModalDeleteButtonClicked">Delete</button>
        </template>
    </Modal>
    <Modal :title="'Create place'" ref="createPlaceModal" id="createPlaceModal">
        <template #body>
            <div class="form-group">
                <label for="placeRoom">Place room</label>
                <input type="text" class="form-control" id="placeRoom" v-model="placeRoom" />
            </div>
            <div class="form-check form-switch">
                <input type="checkbox" class="form-check-input" id="placeHaveComputer" v-model="haveComputer" value="true"/>
                <label for="placeHaveComputer" class="form-check-label">Place have computer</label>
            </div>
        </template>
        <template #footer>
            <button type="button" class="btn btn-primary" @click="createPlace">Create Place</button>
        </template>
    </Modal>
    <div class="container">
        <div class="d-flex justify-content-between mb-2 mt-3">
            <h4 class="section-title bg-light-subtle text-primary px-3">Library Place List</h4>
            <div>
                <button class="btn btn-primary me-3" @click="getPlaceList">Refresh</button>
                <button class="btn btn-outline-primary" @click="onCreatePlaceButtonClicked">Create Place</button>
            </div>
        </div>
        <hr />
        <div class="shadow-sm mt-3 px-3 py-3">
            <div class="row">
                <div class="col-12 col-md-6 col-lg-4 col-xxl-3 pb-3" v-for="libraryPlace in libraryPlaces">
                    <div class="card">
                        <div class="card-header text-center">
                            <h6 class="card-title"></h6>
                        </div>
                        <div class="card-body">
                            <div class="col">
                            <div class="row-9">
                                <div class="d-flex m-auto rounded-3 bg-warning text-center justify-content-center" 
                                style="width: 55px; height: 55px; color: white; align-items: center; text-decoration: none;">
                                <h4><b>{{ libraryPlace.id }}</b></h4>
                                </div>
                            </div>
                            <div class="row-3 border-top pt-2 mt-2">
                                <div class="d-flex justify-content-between">
                                <p class="card-text"><i class="bi bi-laptop me-2" alt="Location has computer: "></i>{{ libraryPlace.haveComputer ? 'Yes' : 'No' }}</p>
                                <p class="card-text"><i class="bi bi-geo-alt-fill me-2" alt="Room: "></i>{{ libraryPlace.room }}</p>
                                </div>
                            </div>
                            </div>
                        </div>
                        <div class="card-footer">
                            <div class="row row-cols-2">
                            <div class="col text-center">
                                <div class="dropdown">
                                    <a class="dropdown-toggle text-decoration-none" href="#" role="link" data-bs-toggle="dropdown" aria-expanded="false">
                                        Actions
                                    </a>

                                    <ul class="dropdown-menu">
                                        <li><a class="dropdown-item" href="#" @click="deleteModalButtonSelected(libraryPlace.id)">Delete place</a></li>
                                        <li><a class="dropdown-item" href="#" @click="createSessionButtonSelected(libraryPlace.id)">Create session here</a></li>
                                        <li><RouterLink class="dropdown-item" :to="'/admin/library-place/' + libraryPlace.id + '/session'">Sessions</RouterLink></li>
                                    </ul>
                                </div>
                            </div>
                            <div class="col text-center">
                                <a href="#" class="text-decoration-none" v-if="!libraryPlace.isInUse"><p>Vacant</p></a>
                                <a href="#" class="text-decoration-none" v-else><p>Is in use</p></a>
                            </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
    import { ref, defineProps, onBeforeMount } from 'vue';
    import Modal from '../../common/Modal.vue';
    import SearchUser from '../borrow_management_components/SearchUser.vue';
    import axios from 'axios';
    import { useNotification } from '@kyvg/vue3-notification';
    const libraryPlaces = ref([]);
    const selectedPlace = ref(null);
    const selectedUserId = ref(null);

    const searchUserId = ref(null);
    const searchUserName = ref(null);
    const searchUserEmail = ref(null);
    const notify = useNotification();
    const searchResultUser = ref([]);

    const createSessionModal = ref(null);
    const deleteModal = ref(null);
    const createPlaceModal = ref(null);

    const deletePlaceId = ref(null);

    const placeRoom = ref(null);
    const haveComputer = ref(false);



    onBeforeMount(() => {
        getPlaceList();
        document.title = 'Library Place List';
    });
    const getPlaceList = () => {
        axios.get('/library/place').then((response) => {
            if (response.data && response.data.success && response.data.success == true){
                libraryPlaces.value = response.data.result;
            }
        });
    };
    const onCreatePlaceButtonClicked = () => {
        createPlaceModal.value.show();
    };
    const onModalDeleteButtonClicked = () => {
        deletePlace(deletePlaceId.value);
        deletePlaceId.value = null;
    };
    const deleteModalButtonSelected = (placeId) => {
        deletePlaceId.value = placeId;
        deleteModal.value.show();
    };
    const createSessionButtonSelected = (placeId) => {
        selectedPlace.value = placeId;
        createSessionModal.value.show();
    };
    const createPlace = () => {
        if (placeRoom.value === null || placeRoom.value === ''){
            notify.notify({
                type: 'warn',
                title: 'Missing data',
                text: 'Please enter a room name to create a place',
            });
            return;
        }
        axios.postForm('/library/place', {
            room: placeRoom.value,
            haveComputer: haveComputer.value,
        }).then((response) => {
            if (response.data && response.data.success && response.data.success == true){
                notify.notify({
                    type: 'success',
                    title: 'Success',
                    text: 'Place created',
                });
            }else{
                notify.notify({
                    type: 'error',
                    title: 'Error',
                    text: 'Failed to create place with error: ' + response.data.error,
                });
            }
        }).catch(err => {
            if (err.response && err.response.data && err.response.data.error){
                notify.notify({
                    type: 'error',
                    title: 'Error',
                    text: 'Failed to create place with error: ' + err.response.data.error,
                });
                return;
            }else {
                notify.notify({
                    type: 'error',
                    title: 'Error',
                    text: 'Failed to create place with unknown error',
                });
            }
        }).finally(() => {
            getPlaceList();
        });
    }
    const createSession = () => {
        if (selectedPlace.value === null || selectedUserId.value === null){
            notify.notify({
                type: 'warn',
                title: 'Missing data',
                text: 'Please select a place and user to create a session',
            });
            return;
        }
        axios.postForm('/library/session', {
            placeId: selectedPlace.value,
            userId: selectedUserId.value,
            startDate: sessionStartTime.value,
        }).then((response) => {
            if (response.data && response.data.success && response.data.success == true){
                notify.notify({
                    type: 'success',
                    title: 'Success',
                    text: 'Session created',
                });
                
            }else{
                notify.notify({
                    type: 'error',
                    title: 'Error',
                    text: 'Failed to create session with error: ' + response.data.error,
                });
            }
        }).catch(err => {
            if (err.response && err.response.data && err.response.data.error){
                notify.notify({
                    type: 'error',
                    title: 'Error',
                    text: 'Failed to create session with error: ' + err.response.data.error,
                });
                return;
            }else {
                notify.notify({
                    type: 'error',
                    title: 'Error',
                    text: 'Failed to create session with unknown error',
                });
            }
        }).finally(() => {
            selectedPlace.value = null; selectedUserId.value = null; searchResultUser.value = [];
            getPlaceList();
        });
    };
    const searchUser = () => {
        // Implement API call to search user with email and username
        if ((searchUserId.value === '' || searchUserId.value === null) 
        && (searchUserEmail.value === '' || searchUserEmail.value === null)
        && (searchUserName.value === '' || searchUserName.value === null)) {
          notify.notify({
            title: "No search query",
            text: "No user ID, email or name to search for",
            type: "warn"
          })
          return;
        }
        let searchParams = {};
        if (searchUserId.value !== '' && searchUserId.value !== null){
          searchParams.user_id = searchUserId.value;
        }

        if (searchUserName.value !== '' && searchUserName.value !== null){
          searchParams.name = searchUserName.value;
        }

        if (searchUserEmail.value !== '' && searchUserEmail.value !== null){
          searchParams.email = searchUserEmail.value;
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
    const deletePlace = (placeId)=>{
        axios.delete('/library/place/' + placeId).then((response) => {
            if (response.data && response.data.success && response.data.success == true){
                notify.notify({
                    type: 'success',
                    title: 'Success',
                    text: 'Place deleted successfully',
                });
            }else{
                notify.notify({
                    type: 'error',
                    title: 'Error',
                    text: 'Failed to delete place with error: ' + response.data.error,
                });
            }
        }).catch(err => {
            if (err.response && err.response.data && err.response.data.error){
                notify.notify({
                    type: 'error',
                    title: 'Error',
                    text: 'Failed to delete place with error: ' + err.response.data.error,
                });
                return;
            }else {
                notify.notify({
                    type: 'error',
                    title: 'Error',
                    text: 'Failed to delete place with unknown error',
                });
            }
        }).finally(() => {
            getPlaceList();
        });
    }
</script>