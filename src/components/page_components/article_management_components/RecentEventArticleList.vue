<template>
    <h4 class="section-title ms-3 bg-light-subtle text-center mt-3 mb-3">Recent Events</h4>
    <div class="py-3 px-3 mb-2 mx-4 rounded bg-dark-blue">
        <label for="eventSearchBar" class="form-label text-white" style="font-weight: 620;">Search Event</label>
        <div class="d-flex">
            <input type="text" class="form-control me-2" placeholder="Search event" v-model="searchQuery" id="eventSearchBar" />
            <button class="btn btn-primary" @click="searchEvent">Search</button>
        </div>
    </div>
    <ul class="component-pagination">
        <li class="pagination-arrow arrow-left me-1">
            <a href="#" class="page-link" @click="currentPage = currentPage > 1 ? currentPage - 1 : 1" id="prevPageButton"><i class="bi bi-chevron-left"></i></a>
        </li>
        <li class="page-item">
            <li class="pagination-number current-number" ><input type="number" style="margin: 0 5px; max-width: 50px;" 
                v-model.number="currentPage" min="1"/></li>
        </li>
        <li class="pagination-arrow arrow-left ms-1">
            <a href="#" class="page-link" @click="currentPage = currentPage < maxPage ? currentPage + 1 : maxPage" id="nextPageButton"><i class="bi bi-chevron-right"></i></a>
        </li>
    </ul>
    <div class="px-4">
        <div v-for="(article, index) in articles" :key="article.id">
            <div class="border-bottom border-secondary" :class="[index === 1 ? 'border-top' : '']">
                <RouterLink :to="'/article/' + String(article.id)" class="text-decoration-none" style="font-family: Georgia, 'Times New Roman', Times, serif;">
                    <h4>{{ article.title }}</h4>
                </RouterLink>
                <p>{{ article.category !== null ? article.category : 'N/A' }}</p>
                <p><i class="bi bi-calendar-week me-1"></i> {{ article.date }}</p>
                <p><i class="bi bi-box-seam-fill me-1"></i> {{ article.note !== null ? article.note : 'N/A' }}</p>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { ref, watch } from 'vue';
import { onBeforeMount } from 'vue';
import { useNotification } from '@kyvg/vue3-notification';
import { useRoute } from 'vue-router';
import axios from 'axios';

const articles = ref([]);
const currentPage = ref(1);
const nofification = useNotification();
const maxPage = 10;
const searchQuery = ref('');
const router = useRoute();

const searchEvent = () => {
    axios.get('/api/search-event', {
        params: {
            query: searchQuery.value,
            page: currentPage.value
        }
    }).then((response) => {
        if (response.status === 200 && response.data && response.data.success === true) {
            articles.value = response.data.result;
        }else {
            nofification.notify({
                title: 'Error',
                text: 'Failed to fetch events with error: ' + response.data.error,
                type: 'error'
            });
        }
    }).catch(err => {
        if (err.response && err.response.data && err.response.data.error) {
            nofification.notify({
                title: 'Error',
                text: 'Failed to fetch events with error: ' + err.response.data.error,
                type: 'error'
            });
        }else {
            nofification.notify({
                title: 'Error',
                text: 'Failed to fetch events with unknown error',
                type: 'error'
            });
        }
    });
}
const getRecentEvents = () => {
    axios.get('/api/recent-events', {
        params: {
            page: currentPage.value
        }
    }).then((response) => {
        if (response.status === 200 && response.data && response.data.success === true) {
            articles.value = response.data.result;
        }else {
            nofification.notify({
                title: 'Error',
                text: 'Failed to fetch events with error: ' + response.data.error,
                type: 'error'
            });
        }
    }).catch(err => {
        if (err.response && err.response.data && err.response.data.error) {
            nofification.notify({
                title: 'Error',
                text: 'Failed to fetch events with error: ' + err.response.data.error,
                type: 'error'
            });
        }else {
            nofification.notify({
                title: 'Error',
                text: 'Failed to fetch events with unknown error',
                type: 'error'
            });
        }
    });
}

watch(currentPage, () => {
    if (searchQuery.value === '') {
        getRecentEvents();
    }else {
        searchEvent();
    }
}, { immediate: true });

onBeforeMount(() => {
    if (router.query.searchQuery) {
        searchQuery.value = String(router.query.searchQuery); searchEvent();
    }
});

</script>