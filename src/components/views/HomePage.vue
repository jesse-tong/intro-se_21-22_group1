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
                            <td><span>{{ getNormalDayRangeString() + ':' }}</span></td>
                            <td><span>{{ removeTimeSecond(normalDayOpen) + ' - ' + removeTimeSecond(normalDayClose) }}</span></td>
                        </tr>
                        <tr>
                            <td><span>{{ getWeekendDayRangeString() + ':' }}</span></td>
                            <td><span>{{ removeTimeSecond(weekendOpen) + ' - ' + removeTimeSecond(weekendClose) }}</span></td>
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

                normalDayOpen: 'N/A',
                normalDayClose: 'N/A',
                weekendOpen: 'N/A',
                weekendClose: 'N/A',
                weekendStart: 'N/A',
                weekendEnd: 'N/A',
                
                LibraryImage
            }
        },
        created(){
            this.getHighestRatingBooks();
            this.getMostBorrowedBooks();
            this.getBookCount(); this.getBorrowCount();
            this.getContacts(); this.getLibraryTimings();
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
            },
            getLibraryTimings(){
                axios.get('/api/timings').then(response => {
                  if (response.data.success === true){    
                    this.normalDayOpen = response.data.result.normal_open;
                    this.normalDayClose = response.data.result.normal_close;
                    this.weekendOpen = response.data.result.weekend_open;
                    this.weekendClose = response.data.result.weekend_close;
                    this.weekendStart = response.data.result.weekend_start;
                    this.weekendEnd = response.data.result.weekend_end;

                  }else {
                    this.$notify({
                      title: "Get library timings failed",
                      text: "Get library timings failed",
                      type: "error"
                    });
                  }
                }).catch(err=>{
                    this.$notify({
                      title: "Get library timings failed",
                      text: "Get library timings failed",
                      type: "error"
                    });
                })
            },
            removeTimeSecond(timeString){
                var [hour, minute, second] = timeString.split(':');
                return hour + ':' + minute;
            },
            getWeekendDayRangeString(){
                if (Number.isInteger(this.weekendStart) && parseInt(this.weekendStart) >=2 && parseInt(this.weekendStart) <= 8){
                    var startWeekendName =  this.daysOfWeek[parseInt(this.weekendStart) - 2];
                }else {
                    var startWeekendName = 'N/A';
                }
                if (Number.isInteger(this.weekendEnd) && parseInt(this.weekendEnd) >=2 && parseInt(this.weekendEnd) <= 8){
                    var endWeekendName =  this.daysOfWeek[parseInt(this.weekendEnd) - 2];
                }else {
                    var endWeekendName = 'N/A';
                }
                if (startWeekendName === endWeekendName){
                    return startWeekendName;
                }
                return startWeekendName + '-' + endWeekendName;
            },
            getNormalDayRangeString(){
                var indexStart = null, indexEnd = null;
                if (Number.isInteger(this.weekendStart) && parseInt(this.weekendStart) >=2 && parseInt(this.weekendStart) <= 8){
                    indexStart = (parseInt(this.weekendStart - 2) - 1) % this.daysOfWeek.length;
                    if (indexStart < 0) { indexStart = (indexStart + this.daysOfWeek.length) % this.daysOfWeek.length}
                    var startNormalDayName =  this.daysOfWeek[indexStart];
                }else {
                    var startNormalDayName = 'N/A';
                }
                if (Number.isInteger(this.weekendEnd) && parseInt(this.weekendEnd) >=2 && parseInt(this.weekendEnd) <= 8){
                    indexEnd = (parseInt(this.weekendEnd - 2) + 1) % this.daysOfWeek.length;
                    if (indexEnd < 0) { indexEnd = (indexEnd + this.daysOfWeek.length) % this.daysOfWeek.length}
                    var endNormalDayName =  this.daysOfWeek[indexEnd];
                }else {
                    var endNormalDayName = 'N/A';
                }
                
                if (indexStart !== null && indexEnd !== null && indexEnd < indexStart){
                    return endNormalDayName + '-' + startNormalDayName;
                }else if (indexStart === indexEnd){
                    return startNormalDayName;
                }else{
                    return startNormalDayName + '-' + endNormalDayName;
                }
                
            }
        },
        components: {
            BookCarousel: BookCarousel
        }
    }
</script>