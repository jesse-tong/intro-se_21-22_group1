<template>
    <div class="row mt-3">
        <div class="col-3 g-0 rounded"  >
            <ul class="list-group mt-2 rounded">
                <li class="list-group-item" :class="{ active: isTabActive(genre.id) }" v-for="genre in genres" @click="selectedId = parseInt(genre.id)"><span>{{ genre.name }}</span></li>
            </ul>
        </div>
        <div class="bg-light col-9"  v-if="selectedId === null"></div>
        <div class="col-9 my-2 pe-3" v-else>
            <div class="bg-light rounded shadow-sm p-1 border-1">
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
                authorPage: 1,
                selectedId: 0
            }
        },
        created() {
            axios.get('/api/get-genres', {
                params: {
                    page: this.authorPage,
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
                
            })   
        },
        methods: {
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