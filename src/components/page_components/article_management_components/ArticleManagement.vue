<template>
    
    <div class="mx-2">
        <div class="text-center w-100 mt-4">
            <h4 class="section-title bg-light-subtle text-center text-primary px-3">Library Article Management</h4>
        </div>
        <ArticleList :articles="articles" @update:currentPage="(page) => { currentPage = page }" :currentPage="currentPage" @deleteArticle="onDeleteArticle" @editArticle="onEditArticle" />
        <div class="mt-2 mb-2">
            <hr class="hr" />
            <h5 class="section-title bg-light-subtle text-primary pe-3 mt-2 mb-2">Create/Edit New Article</h5>
            <div class="d-flex flex-column justify-content-between">
                
                <div class="">
                    <label for="articleTitle" class="form-label ms-1"><span>Title: </span></label>
                    <input type="text" v-model="articleTitle" class="form-control" id="articleTitle"/>
                </div>
                <div class="mt-2">
                    <label for="articleContent" class="form-label ms-1"><span>Content: </span></label>
                    <MdEditor v-model="articleContent" :language="'en-US'" :codeTheme="'a11y'" id="articleContent" @onSave="onSaveArticle" :noMermaid="true" :noKatex="true"/>
                    <div class="d-flex justify-content-between w-100 mt-2">
                        <button class="btn btn-success" v-if="selectedArticleId === null" @click="(e) => onCreateNewArticle()">Save new article</button>
                        <button class="btn btn-success" v-else @click="(e)=>onSaveEditArticle(selectedArticleId)">Save article</button>
                        <div class="ms-3 ms-md-0">
                            <span v-if="selectedArticleId === null" class="me-md-2">New article</span>
                            <span v-else class="me-md-2">{{ 'Editing article: ' + selectedArticleId }}</span>
                            <button class="btn btn-outline-success" @click="(e) => onNewArticleDrafted()"><span>Create new article</span></button>
                        </div>
                    </div>        
                </div>
            </div>
        </div>
        <hr class="hr" />
        <h5 class="section-title bg-light-subtle text-primary pe-3 ms-1">Upload Image</h5>
        <ImageUpload @select-image="onImageSelected" class="card pt-2 pb-2"/>
    </div>
    
