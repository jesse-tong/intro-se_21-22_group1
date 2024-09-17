<template>
    <div class="mx-2">
        <div class="text-center w-100 mt-4">
            <h4 class="section-title bg-light-subtle text-center text-primary px-3">Articles from Library</h4>
        </div>
        <ArticleList :articles="articles" @update:currentPage="(page) => { currentPage = page }" :currentPage="currentPage" :actionVisible="false"/>
    </div>
</template>
<script>
    import axios from 'axios';
    import ArticleList from '@page_components/article_management_components/ArticleList.vue';
    export default {
        data(){
            return {
                articles: [],
                currentPage: 1,
            }
        },
        watch: {
            currentPage: {
                handler(newCurrentPage){
                    this.fetchArticles(newCurrentPage);
                },
                immediate: true
            }
        },
        components: {
            ArticleList
        },
        methods: {
            fetchArticles(page){
                axios.get('/api/article', {params: { page: page, limit: 10} })
                .then(response => {
                    if (response.data !== undefined && response.data.success === true){
                        this.articles = response.data.result;
                    }else if (response.data.success === false){
                        this.$notify({
                            title: 'Fetching article at page ' + page + ' failed',
                            text: 'Fetching article at page ' + page + ' failed with error: ' + response.data.error,
                            type: 'error'
                        });
                    }
                }).catch(err => {
                    if (err.response){
                        if (err.response.data && err.response.data.error){
                            this.$notify({
                                title: 'Fetching article at page ' + page + ' failed',
                                text: 'Fetching article at page ' + page + ' failed with error: ' + err.response.data.error,
                                type: 'error'
                            });
                        }else {
                            this.$notify({
                                title: 'Fetching articles at page ' + page + ' failed',
                                text: 'Fetching articles failed with unknown error',
                                type: 'error'
                            });
                        }
                    }
                })
            }
        },
        created(){
            document.title = "EasyLib - Articles";
        }
    }
</script>