<template>
    <div class="table-responsive">
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
<script>
    import axios from 'axios';
    export default {
        props: {
            genreOrAuthorId: {
                type: Number,
                required: true
            },
            fetchGenre: {
                type: Boolean,
                required: true
            }
        },
        data(){
            return {
                currentPage: 1,
                data: [],
            }
        },
        methods: {
            fetchData(id, fetchGenreInsteadOfAuthor){
                const subPath = fetchGenreInsteadOfAuthor ? 'genre' : 'author'
                axios.get('/api/' + subPath + '/' + this.$props.genreOrAuthorId + '/books', {
                    params: {
                        page: this.currentPage,
                        limit: 10
                    }
                }).then(response=> {
                    if (!response.data || response.data == undefined || !response.data.success){
                        this.$notify({
                            title: "Search failed",
                            text: "Search failed with unknown error, this can be from network or server",
                            type: "error"
                        });
                    }
                    if (response.data.success === true){
                        this.data = response.data.result;
                    }else{
                        this.$notify({
                            title: "Search failed",
                            text: "Search book by " + subPath + " failed with error: " + response.data.error,
                            type: "error"
                        });
                    }   
                }).catch(err=>{
                    this.$notify({
                        title: "Search book failed",
                        text: "Search book by " + subPath + " failed with error: " + err.response.data.error,
                        type: "error"
                    })
                }).finally(()=>{
                    
                })   
            }
        },
        watch: {
            currentPage: {
                handler(newPage, oldPage){
                    this.fetchData(this.$props.genreOrAuthorId, this.$props.fetchGenre);
                },
                immediate: true
            },
            genreOrAuthorId:{
                handler(newId, oldId){
                    this.fetchData(newId, this.$props.fetchGenre);
                }
            },
            fetchGenre: {
                handler(fetchBooksByGenreOrAuthor){
                    this.fetchData(this.$props.genreOrAuthorId, fetchBooksByGenreOrAuthor);
                }
            }
        }
    }
</script>