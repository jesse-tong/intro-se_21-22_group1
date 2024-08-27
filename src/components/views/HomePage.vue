<template>
<div class="col">
    <div class="row-5">
        <div class="library-homepage-container">
            <img :src="LibraryImage" style="width: 100%; max-height: 400px;" alt="Library image"/>
            
            <h1 style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;" class="library-homepage-image-text text-white display-1">Welcome to library</h1>
        </div>
        <div class="mx-3 my-3 row row-cols-1 row-cols-md-2 row-cols-lg-3 row-gap-3">
            <div class="col">
                <div class="card bg-light-subtle shadow-sm">
                    <div class="card-body">
                        <RouterLink to="/search-website" class="text-decoration-none" title="Search books, events, articles,... in this website">
                            <h5 class="card-title text-primary"><i class="bi bi-search me-2"></i>Search website</h5>
                        </RouterLink>
                    </div>
                </div>
            </div>
            <div class="col">
                <div class="card bg-light-subtle shadow-sm">
                    <div class="card-body">
                        <RouterLink to="/get-library-card" class="text-decoration-none"><h5 class="card-title text-primary"><i class="bi bi-credit-card-2-front-fill me-2"></i>Get a library card</h5></RouterLink>
                    </div>
                </div>
            </div>
            <div class="col">
                <div class="card bg-light-subtle shadow-sm">
                    <div class="card-body">
                        <RouterLink to="/user/settings#yourCurrentBorrows" class="text-decoration-none" 
                        title="You can renew book in the user settings for borrow if you haven't return the item yet and the borrow request was approved">
                            <h5 class="card-title text-primary"><i class="bi bi-clock-history me-2"></i>Renew item</h5>
                        </RouterLink>
                    </div>
                </div>
            </div>
            <div class="col">
                <div class="card bg-light-subtle shadow-sm">
                    <div class="card-body">
                        <RouterLink to="/book/advanced-search" class="text-decoration-none" title="Advanced search for books and materials">
                            <h5 class="card-title text-primary"><i class="bi bi-search me-2"></i>Search catalogue (advanced)</h5>
                        </RouterLink>
                    </div>
                </div>
            </div>
        </div>
        <h5 class="section-title bg-light-subtle text-start text-primary mt-3 ps-3 pe-3">Latest library articles</h5>
        <ArticleCarousel :articles="latestArticles" :carouselId="'latestArticles'"/>
        <h5 class="section-title bg-light-subtle text-start text-primary mt-3 ps-3 pe-3">Highest rating books</h5>
        <BookCarousel :books="highestRatingBooks" :apiSite="apiSite" :carouselId="'highestRatingBooks'"/>

        <h5 class="section-title bg-light-subtle text-start text-primary mt-3 ps-3 pe-3">Most borrowed books</h5>
        <BookCarousel :books="mostBorrowedBooks" :apiSite="apiSite" :carouselId="'mostBorrowedBooks'"/>
        
    </div>
    <div class="row">
        <hr class="hr" />
    </div>
    <div class="row-5">
        <div class="row">
            <div class="col-12 col-md-5 col-lg-4">
                <div class="ps-4">
                    <table class="table ps-0 ps-lg-2 table-bordered">
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
                            <tr>
                                <th class="table-active text-center" colspan="2">LIBRARY MAP</th>
                            </tr>
                            <tr>
                                <td colspan="2">
                                    <div class="w-100" style="min-height: 180px;" id="map"></div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                
            </div>
            <div class="col-12 col-md-2 col-lg-4">
                
            </div>
            <div class="col-12 col-md-5 col-lg-4">
                <table class="table table-bordered me-2">
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
    import ArticleCarousel from '../page_components/homepage_components/ArticleCarousel.vue';
    import LibraryImage from '../../assets/library.jpg';
    import { useAccountStore } from '../stores/LoginInfoStore';
    import { mapStores } from 'pinia';
    import "leaflet/dist/leaflet.css";
    import markerIconPng from "leaflet/dist/images/marker-icon.png"
    import * as L from 'leaflet';