</template>
<script>
    import axios from 'axios';
    import ArticleList from './ArticleList.vue';
    import ImageUpload from '../image_upload_components/ImageUpload.vue';
    import { MdEditor } from 'md-editor-v3';
    import 'md-editor-v3/lib/style.css';
    

    export default {
        data(){
            return {
                selectedArticleId: null,
                articles: [],
                currentPage: 1,

                articleTitle: '',
                articleContent: ''
            }
        },
        components: {
            ArticleList: ArticleList,
            MdEditor: MdEditor,
            ImageUpload: ImageUpload
        },
        watch: {
            currentPage: {
                handler(newCurrentPage){
                    this.fetchArticles(newCurrentPage);
                },
                immediate: true
            },
            selectedArticleId: {
                handler(newSelectedId){
                    if (newSelectedId !== null && newSelectedId !== undefined){
                        this.fetchArticle(newSelectedId);
                    }else {
                        this.articleTitle = '';
                        this.articleContent = '';
                    }
                },
                immediate: true
            }
        },
        methods: {
            onSaveArticle(md, html){
                /*if (this.selectedArticleId === null){
                    this.onCreateNewArticle();
                }else {
                    this.onSaveEditArticle(this.selectedArticleId);
                }*/
            },
            onImageSelected(url){
                this.articleContent += url;
            },
            onNewArticleDrafted(){
                this.selectedArticleId = null;
            },
            onEditArticle(articleId){
                this.selectedArticleId = articleId;
            },
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
            },
            fetchArticle(articleId){
                axios.get('/api/article/' + articleId)
                .then(response => {
                    if (response.data !== undefined && response.data.success === true){
                        this.articleContent = response.data.result.content;
                        this.articleTitle = response.data.result.title;
                    }else if (response.data.success === false){
                        this.$notify({
                            title: 'Fetching article with ID ' + articleId + ' failed',
                            text: 'Fetching article with ID ' + articleId + ' failed with error: ' + response.data.error,
                            type: 'error'
                        });
                    }
                }).catch(err => {
                    if (err.response){
                        if (err.response.data && err.response.data.error){
                            this.$notify({
                                title: 'Fetching article with ID ' + articleId + ' failed',
                                text: 'Fetching article with ID ' + articleId + ' failed with error: ' + err.response.data.error,
                                type: 'error'
                            });
                        }else {
                            this.$notify({
                                title: 'Fetching article with ID ' + articleId + ' failed',
                                text: 'Fetching article with ID ' + articleId + ' failed with unknown error',
                                type: 'error'
                            });
                        }
                    }
                })
            },
            onCreateNewArticle(){
                axios.postForm('/api/article', { title: this.articleTitle, content: this.articleContent})
                .then(response => {
                    if (response.data !== undefined && response.data.success === true){
                        this.$notify({
                            title: 'Creating article successfully!' ,
                            text: 'Creating article with ID' + response.data.response.id + 'successfully!',
                            type: 'success'
                        });
                    }else if (response.data.success === false){
                        this.$notify({
                            title: 'Creating new article failed',
                            text: 'Error creating new article: ' + response.data.error,
                            type: 'error'
                        });
                    }
                }).catch(err => {
                    if (err.response){
                        if (err.response.data && err.response.data.error){
                            this.$notify({
                                title: 'Creating new article failed',
                                text: 'Error creating new article: ' + err.response.data.error,
                                type: 'error'
                            });
                        }else {
                            this.$notify({
                                title: 'Creating new article failed',
                                text: 'Creating new article failed with unknown error',
                                type: 'error'
                            });
                        }
                    }
                }).finally(() => { 
                    this.fetchArticles(this.currentPage); 
                    this.selectedArticleId = null; 
                    this.articleContent = ''; this.articleTitle = '';
                });
            },
            onDeleteArticle(articleId){
                axios.delete('/api/article/' + articleId)
                .then(response => {
                    if (response.data !== undefined && response.data.success === true){
                        this.$notify({
                            title: 'Deleting article with ID ' + articleId + ' successfully!' ,
                            text: 'Deleting article with ID ' + articleId + ' successfully!',
                            type: 'success'
                        });
                    }else if (response.data.success === false){
                        this.$notify({
                            title: 'Error saving article with ID ' + articleId + ' failed',
                            text: 'Error saving article: ' + response.data.error,
                            type: 'error'
                        });
                    }
                }).catch(err => {
                    if (err.response){
                        if (err.response.data && err.response.data.error){
                            this.$notify({
                                title: 'Deleting article with ID ' + articleId + ' failed',
                                text: 'Error deleting article: ' + err.response.data.error,
                                type: 'error'
                            });
                        }else {
                            this.$notify({
                                title: 'Deleting article with ID ' + articleId + ' failed',
                                text: 'Error deleting article failed with unknown error',
                                type: 'error'
                            });
                        }
                    }
                }).finally(() => { 
                    this.fetchArticles(this.currentPage);
                    this.selectedArticleId = null; 
                    this.articleContent = ''; this.articleTitle = '';
                });
            },
            onSaveEditArticle(articleId){
                
                axios.putForm('/api/article/' + articleId, { title: this.articleTitle, content: this.articleContent})
                .then(response => {
                    if (response.data !== undefined && response.data.success === true){
                        this.$notify({
                            title: 'Saving article successfully!' ,
                            text: 'Saving article with ID ' + articleId + ' successfully!',
                            type: 'success'
                        });
                    }else if (response.data.success === false){
                        this.$notify({
                            title: 'Error saving article with ID ' + articleId + ' failed',
                            text: 'Error saving article: ' + response.data.error,
                            type: 'error'
                        });
                    }
                }).catch(err => {
                    if (err.response){
                        if (err.response.data && err.response.data.error){
                            this.$notify({
                                title: 'Error saving article with ID ' + articleId + ' failed',
                                text: 'Error saving article: ' + err.response.data.error,
                                type: 'error'
                            });
                        }else {
                            this.$notify({
                                title: 'Error saving article with ID ' + articleId + ' failed',
                                text: 'Error saving article failed with unknown error',
                                type: 'error'
                            });
                        }
                    }
                }).finally(() => { 
                    this.fetchArticles(this.currentPage);
                    this.selectedArticleId = null; 
                    this.articleContent = ''; this.articleTitle = '';
                 });
            }
        }
    }
</script>