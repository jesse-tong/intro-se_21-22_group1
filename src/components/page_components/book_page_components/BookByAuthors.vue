<template>
    <div class="row mt-3 ms-2">
        <div class="col-12 col-md-4 col-lg-3 rounded g-0"  >
            <h5 class="ms-3 ms-md-3 ms-lg-3">Authors:</h5>
            <div class="">
                <ul class="list-group mt-2 rounded">
                    <li class="list-group-item" :class="{ active: isTabActive(author.id) }" v-for="author in authors" @click="selectedId = parseInt(author.id)"><span>{{ author.name }}</span></li>
                </ul>
                <nav aria-label="Author list navigation">
                    <ul class="pagination input-group">
                        <li class="page-item">
                            <a href="#prevPageButton" class="page-link" @click="authorPage =  authorPage > 1 ? authorPage - 1 : 1" id="prevPageButton"><span>Previous page</span></a>
                        </li>
                        <li class="page-item">
                            <input @input="(e)=> {authorPage = e.target.value}" type="number" min="1"  class="page-link" style="max-width: 75px" :value="authorPage">
                        </li>
                        <li class="page-item">
                            <a href="#nextPageButton" class="page-link" @click="authorPage =  authorPage + 1" id="nextPageButton"><span >Next page</span></a>
                        </li>
                    </ul>
                </nav>
            </div>
            
        </div>
        <div class="bg-light col-12 col-md-8 col-lg-9 my-2 rounded shadow-sm"  v-if="selectedId === null"></div>
        <div class="col-12 col-md-8 col-lg-9 my-2 pe-3" v-else>
            <div class="bg-light rounded shadow-sm p-1 border-1" >
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
                selectedId: 0
            }
        },
        
        methods: {
            getAuthors(page){
                axios.get('/api/get-authors', {
                    params: {
                        page: page,
                        limit: 15
                    }
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
            }
        },
        components: {
            GetBookByAuthorOrGenreId: GetBookByAuthorOrGenreId
        }
    }
</script>