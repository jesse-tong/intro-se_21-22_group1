<template>
<div class="col">
    <div class="row-5">
        <div class="library-homepage-container">
            <img :src="LibraryImage" style="width: 100%; max-height: 300px;" alt="Library image"/>
            <h1 style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;" class="library-homepage-image-text text-white display-1">Welcome to library</h1>
        </div>
        <h3 class="mt-3 ms-3 mb-3">Highest rating books</h3>
        <BookCarousel :books="highestRatingBooks" :apiSite="apiSite" :carouselId="'highestRatingBooks'" />
        <h3 class="mt-4 ms-3 mb-3">Most borrowed books</h3>
        <BookCarousel :books="mostBorrowedBooks" :apiSite="apiSite" :carouselId="'mostBorrowedBooks'"/>
    </div>
    <div class="row">
        <hr class="hr" />
    </div>
    <div class="row-5">
        <div class="row">
            <div class="col-12 col-md-5 col-lg-4">
                <div class="ps-4">
                    <table class="table ps-2 table-bordered">
                        <thead>
                            <tr>
                                <th class="table-active text-center" colspan="2">LIBRARY STATISTICS</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><span>Number of books:</span></td>
                                <td><span>{{ bookCount }}</span></td>
                            </tr>
                            <tr>
                                <td><span>Number of borrows:</span></td>
                                <td><span>{{ borrowCount }}</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                
            </div>
            <div class="col-12 col-md-2 col-lg-4">
                
            </div>
            <div class="col-12 col-md-5 col-lg-4">
                <table class="table table-bordered">
                    <thead>
                        <tr>
                            <th class="table-active text-center" colspan="2">LIBRARY TIMINGS</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><span>Monday-Saturday:</span></td>
                            <td><span>9:00 AM - 9:00 PM</span></td>
                        </tr>
                        <tr>
                            <td><span>Sunday:</span></td>
                            <td><span>10:00 AM - 8:00 PM</span></td>
                        </tr>
                        <tr>
                            <td colspan="2"><span>Library will remain closed during public holidays</span></td>
                        </tr>
                        <tr>
                            <th colspan="2" class="text-center"><span>CONTACT US:</span></th>
                        </tr>
                        <tr>
                            <td colspan="2">
                                <span style="white-space: pre-wrap;">
                                    {{ 'Address: ' + contactAddress +'\n'
                                    +  'Email: ' + contactEmail + '\n' 
                                    +  'Phone number: ' + contactPhoneNumber + '\n' }}
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

        </div>
    </div>
    <div class="row">
        <hr class="hr" />
    </div>
</div>
</template>
<script>
    import axios from 'axios';
    import BookCarousel from '../page_components/homepage_components/BookCarousel.vue';
    import LibraryImage from '../../assets/library.jpg'
    export default {
        data(){
            return {
                bookCount: 'N/A',
                borrowCount: 'N/A',
                highestRatingBooks: [],
                mostBorrowedBooks: [],
                contactEmail: 'N/A',
                contactAddress: 'N/A',
                contactPhoneNumber: 'N/A',
                LibraryImage
            }
        },
        created(){
            this.getHighestRatingBooks();
            this.getMostBorrowedBooks();
            this.getBookCount(); this.getBorrowCount();
            this.getContacts();
        },
        methods: {
            getHighestRatingBooks(){
                axios.get('/api/highest-rating-books').then(response=> {
                    if (!response.data || response.data == undefined || !response.data.success){
                        this.$notify({
                            title: "Fetch highest rating books failed",
                            text: "Fetch highest rating books failed with unknown error, this can be from network or server",
                            type: "error"
                        });
  
                        return;
                    }
                    if (response.data.success === true){
                        /* this.$notify({
                            title: "Fetch highest rating books successfully!",
                            text: "Fetch highest rating books successfully!",
                            type: "success"
                        }); */
                        this.highestRatingBooks = response.data.result;
                    }else{
                        this.$notify({
                            title: "Fetch highest rating books failed",
                            text: "Fetch highest rating books failed with error: " + response.data.error,
                            type: "error"
                        });
                        
                    }   
                }).catch(err=>{
                    this.$notify({
                        title: "Fetch highest rating books failed",
                        text: "Fetch highest rating books failed with error: " + err.response.data.error,
                        type: "error"
                    });
                    
                }).finally(()=>{
                })   
            },
            getMostBorrowedBooks(){
                axios.get('/api/most-borrowed-books').then(response=> {
                    if (!response.data || response.data == undefined || !response.data.success){
                        this.$notify({
                            title: "Fetch highest rating books failed",
                            text: "Fetch highest rating books failed with unknown error, this can be from network or server",
                            type: "error"
                        });
  
                        return;
                    }
                    if (response.data.success === true){
                        
                        this.mostBorrowedBooks = response.data.result;
                    }else{
                        this.$notify({
                            title: "Fetch highest rating books failed",
                            text: "Fetch highest rating books failed with error: " + response.data.error,
                            type: "error"
                        });
                        
                    }   
                }).catch(err=>{
                    this.$notify({
                        title: "Fetch highest rating books failed",
                        text: "Fetch highest rating books failed with error: " + err.response.data.error,
                        type: "error"
                    });
                    
                }).finally(()=>{
                })   
            },
            getBookCount(){
                axios.get('/api/book-count').then(response=> {
                    if (!response.data || response.data == undefined || !response.data.success){
                        this.$notify({
                            title: "Fetch book count failed",
                            text: "Fetch book count failed with unknown error, this can be from network or server",
                            type: "error"
                        });
                        return;
                    }
                    if (response.data.success === true){    
                        this.bookCount = response.data.result;
                    }else{
                        this.$notify({
                            title: "Fetch book count failed",
                            text: "Fetch book count failed with error: " + response.data.error,
                            type: "error"
                        });
                        
                    }   
                }).catch(err=>{
                    this.$notify({
                        title: "Fetch book count failed",
                        text: "Fetch book count failed with error: " + err.response.data.error,
                        type: "error"
                    });
                    
                }).finally(()=>{
                })  
            },
            getBorrowCount(){
                axios.get('/api/borrow-count').then(response=> {
                    if (!response.data || response.data == undefined || !response.data.success){
                        this.$notify({
                            title: "Fetch borrow count failed",
                            text: "Fetch borrow count failed with unknown error, this can be from network or server",
                            type: "error"
                        });
  
                        return;
                    }
                    if (response.data.success === true){
                        this.borrowCount = response.data.result;
                    }else{
                        this.$notify({
                            title: "Fetch borrow count failed",
                            text: "Fetch borrow count failed with error: " + response.data.error,
                            type: "error"
                        });
                        
                    }   
                }).catch(err=>{
                    this.$notify({
                        title: "Fetch borrow count failed",
                        text: "Fetch borrow count failed with error: " + err.response.data.error,
                        type: "error"
                    });
                    
                }).finally(()=>{
                }) 
            },
            getContacts(){
                axios.get('/api/contacts').then(response => {
                  if (response.data.success === true){    
                    this.contactAddress = response.data.result.address;
                    this.contactEmail = response.data.result.email;
                    this.contactPhoneNumber = response.data.result.phone_number;
                  }else {
                    this.$notify({
                      title: "Get contacts failed",
                      text: "Get contacts failed",
                      type: "error"
                    });
                  }
                }).catch(err=>{
                    this.$notify({
                      title: "Get contacts failed",
                      text: "Get contacts failed",
                      type: "error"
                    });
                })
            }
        },
        components: {
            BookCarousel: BookCarousel
        }
    }
</script>