<template>
    <div class="row mt-3 ms-2">
        <div class="col-12 col-md-4 col-lg-3 rounded g-0"  >
            <h5 class="section-title bg-light-subtle text-start text-primary ms-3 ms-md-3 ms-lg-3 px-3">Book by authors</h5>
            <div class="ps-1 shadow-sm rounded-2">
                <div class="mb-2 px-3">
                    <input type="text" class="form-control" v-model="authorSearchQuery" placeholder="Search author" />
                </div>
                <ul class="author-list mt-2 pe-2" style="padding-left: 1rem;">
                    <li class="list-item" :class="{ active: isTabActive(author.id) }" v-for="author in authors" @click="selectedId = parseInt(author.id)"><span>{{ author.name }}</span></li>
                </ul>
                <nav aria-label="Author list navigation">
                    <ul class="component-pagination">
                        <li class="pagination-arrow arrow-left me-1">
                            <a href="#prevPageButton" class="page-link" @click="authorPage =  authorPage > 1 ? authorPage - 1 : 1" id="prevPageButton"><i class="bi bi-chevron-left"></i></a>
                        </li>
                        <li class="page-item">
                            <li class="pagination-number current-number" ><input type="number" style="margin: 0 5px; max-width: 50px;" 
                                @input="(e)=> {authorPage = e.target.value}" :value="authorPage" min="1"/></li>
                        </li>
                        <li class="pagination-arrow arrow-left ms-1">
                            <a href="#nextPageButton" class="page-link" @click="authorPage =  authorPage + 1" id="nextPageButton"><i class="bi bi-chevron-right"></i></a>
                        </li>
                    </ul>
                </nav>
            </div>
            
        </div>
        <div class=" col-12 col-md-8 col-lg-9 my-2 rounded shadow-sm"  v-if="selectedId === null"></div>
        <div class="col-12 col-md-8 col-lg-9 my-2 pe-3" v-else>
            <div class=" rounded p-1 border-0" >
                <GetBookByAuthorOrGenreId :genreOrAuthorId="selectedId" :fetchGenre=false />
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
                authors: [],
                authorPage: 1,
                selectedId: 0,
                authorSearchQuery: ''
            }
        },
        
        methods: {
            getAuthors(page){
                let params = {
                    page: page,
                    limit: 15
                }
                if (this.authorSearchQuery !== ''){
                    params.name = this.authorSearchQuery;
                }
                axios.get('/api/get-authors', {
                    params: params
                }).then(response=> {
                    if (!response.data || response.data == undefined || !response.data.success){
                        this.$notify({
                            title: "Get book by authors failed!",
                            text: "Get books by authors failed with unknown error, this can be from network or server",
                            type: "error"
                        });
                    }
                    if (response.data.success === true){
                        this.authors = response.data.result;
                    }else{
                        this.$notify({
                            title: "Get book by authors failed!",
                            text: "Get book by authors failed with error: " + response.data.error,
                            type: "error"
                        });
                    }   
                }).catch(err=>{
                    this.$notify({
                        title: "Get book by authors failed!",
                        text: "Get book by authors failed failed with error: " + err.response.data.error,
                        type: "error"
                    })
                }).finally(()=>{
                    
                })   
            },
            isTabActive(tabId){
                if (this.selectedId === tabId){
                    return true;
                }else {
                    return false;
                }
            }
        },
        watch: {
            authorPage: {
                handler(newPage, oldPage){
                    this.getAuthors(newPage);
                },
                immediate: true
            },
            authorSearchQuery: {
                handler(newQuery, oldQuery){
                    this.getAuthors(this.authorPage);
                },
                immediate: false
            }
        },
        components: {
            GetBookByAuthorOrGenreId: GetBookByAuthorOrGenreId
        },
        created(){
            document.title = "Books by Authors";
        }
    }
</script>