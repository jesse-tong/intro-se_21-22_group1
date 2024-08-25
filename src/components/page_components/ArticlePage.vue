<template>
    <section class="wrapper bg-soft-primary">
        <div class="container pt-8 pt-md-10 pb-18 pb-md-20 text-center">
            <div class="row">
                <div class="col-md-10 col-xl-8 mx-auto"> 
                    <div class="post-header">
                        <div class="post-category text-line">
                            <RouterLink to="/articles" class="hover" rel="category">
                                <h6 class="section-title text-center text-primary px-2 mt-2">Return to Article List</h6>
                            </RouterLink>
                        </div>
                    <h1 class="display-6 mb-3 post-title article-title"><b>{{ title }}</b></h1>
                    <ul class="post-meta" style="list-style-type: none;">
                        <li class="post-date" ><i class="bi bi-calendar3 me-3"></i><span>{{ date }}</span></li>
                        <li class="post-category" v-if="category !== null && category !== undefined"><i class="bi bi-folder2 me-3"></i><span>Category: {{ category }}</span></li>
                        <li class="post-note" v-if="note !== null && note !== undefined"><i class="bi bi-box-seam-fill me-3"></i><span>{{ note }}</span></li>
                    </ul>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <section class="wrapper bg-light-primary">

        <div class="container pb-14 pb-md-16">
            <div class="row">
                <div class="col-lg-10 mx-auto">
                    <div class="blog single mt-n17 mt-lg-n18">
                        <div class="card">
                            <div class="card-body px-4 px-md-6 py-4">
                                <article class="post-content article-text-align mb-5" v-html="parsedContent">
                                    
                                </article>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </section>
</template>

<script>
    import axios from 'axios';
    import { marked } from 'marked';
import { RouterLink } from 'vue-router';
    export default {
        data(){
            return {
                title: 'N/A',
                content: 'N/A',
                date: 'N/A',
                category: 'N/A',
                note: 'N/A',
                parsedContent: ''
            }
        },
        props: {
            articleId: {
                type: String,
                required: true
            }
        },
        created(){
            this.fetchArticle(this.$props.articleId);
        },
        methods: {
            fetchArticle(articleId){
                axios.get('/api/article/' + articleId)
                .then(response => {
                    if (response.data !== undefined && response.data.success === true){
                        if (response.data.result === null){
                            //Server return no article content, redirect to 404 page
                            this.$router.push({name: 'not-found-inner'});
                        }
                        this.content = response.data.result.content;
                        this.title = response.data.result.title;
                        this.date = response.data.result.date;
                        this.category = response.data.result.category;
                        this.note = response.data.result.note;
                        this.parsedContent = marked.parse(this.content);
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
        }
    }
</script>
