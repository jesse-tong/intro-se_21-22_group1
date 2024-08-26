<template>
    <h4 class="section-title ms-3 bg-light-subtle text-center mt-3 mb-3">Search on website</h4>
    <div class="py-3 px-3 mb-2 mx-4 rounded bg-dark-blue">
        <label for="eventSearchBar" class="form-label text-white" style="font-weight: 620;">Search Website</label>
        <div class="d-flex">
            <input type="text" class="form-control me-2" placeholder="Enter search query here..." v-model="searchQuery" id="eventSearchBar" />
            <button class="btn btn-primary" @click="getSearchResults">Search</button>
        </div>
    </div>
    <div class="row">
    <div class="ps-4 col-12 col-xl-6 pe-3">
        <h4 class="section-title ms-3 bg-light-subtle text-center mt-3 mb-2" v-if="books.length > 0">Books</h4>
        <div v-for="(book, index) in books" :key="book.id">
            <div class="border-bottom border-secondary" :class="[index === 1 ? 'border-top' : '']">
                <div class="row">
                    <div class="col-12 col-md-4 col-lg-3 col-xl-3">
                        <div class="pe-2 py-2">
                            <img :src="'/image/' + book.id" class="img-fluid" alt="Book cover" style="max-height: 120px; max-width: 120px;"/>
                        </div>
                    </div>
                    <div class="col-12 col-md-8 col-lg-9 col-xl-9">
                        <RouterLink :to="'/book/' + String(book.id)" class="text-decoration-none" style="font-family: Georgia, 'Times New Roman', Times, serif;">
                            <h4>{{ book.title }}</h4>
                        </RouterLink>
                        <p>{{ book.isbn }}</p>
                        <p><i class="bi bi-calendar-week me-1"></i> {{ book.publish_year }}</p>
                        <p><i class="bi bi-box-seam-fill me-1"></i> {{ book.stock }}</p>
                    </div>
                </div>
                
            </div>
        </div>
    </div>
    <div class="pe-4 col-12 col-xl-6 ps-3">
        <h4 class="section-title ms-3 bg-light-subtle text-center mt-3 mb-2" v-if="articles.length > 0">Articles</h4>
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
        <h4 class="section-title ms-3 bg-light-subtle text-center mt-3 mb-2" v-if="events.length > 0">Events</h4>
        <div v-for="(event, index) in events" :key="events.id">
            <div class="border-bottom border-secondary" :class="[index === 1 ? 'border-top' : '']">
                <RouterLink :to="'/article/' + String(event.id)" class="text-decoration-none" style="font-family: Georgia, 'Times New Roman', Times, serif;">
                    <h4>{{ event.title }}</h4>
                </RouterLink>
                <p><i class="bi bi-calendar-week me-1"></i> {{ event.date }}</p>
                <p><i class="bi bi-box-seam-fill me-1"></i> {{ event.note !== null ? event.note : 'N/A' }}</p>
            </div>
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

const articles = ref<any>([]);
const events = ref<any>([]);
const books = ref<any>([]);
const nofification = useNotification();
const searchQuery = ref('');
const router = useRoute();


const getSearchResults = () => {
    axios.get('/api/search-everything', {
        params: {
            query: searchQuery.value,
        }
    }).then((response) => {
        if (response.status === 200 && response.data && response.data.success === true) {
            articles.value = response.data.result.articles;
            books.value = response.data.result.books;
            events.value = response.data.result.events;
        }else {
            nofification.notify({
                title: 'Error',
                text: 'Failed to fetch search results with error: ' + response.data.error,
                type: 'error'
            });
        }
    }).catch(err => {
        if (err.response && err.response.data && err.response.data.error) {
            nofification.notify({
                title: 'Error',
                text: 'Failed to fetch search results with error: ' + err.response.data.error,
                type: 'error'
            });
        }else {
            nofification.notify({
                title: 'Error',
                text: 'Failed to fetch search results with unknown error',
                type: 'error'
            });
        }
    });
}


onBeforeMount(() => {
    if (router.query.searchQuery) {
        searchQuery.value = String(router.query.searchQuery); getSearchResults();
    }
});

</script>