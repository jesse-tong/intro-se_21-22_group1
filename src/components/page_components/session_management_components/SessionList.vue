<template>
    <div class="container mt-3">
        <div class="d-flex justify-content-between mb-2">
            <h4 class="section-title bg-light-subtle text-primary px-3">Session List</h4>
            <RouterLink class="btn btn-primary" to="/admin/library-place"><< Return</RouterLink>
        </div>
        <hr />
        <div class="shadow-sm mt-3 px-3 py-3">
            <div class="row">

                <div class="col-12 col-md-6 col-lg-4 col-xxl-3 pe-2 pb-2" v-for="session in sessions">
                    <div class="card">
                        <div class="card-header text-center" v-if="session.user !== undefined && session.user!== null">
                            <p class="card-title" >{{ session.user.name + ' (' + session.user.email + ')' + ' - ID: ' + session.userId }}</p>
                        </div>
                        <div class="card-body">
                            <div class="col">
                            <div class="row-9">
                                <p class="card-text" v-for="book in session.books">{{ book.title + ' - ' + book.id}}</p>
                                
                            </div>
                            <div class="row-3 border-top pt-2 mt-2">
                                <div class="d-flex justify-content-between">
                                <p class="card-text"><i class="bi bi-calendar2-date me-2"></i>{{ new Date(session.startDate).toString() }}</p>
                                <p class="card-text"><i class="bi bi-person-add me-2"></i>In use: {{ session.inUse }}</p>
                                </div>
                            </div>
                            </div>
                        </div>
                        <div class="card-footer">
                            <div class="row row-cols-2">
                            <div class="col text-center">
                                <RouterLink :to="'/admin/library-place/session/' + session.id" class="text-decoration-none"><p>Session details</p></RouterLink>
                            </div>
                            <div class="col text-center">
                                <a href="#" @click="endSession(session.id)" class="text-decoration-none" v-if="session.inUse === true"><p>End session</p></a>
                                <a href="#" @click="markInUse(session.id)" class="text-decoration-none" v-else="session.inUse === true"><p>Mark in use</p></a>
                            </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
            <div v-if="sessions.length === 0" class="text-center mt-3">
                <p>No sessions found</p>
            </div>
        </div>
    </div>
</template>
<script setup>
    import { ref, defineProps, onBeforeMount } from 'vue';
    import axios from 'axios';
    import { useNotification } from '@kyvg/vue3-notification';

    const sessions = ref([]);
    const props = defineProps({
        placeId: {
            type: [Number, null],
            required: false,
            default: null,
        },
    });
    onBeforeMount(() => {
        getSessionList();
        document.title = 'Session List';
    });
    const notify = useNotification();
    const markInUse = (sessionId) => {
        axios.post('/library/session/' + sessionId + '/in-use').then((response) => {
            if (response.data && response.data.success && response.data.success == true){
                notify.notify({
                    type: 'success',
                    title: 'Success',
                    text: 'Session marked in use',
                });
            }else{
                notify.notify({
                    type: 'error',
                    title: 'Error',
                    text: 'Failed to mark session in use with error: ' + response.data.error,
                });
            }
        }).catch(err => {
            if (err.response && err.response.data && err.response.data.error){
                notify.notify({
                    type: 'error',
                    title: 'Error',
                    text: 'Failed to mark session in use with error: ' + err.response.data.error,
                });
                return;
            }else {
                notify.notify({
                    type: 'error',
                    title: 'Error',
                    text: 'Failed to mark session in use with unknown error',
                });
            }
        }).finally(() => {
            getSessionList();
        });
    }
    const endSession = (sessionId) => {
        axios.post('/library/session/' + sessionId + '/end').then((response) => {
            if (response.data && response.data.success && response.data.success == true){
                notify.notify({
                    type: 'success',
                    title: 'Success',
                    text: 'Session ended successfully',
                });
            }else{
                notify.notify({
                    type: 'error',
                    title: 'Error',
                    text: 'Failed to end session with error: ' + response.data.error,
                });
            }
        }).catch(err => {
            if (err.response && err.response.data && err.response.data.error){
                notify.notify({
                    type: 'error',
                    title: 'Error',
                    text: 'Failed to end session with error: ' + err.response.data.error,
                });
                return;
            }else {
                notify.notify({
                    type: 'error',
                    title: 'Error',
                    text: 'Failed to end session with unknown error',
                });
            }
        }).finally(() => {
            getSessionList();
        });
    }

    const getSessionList = () => {
        axios.get('/library' + (props.placeId !== null ? '/place/' + props.placeId : '') + '/session').then((response) => {
            if (response.data && response.data.success && response.data.success == true){
                sessions.value = response.data.result;
            }
        });
    };
</script>