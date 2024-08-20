<template>
    <div class="row mt-3">
        <div class="col-12 col-md-4 col-lg-3 g-0 rounded"  >
            <h5 class="ms-3 ms-md-3 ms-lg-3">Genres:</h5>
            <ul class="list-group mt-2 border-0 list-group-flush">
                <ul class="author-list mt-2">
                    <li class="list-item" :class="{ active: isTabActive(genre.id) }"  v-for="genre in genres" @click="selectedId = parseInt(genre.id)"><span>{{ genre.name }}</span></li>
                </ul>
            </ul>
            <nav aria-label="Genre list navigation">
                <ul class="component-pagination">
                    <li class="pagination-arrow arrow-left me-1">
                        <a href="#" class="page-link" @click="genrePage =  genrePage > 1 ? genrePage - 1 : 1" id="prevPageButton"><i class="bi bi-chevron-left"></i></a>
                    </li>
                    <li class="page-item">
                        <li class="pagination-number current-number" ><input type="number" style="margin: 0 5px; max-width: 50px;" 
                            @input="(e)=> {genrePage = e.target.value}" :value="genrePage" min="1"/></li>
                    </li>
                    <li class="pagination-arrow arrow-left ms-1">
                        <a href="#" class="page-link" @click="genrePage =  genrePage + 1" id="nextPageButton"><i class="bi bi-chevron-right"></i></a>
                    </li>
                </ul>
                
            </nav>
        </div>
        <div class=" col-12 col-md-8 col-lg-9"  v-if="selectedId === null"></div>
        <div class="col-12 col-md-8 col-lg-9 my-2 pe-3" v-else>
            <div class=" rounded p-1 border-0">
                <GetBookByAuthorOrGenreId :genreOrAuthorId="selectedId" :fetchGenre=true />
            </div>
        </div>
        
        
    </div>
</template>
<script>
    import axios from 'axios';
import GetBookByAuthorOrGenreId from './GetBookByAuthorOrGenreId.vue';
    export default {
        data(){
            return {
                genres: [],
                genrePage: 1,
                selectedId: 0
            }
        },
        watch: {
            genrePage: {
                handler(newPage, oldPage){
                    this.getGenres(newPage);
                },
                immediate: true
            }
        },
        methods: {
            getGenres(page){
                axios.get('/api/get-genres', {
                    params: {
                        page: page,
                        limit: 15
                    }
                }).then(response=> {
                    if (!response.data || response.data == undefined || !response.data.success){
                        this.$notify({
                            title: "Get book by genres failed!",
                            text: "Get books by genres failed with unknown error, this can be from network or server",
                            type: "error"
                        });
                    }
                    if (response.data.success === true){
                        this.genres = response.data.result;
                    }else{
                        this.$notify({
                            title: "Get book by genres failed!",
                            text: "Get book by genres failed with error: " + response.data.error,
                            type: "error"
                        });
                    }   
                }).catch(err=>{
                    this.$notify({
                        title: "Get book by genres failed!",
                        text: "Get book by genres failed failed with error: " + err.response.data.error,
                        type: "error"
                    })
                }).finally(()=>{
                    
                }); 
            },
            isTabActive(tabId){
                if (this.selectedId === tabId){
                    return true;
                }else {
                    return false;
                }
            }
        },
        components: {
            GetBookByAuthorOrGenreId: GetBookByAuthorOrGenreId
        }
    }
</script>