import { RouterLink } from 'vue-router';



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

                latestArticles: [],
                map: null,
                libraryCoordinate: null,
                LibraryImage
            }
        },
        created(){
            this.getHighestRatingBooks();
            this.getMostBorrowedBooks();
            this.getBookCount(); this.getBorrowCount();
            this.getContacts(); this.getLibraryTimings();
            this.getLatestArticles();
            
        },
        beforeMount(){
            if (this.$route.query.userId !== undefined && this.$route.query.userId !== null
            && this.$route.query.name !== undefined && this.$route.query.name !== null 
            && this.$route.query.role !== undefined && this.$route.query.role !== null){
                this.accountStore.clearStoredData();
                this.accountStore.setAccountInfo(this.$route.query.userId, this.$route.query.name, 
                this.$route.query.role, this.$route.query.isRestricted);
                this.accountStore.setLocalStorage();
                axios.post('/analytics', {
                  referer: document.referrer,
                }).then(response => {}).catch(()=>{})
                this.$router.replace('/');
            };
            
        },
        mounted(){
            //this.initiateMap();
        },
        computed: {
            ...mapStores(useAccountStore)
        },
        watch: {
            contactAddress: {
                handler(newAddress){
                    if (newAddress !== null && newAddress !== 'N/A'){                       
                        this.coordinateFromAddress(newAddress);
                    }
                },
                once: true
            },
            libraryCoordinate: {
                handler(newCoordinate){
                    this.initiateMap(newCoordinate);
                }
            }
        },
        methods: {
            initiateMap(libraryCoordinate){
                if (libraryCoordinate !== null && this.tileServer !== null){
                    const markerIcon = L.icon({
                        iconUrl: markerIconPng
                    });
                    var map = L.map('map', { minZoom: 9.5, maxZoom: 17}).setView(libraryCoordinate, 16);

                    L.tileLayer(this.tileServer + '/{z}/{x}/{y}.png', {
                        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    }).addTo(map);

                    L.marker(libraryCoordinate, {icon: markerIcon}).addTo(map)
                        .bindPopup('Library location: ' + this.contactAddress)
                        .openPopup();
                }
                
            },
            parseAddress(addressString){
                var result = {}; let splitByCommas = String(addressString).split(',');
                splitByCommas.forEach((subString) => {
                    if (subString.match(/\s+street\s*/i) !== null){
                        result.street = subString.replace(/\s+street\s*/i, '');
                    }else if (subString.match(/\s+city\s*/i) !== null){
                        result.city = subString.replace(/\s+country\s*/i, '');
                    }else if (subString.match(/\s+county\s*/i) !== null){
                        result.county = subString.replace(/\s+county\s*/i, '');
                    }else if (subString.match(/\s+state\s*/i) !== null){
                        result.state = subString.replace(/\s+state\s*/i, '');
                    }else if (subString.match(/\s+country\s*/i) !== null){
                        result.country = subString.replace(/\s+country\s*/i, '');
                    }
                });
                //If street not found, and the first substring not match one of the above, use the first substring
                if (!result.street && splitByCommas.length > 0 
                && splitByCommas[0].match(/\s+street|county|state|city|country\s*/i) === null){
                    result.street = splitByCommas[0];
                }
                //If country not found, and the last substring not match one of the above, use the last substring
                if (!result.country && splitByCommas.length > 1 
                && splitByCommas[splitByCommas.length - 1].match(/\s+street|county|state|city|country\s*/i) === null){
                    result.country = splitByCommas[splitByCommas.length - 1];
                }
                return result;
            },
            coordinateFromAddress(addressString){
                var searchObj = this.parseAddress(addressString);
                searchObj.format = 'json'; searchObj.limit = 1;
                axios.get(this.nominatimServer + '/search', { params: searchObj, withCredentials: false})
                    .then(response => {
                        
                        this.libraryCoordinate = [parseFloat(response.data[0].lat), parseFloat(response.data[0].lon)];
                    })
            },
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
                    if (err.response && err.response.data && err.response.data.error){
                        this.$notify({
                            title: "Fetch highest rating books failed",
                            text: "Fetch highest rating books failed with error: " + err.response.data.error,
                            type: "error"
                        });
                    } 
                }).finally(()=>{
                })   
            },
            getLatestArticles(){
                axios.get('/api/article', { params: { page: 1, limit: 10}}).then(response => {
                    if (response.data !== undefined && response.data.success === true){
                        this.latestArticles = response.data.result;
                    }
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
                    if (err.response && err.response.data && err.response.data.error){
                        this.$notify({
                            title: "Fetch highest rating books failed",
                            text: "Fetch highest rating books failed with error: " + err.response.data.error,
                            type: "error"
                        });
                    }
  
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
                    if (err.response && err.response.data && err.response.data.error){
                        this.$notify({
                            title: "Fetch book count failed",
                            text: "Fetch book count failed with error: " + err.response.data.error,
                            type: "error"
                        });
                    }   
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
                    if (err.response && err.response.data && err.response.data.error){
                        this.$notify({
                            title: "Fetch borrow count failed",
                            text: "Fetch borrow count failed with error: " + err.response.data.error,
                            type: "error"
                        });
                    }   
                    
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
            BookCarousel: BookCarousel,
            ArticleCarousel: ArticleCarousel,
        }
    }
</script>