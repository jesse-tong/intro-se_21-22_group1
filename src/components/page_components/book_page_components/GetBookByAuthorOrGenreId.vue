<template>
    <table class="table table-striped">
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
          <td><button class="btn btn-primary"><RouterLink :to="'/book/' + book.id" class="text-white">Details</RouterLink></button></td>
        </tr>
      </tbody>
    </table>
    <nav aria-label="Book table navigation">
        <ul class="pagination">
            <li class="page-item">
                <a href="#prevPageButton" class="page-link" @click="currentPage =  currentPage > 1 ? currentPage - 1 : 1" id="prevPageButton"><span>Previous page</span></a>
            </li>
            <li class="page-item">
                <input @input="(e)=> {currentPage = e.target.value}" type="number" min="1"  class="page-link" style="max-width: 95px" :value="currentPage">
            </li>
            <li class="page-item">
                <a href="#nextPageButton" class="page-link" @click="currentPage =  currentPage + 1" id="nextPageButton"><span >Next page</span></a>
            </li>
        </ul>
    </nav>
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
                apiSite: 'http://localhost:5000'
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
                    console.log('Current page changed!')
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