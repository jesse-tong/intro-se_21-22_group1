<template>
    <div class="row mt-3 ms-2">
        <div class="col-12 col-md-3 col-lg-3 g-0 pe-3 pe-md-0 pe-lg-2">
            <div class="card mb-3">
                <div class="card-header">
                    Advanced Search
                </div>
                <div class="card-body">
                    <div id="search-form">
                        <div class="mb-3">
                            <label for="title" class="form-label">Title</label>
                            <input type="text" class="form-control" id="title" placeholder="Enter Title" v-model="searchTitle"
                        </div>
                        <div class="mb-3">
                            <label for="description" class="form-label">Description</label>
                            <textarea class="form-control" id="description" rows="3" placeholder="Enter Description" v-model="searchDescription"></textarea>
                        </div>
                        <div class="mb-3">
                            <label for="id" class="form-label">ID</label>
                            <input type="number" class="form-control" id="id" placeholder="Enter ID" v-model.number="searchId" min="0">
                        </div>
                        <div class="mb-3">
                            <label for="isbn" class="form-label">ISBN</label>
                            <input type="text" class="form-control" id="isbn"  placeholder="Enter ISBN" v-model="searchIsbn">
                        </div>
                        <div class="mb-3">
                            <label for="authors" class="form-label">Authors</label>
                            <input type="text" class="form-control" id="authors" placeholder="Enter Authors (comma separated)" v-model="searchAuthors">
                        </div>
                        <div class="mb-3">
                            <label for="genres" class="form-label">Genres</label>
                            <input type="text" class="form-control" id="genres" placeholder="Enter Genres (comma separated)" v-model="searchGenres">
                        </div>
                        <button class="btn btn-primary" @click="submitSearch" id="searchButton">Search</button>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-12 col-md-9 col-lg-9 my-2 pe-3">
            <div class=" rounded shadow-sm p-1 border-1 table-responsive" >
                <table class="table table-bordered ">
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
                        <tr v-for="book in searchResults" :key="book.id" data-testid="searchResultRow">
                            <td><img :src="apiSite + '/image/' + book.id" :alt="'Image for book with title: ' + book.title" style="max-height: 90px;"/></td>
                            <td>{{ book.id }}</td>
                            <td>{{ book.title }}</td> 
                            <td>{{ book.publish_year }}</td>
                            <td>{{ book.isbn }}</td>
                            <td>{{ book.stock }}</td>
                            <td><button class="btn btn-primary"><RouterLink :to="'/book/' + book.id" class="text-white">Details</RouterLink></button></td>
                        </tr>
                        <tr v-if="searchResults === null || searchResults === undefined ||searchResults.length === 0">
                            <td colspan="7" class=""><span class="m-auto"><i>No search result found</i></span></td>
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
        </div>
    </div>
    
</template>
<script>
import axios from 'axios';
import { mapStores } from 'pinia';
import { useSearchQueryStore } from '../../stores/SearchQueryStore';

    export default {
        data(){
            return {
                searchTitle:  '',
                searchId: '',
                searchIsbn: '',
                searchDescription: '',
                searchAuthors: '',
                searchGenres: '',
                currentPage: 1,
                limitPerPage: 10,


                searchResults: []
            }
        },
        methods: {
            fetchSearchResult(){
                let searchParams = {}
                //This will split the authors by commas and remove all empty items when split
                let authors = this.searchAuthors.split(/,\s?/).filter(item => item);
                if (authors.length !== 0){
                    searchParams.authors = authors;
                }
                let genres = this.searchGenres.split(/,\s?/).filter(item => item);
                if (genres.length !== 0){
                    searchParams.genres = genres;
                }
                if (this.searchTitle !== '' && this.searchTitle !== null){
                    searchParams.title = this.searchTitle;
                }
                if (this.searchId !== null && this.searchId !== '' && this.searchId > 0){
                    searchParams.book_id = this.searchId;
                }
                if (this.searchIsbn !== null && this.searchIsbn !== ''){
                    searchParams.isbn = this.searchIsbn;
                }
                if (this.searchDescription !== null && this.searchDescription !== ''){
                    searchParams.description = this.searchDescription;
                }
                searchParams.page = this.currentPage; searchParams.limit = this.limitPerPage;

                axios.get('/api/advanced-search', {
                    params: searchParams
                }).then(response=> {
                    if (!response.data || response.data == undefined || !response.data.success){
                        this.$notify({
                            title: "Search failed",
                            text: "Search failed with unknown error, this can be from network or server",
                            type: "error"
                        });
                    }
                    if (response.data.success === true){
                        this.searchResults = response.data.result;
                        /* this.$notify({
                            title: "Search successfully",
                            text: "Search successfully!",
                            type: "success"
                        }); */
                    }else{
                        this.$notify({
                            title: "Search failed",
                            text: "Search books failed with error: " + response.data.error,
                            type: "error"
                        });
                    }   
                }).catch(err=>{
                    this.$notify({
                        title: "Search book failed",
                        text: "Search book failed with error: " + err.status,
                        type: "error"
                    })
                }).finally(()=>{
                    
                })   
            },
            submitSearch(){
                this.fetchSearchResult();
            },
            
        },
        watch: {
            currentPage(newPage, oldPage){
                this.fetchSearchResult();
            }
        },
        computed: {
            ...mapStores(useSearchQueryStore)
        },
        created() {
            this.searchTitle = this.searchQueryStore.title;
            this.searchIsbn = this.searchQueryStore.isbn;
            this.searchDescription = this.searchQueryStore.description;
 
            this.searchQueryStore.clearQueries(); //clear search query

            if ((this.searchTitle !== '' && this.searchTitle !== null) 
            || (this.searchId !== null && this.searchId !== '' && this.searchId > 0) 
            || (this.searchIsbn !== null && this.searchIsbn !== '') ){
                //If one of title, id, isbn or description is not empty because of query parameters, fetch without user input
                this.fetchSearchResult(); 
            }
        }
    }
</script>