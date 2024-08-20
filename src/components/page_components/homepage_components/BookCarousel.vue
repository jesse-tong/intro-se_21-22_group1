<!-- A component to display book data in a carousel -->
<template>
    <div class="carousel slide" data-bs-ride="carousel" :id="'myCarousel' + $props.carouselId"  >
        <div class="carousel-indicators" v-if="numSlides > 1">
            <button v-for="i in numSlides" :key="i" type="button" :data-bs-target="'#myCarousel' + $props.carouselId" :data-bs-slide-to="(i-1)" :class="{ active: i === 1 }" :aria-label="'Slide ' + i"></button>        
        </div>

        <div class="carousel-inner" >
            <div v-for="i in numSlides" :key="books.id" style="padding-left: 10%; padding-right: 10%">
                <div v-if="i <= numSlides" class="carousel-item" :class="{ active: i === 1 }">
                    <div class="row">

                        <div class="col-lg-4 col-md-6 wow fadeInUp" v-for="j in 3" :key="j">
                            <div class="course-item bg-light" v-if="(i - 1) * 3 + (j - 1) <= books.length - 1">
                                <div class="position-relative overflow-hidden">
                                    <img :src="apiSite + '/image/' + $props.books[(i - 1) * 3 + (j - 1)].id + '?id=' + getRandomId" class="card-img-top" 
                                    :style="{ minHeight: $props.imgHeight + 'px', maxHeight: $props.imgHeight + 'px'} " :alt="'Book Cover for ' + books[(i - 1) * 3 + (j - 1)].title" 
                                    :title="'Book Cover for ' + books[(i - 1) * 3 + (j - 1)].title"/>
                                    <div class="w-100 d-flex justify-content-center position-absolute bottom-0 start-0 mb-4">
                                        <RouterLink :to="'/book/' + $props.books[(i - 1) * 3 + (j - 1)].id" 
                                         class="flex-shrink-0 btn btn-sm btn-primary px-3 border-end" style="border-radius: 30px 0 0 30px;">Read More</RouterLink>

                                        <a href="#" @click="favoriteBook($props.books[(i - 1) * 3 + (j - 1)].id)" class="flex-shrink-0 btn btn-sm btn-primary px-3" style="border-radius: 0 30px 30px 0;">Favorite</a>
                                    </div>
                                </div>
                                <div class="text-center p-4 pb-0">
                                    <h5 class="mb-4">{{ $props.books[(i - 1) * 3 + (j - 1)].title }}</h5>
                                </div>
                                <div class="d-flex border-top">
                                    <small class="flex-fill text-center border-end py-2"><i class="bi bi-bookmarks-fill me-2"></i><div class="sr-only">Remaining books</div>{{ $props.books[(i - 1) * 3 + (j - 1)].stock }}</small>
                                    <small class="flex-fill text-center border-end py-2"><i class="bi bi-clock text-primary me-2"></i><div class="sr-only">Publish year</div>{{$props.books[(i - 1) * 3 + (j - 1)].publish_year}}</small>
                                    <small class="flex-fill text-center py-2"><i class="bi bi-bookmark me-2"></i><div class="sr-only">ISBN</div>{{$props.books[(i - 1) * 3 + (j - 1)].isbn}}</small>
                                </div>
                            </div>
                        </div>

                        
                    </div>
                </div>
            </div>
        </div>
        <button class="carousel-control-prev" type="button" :data-bs-target="'#myCarousel' + $props.carouselId" data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" :data-bs-target="'#myCarousel' + $props.carouselId"  data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Next</span>
        </button>
    </div>
</template>

<script>
import { RouterLink } from 'vue-router';
import { v4 as uuidv4 } from 'uuid';
import axios from 'axios';

export default {
  props: {
    books: {
      type: Array,
      required: true,
      default: []
    },
    imgHeight: {
      type: Number,
      default: 375
    },
    carouselId: {
      type: String,
      default: ''
    }
  },
  computed: {
    numSlides() {
        let numSlides = Math.ceil(this.$props.books.length / 3);
        return numSlides;
    },
    getRandomId(){
        //This will generated a random uuid and added to img src as a query 
        //so that Vue will not use the cached image but the updated one instead
        return uuidv4();
    }
  },
  methods: {
    favoriteBook(bookId){
        axios.post('/api/favorite/' + bookId);
    }
  }
};
</script>
