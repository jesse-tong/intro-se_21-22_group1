<template>
    <div class="row">
    <div :class="['col-12', 'col-lg-3']" v-if="$props.bookId !== null">
        <UpdateEbook :bookId="$props.bookId" v-if="$props.bookId !== null" />
        <UpdateImage :bookId="$props.bookId" v-if="$props.bookId !== null"/>
    </div>
    <div :class="['col-12', $props.bookId !== null ? 'col-lg-9' : 'col-12']">
        <h4 v-if="$props.bookId !== null || $props.isEditPage === true" class="mb-2 mt-3 section-title bg-light-subtle">Update book data</h4>
        <h4 v-else class="mb-2 mt-3 section-title bg-light-subtle">Add book</h4>
        <div class="row">
            <div v-if="$props.bookId !== null" class="col-12 col-md-6 col-lg-4">
                <div class="input-group my-2">
                    <label for="editBookId" class="input-group-text" v-if="$props.bookId !== null"><span>Book ID: </span></label>
                    <input type="text" :value="bookId" @input="$emit('update:bookId', $event.target.value)" 
                     v-if="$props.bookId !== null" id="editBookId" disabled class="form-control"/>
                </div>
                
            </div>
            <div class="col-12 col-md-6 col-lg-4">
                <div class="input-group my-2">
                    <label for="editBookISBN" class=" input-group-text"><span>ISBN:</span></label>
                    <input type="text" v-model="bookIsbn" id="editBookISBN" class="form-control"/>
                </div> 
            </div>
            <div class="col-12 col-md-6 col-lg-4">
                <div class="input-group my-2">
                    <label for="editBookStock" class="input-group-text"><span>Book stock in library: </span></label>
                    <input type="number" min="0" max="1000" id="editBookStock" v-model="stock" class="form-control"/>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-12 col-lg-4">
                <div class="input-group my-2">
                    <label for="editPublishYear" class="input-group-text"><span>Publish year:</span></label>
                    <input type="number" v-model.number="publishYear" min="-2000" max="3000" id="editPublishYear" class="form-control"/>
                    <span class="input-group-text">{{ publishYear < 0 ? (Math.abs(publishYear) + ' BC') : (publishYear + ' AD') }}</span>
                </div>
                
            </div>
            <div class="col">
                <div class="input-group me-2 my-2">
                    <label for="editBookTitle" class="input-group-text"><span>Title:</span></label>
                    <input type="text" v-model.number="bookTitle" min="-2000" max="3000" id="editBookTitle" class="form-control"/>
                </div>
                
            </div>
        </div>
        <div class="row">
            <div class="col-md-4 col-12">
                <div class="col border border-2 rounded p-3">
                    <div class="row-6 mt-2">
                        <div class="col-rows-3">
                            <label for="editAuthor" class="form-label"><h5>Add author</h5></label>
                            <input type="text" v-model="inputAuthor" class="form-control" id="editAuthor"/>
                            <div class="row gap-3 ms-2 mt-3">
                                <button class="col-4 btn btn-primary" @click="(e)=>pushAuthorToList(inputAuthor)" id="addAuthorButton">Add author</button>
                                <button class="col-4 btn btn-danger" @click="(e)=>clearEditAuthorList()" id="clearAllAuthorButton">Clear all authors</button>
                                <div class="form-check col-3">
                                    <input class="form-check-input" type="checkbox" v-model="notUpdateAuthors" id="notUpdatingAuthors">
                                    <label for="notUpdatingAuthors" class="form-check-label"><span>Not updating authors</span></label>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row-6 mt-3 ms-1">
                        <span>Authors: </span>
                        <h6 class="badge text-bg-secondary me-1" data-testid="authorBadge" v-for="author in authors">{{ author }}</h6>
                    </div>
                </div>
            </div>
            <div class="col-md-4 col-12">
                <div class="col border border-2 rounded p-3">
                    <div class="row-6 mt-2">
                        <div class="col-rows-3">
                            <label for="editGenre" class="form-label mx-2"><h5>Add genre</h5></label>
                            <input type="text" v-model="inputGenre" class="form-control mx-2" id="editGenre"/>
                            <div class="row gap-3 ms-2 mt-3">
                                <button class="col-4 btn btn-primary" @click="(e)=>pushGenreToList(inputGenre)" id="addGenreButton">Add genre</button>
                                <button class="col-4 btn btn-danger" @click="(e)=>clearEditGenreList()" id="clearAllGenresButton">Clear all genres</button>
                                <div class="form-check col-3">
                                    <input class="form-check-input" type="checkbox" v-model="notUpdateGenres" id="notUpdatingGenres">
                                    <label for="notUpdatingGenres" class="form-check-label"><span>Not updating genres</span></label>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row-6 mt-3 ms-1">
                        <span>Genres: </span>
                        <h6 class="badge text-bg-secondary me-1" data-testid="genreBadge" v-for="genre in genres">{{ genre }}</h6>
                    </div>
                </div>
            </div>
            <div class="col-md-4 col-12">
                <div class="col border border-2 rounded p-3">
                    <div class="row-6 mt-2">
                        <div class="col-rows-3">
                            <label for="editLanguage" class="form-label mx-2"><h5>Add language</h5></label>
                            <input type="text" v-model="inputLanguage" class="form-control mx-2" id="editLanguage"/>
                            <div class="row gap-3 ms-2 mt-3">
                                <button class=" btn btn-primary col-4" @click="(e)=>pushLanguageToList(inputLanguage)" id="addLanguageButton">Add language</button>
                                <button class=" btn btn-danger col-4" @click="(e)=>clearEditLanguageList()" id="clearAllLanguagesButton">Clear all languages</button>
                                <div class="form-check col-3">
                                    <input class="form-check-input" type="checkbox" v-model="notUpdateLanguages" id="notUpdatingLanguages">
                                    <label for="notUpdatingLanguages" class="form-check-label"><span>Not updating languages</span></label>
                                </div>
                            </div>
                        </div>              
                    </div>     
                    <div class="row-6 mt-3 ms-1">
                        <div>
                            <span><h6>Languages: </h6></span>
                            <h6 class="badge text-bg-secondary me-1" data-testid="languageBadge" v-for="language in languages">{{ language }}</h6>
                        </div>     
                    </div>
                </div>
            </div>

        </div>
        <div class="row">
            <div class="col-10">
                <div class="form-floating mt-3">
                    <textarea id="editDescription" v-model="description" placeholder="Book description here" style="height: 200px;" class="form-control" ></textarea>
                    <label for="editDescription" class><span>Book description:</span></label>
                </div>
            </div>
            <div class="col m-auto">
                <button class="btn btn-primary" @click="(e)=>onSubmitAddUpdateBook()">
                    <span v-if="$props.isEditPage === false" id="addBookButton">Add book</span>
                    <span v-else id="editBookButton">Edit book</span>
                </button>
            </div>
        </div>   
    </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import UpdateImage from './UpdateImage.vue';
    import UpdateEbook from './UpdateEbook.vue';
    export default {
        props: {
            bookId: {
                /*If this props has value passed */
                type: Number,
                required: false,
                default: null
            },
            isEditPage: {
                type: Boolean,
                required: false,
                default: false
            }
        },
        data(){
            return {
                inputAuthor: '',
                inputGenre: '',
                inputLanguage: '',

                bookTitle: '',
                bookIsbn: '',
                publishYear: 2024,
                description: '',
                authors: [],
                genres: [],
                languages: [],
                stock: 0,

                notUpdateAuthors: false,
                notUpdateGenres: false,
                notUpdateLanguages: false,
            }
            
        },
        created(){
            this.fetchInitialEditData(this.$props.bookId)
        },
        methods: {
            fetchInitialEditData(bookId){
                if (bookId !== null){
                    axios.get('/api/book/' + bookId).then(response => {
                        if (!response.data){
                            this.$notify({
                                title: "Cannot fetch initial book data",
                                text: "Cannot fetch initial fetch data, no response. This may be from your network, server or frontend",
                                type: "error"
                            });
                            return;
                        }
                        if (response.data.success === true){
                            let bookDataForId = response.data.result;
                            this.bookTitle = bookDataForId.title;
                            this.bookIsbn = bookDataForId.isbn;
                            this.stock = bookDataForId.stock;
                            this.publishYear = bookDataForId.publish_year;
                            this.description = bookDataForId.description;
                            this.authors = bookDataForId.authors;
                            this.genres = bookDataForId.genres;
                            this.languages = bookDataForId.languages;
                            
                        }else {
                            this.$notify({
                                title: "Cannot fetch initial fetch data",
                                text: "Cannot fetch initial fetch data, with error: " + response.data.error,
                                type: "error"
                            });
                            return;
                        }

                    }).catch(err=>{
                        this.$notify({
                                title: "Cannot fetch initial fetch data",
                                text: "Cannot fetch initial fetch data, with error: " + err.response.data.error,
                                type: "error"
                            });
                        return;
                    });
                }
            },
            onSubmitAddUpdateBook(){
                var bookUpdateObject = {}
                if (this.bookId !== null){
                    bookUpdateObject.book_id = this.bookId;
                }
                if (this.notUpdateAuthors === false){
                    bookUpdateObject.authors = this.authors;
                }
                if (this.notUpdateGenres === false){
                    bookUpdateObject.genres = this.genres;
                }
                if (this.notUpdateLanguages === false){
                    bookUpdateObject.languages = this.languages;
                }
                if (this.bookTitle === ''){
                    this.$notify({
                        title: "Empty title",
                        text: "Empty book title, please check again",
                        type: "warn"
                    });
                    return;
                }else {
                    bookUpdateObject.title = this.bookTitle;
                }
                bookUpdateObject.isbn = this.bookIsbn;
                bookUpdateObject.publish_year = this.publishYear;
                bookUpdateObject.description = this.description;
                bookUpdateObject.stock = this.stock !== null && this.stock !== '' && this.stock !== 0 ? this.stock : 0;

                //Use axios to send request here
                if (this.$props.bookId === null || this.$props.isEditPage === false){
                    //Add new book
                    axios.postForm('/api/book', bookUpdateObject)
                        .then(response => {
                            if (response.status !== 200 || !response.data || response.data.success === undefined ){
                                this.$notify({
                                    title: "Unknown error or network error",
                                    text: "Unknown error from server or network error, please check your network connection",
                                    type: "error"
                                });
                            }
                            if (response.data.success === true ){
                                this.$notify({
                                    title: "Add book successfully!",
                                    text: "Add book successfully!",
                                    type: "success"
                                })
                            }else {
                                this.$notify({
                                    title: "Add book failed!",
                                    text: "Add book failed with error: " + response.data.error,
                                    type: "error"
                                })
                            }
                        }).catch(err => {
                            this.$notify({
                                title: "Error adding new book",
                                text: "Add book failed with error" + err.response.data.error,
                                type: "error"
                            })
                        }).finally(()=>{
                            this.bookTitle = ''; this.bookIsbn = ''; this.publishYear = '';
                            this.genres = []; this.authors =[]; this.languages = [];
                            this.$emit('addUpdateBookCallback')
                        })
                }else {
                    //Update book with id bookId
                    axios.putForm('/api/book', bookUpdateObject)
                        .then(response => {
                            if (response.status !== 200 || !response.data || response.data.success === undefined ){
                                this.$notify({
                                    title: "Unknown error or network error",
                                    text: "Unknown error from server or network error, please check your network connection",
                                    type: "error"
                                });
                            }
                            if (response.data.success === true ){
                                this.$notify({
                                    title: "Edit book details successfully!",
                                    text: "Edit book successfully!",
                                    type: "success"
                                })
                            }else {
                                this.$notify({
                                    title: "Edit book details failed!",
                                    text: "Edit book failed with error: " + response.data.error,
                                    type: "error"
                                })
                            }
                        }).catch(err => {
                            this.$notify({
                                title: "Error editing book details",
                                text: "Editing book data failed with error" + err.response.data.error,
                                type: "error"
                            })
                        }).finally(()=>{
                            this.bookTitle = ''; this.bookIsbn = ''; this.publishYear = '';
                            this.genres = []; this.authors =[]; this.languages = [];
                            this.description = ''; this.stock = null;
                            
                            this.$emit('addUpdateBookCallback');
                        })
                }
            },
            pushAuthorToList(author){
                this.authors.push(author);
            },
            clearEditAuthorList(){
                this.authors = [];
            },
            pushGenreToList(genre){
                this.genres.push(genre);
            },
            clearEditGenreList(){
                this.genres = [];
            },
            pushLanguageToList(language){
                this.languages.push(language);
            },
            clearEditLanguageList(){
                this.languages = [];
            }
        },
        emits: ['update:bookId', 'addUpdateBookCallback'],
        components: {
            UpdateImage: UpdateImage,
            UpdateEbook: UpdateEbook
        }
    }
</script>