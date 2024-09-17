<template>
<h3 class="mt-3">Favorite books</h3>
<div class="table-responsive rounded-3 px-3 py-3 mx-3">
    <table class="table table-bordered">
        <thead>
            <tr>
                <th>Image</th>
                <th>Book ID</th>
                <th>Book Title</th>
                <th>Publish year</th>
                <th>ISBN</th>
                <th>Stock</th>
                <th>Actions</th>
            </tr>
        </thead>
    <tbody>
        <tr v-for="book in data" :key="book.id">
            <td><img :src="apiSite + '/image/' + book.id" :alt="'Image for book with title: ' + book.title" style="max-height: 90px;"/></td>
            <td>{{ book.id }}</td>
            <td>{{ book.title }}</td> 
            <td>{{ book.publish_year }}</td>
            <td>{{ book.isbn }}</td>
            <td>{{ book.stock }}</td>
            <td><RouterLink :to="'/book/' + book.id" class="text-decoration-none"><button class="btn btn-outline-primary">Details</button></RouterLink></td>
        </tr>
    </tbody>
    </table>
    <nav aria-label="Book table navigation">
        <ul class="component-pagination">
            <li class="pagination-arrow arrow-left me-1">
                <a href="#" class="page-link" @click="currentPage =  currentPage > 1 ? currentPage - 1 : 1" id="prevPageButton"><i class="bi bi-chevron-left"></i></a>
            </li>
            <li class="page-item">
                <li class="pagination-number current-number" ><input type="number" style="margin: 0 5px; max-width: 50px;" 
                    @input="(e)=> {currentPage = e.target.value}" :value="currentPage" min="1"/></li>
            </li>
            <li class="pagination-arrow arrow-left ms-1">
                <a href="#" class="page-link" @click="currentPage =  currentPage + 1" id="nextPageButton"><i class="bi bi-chevron-right"></i></a>
            </li>
        </ul>
    </nav>
</div>
</template>
<script setup>
import axios from 'axios';
import { watch, ref, onBeforeMount } from 'vue';
const currentPage = ref(1);
const data = ref([]);

const fetchFavoriteBooks = (page) => {
    // Fetch favorite books
    axios.get('/api/favorite', { params: { page: page, limit: 10 } })
        .then(response => {
            if (!response.data || response.data == undefined || !response.data.success) {
                this.$notify({
                    title: "Get favorite books failed!",
                    text: "Get favorite books failed with unknown error, this can be from network or server",
                    type: "error"
                });
            }
            data.value = response.data.data;
        }).catch(error => {
            this.$notify({
                title: "Get favorite books failed!",
                text: "Get favorite books failed with unknown error, this can be from network or server",
                type: "error"
            });
        });
}
watch(currentPage, (newPage, oldPage) => {
    fetchFavoriteBooks(newPage);
}, { immediate: true });
</script>