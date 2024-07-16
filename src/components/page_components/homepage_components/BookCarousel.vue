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
                        <div class="col-md-4" v-for="j in 3" :key="j">
                            <div v-if="(i - 1) * 3 + (j - 1) <= books.length - 1">
                                <div class="card mb-3">
                                    <img :src="apiSite + '/image/' + $props.books[(i - 1) * 3 + (j - 1)].id + '?id=' + getRandomId" class="card-img-top" 
                                    :style="{ minHeight: $props.imgHeight + 'px', maxHeight: $props.imgHeight + 'px'} " :alt="'Book Cover for ' + books[(i - 1) * 3 + (j - 1)].title" 
                                    :title="'Book Cover for ' + books[(i - 1) * 3 + (j - 1)].title"/>
                                    <div class="card-body">
                                        <h5 class="card-title">{{ $props.books[(i - 1) * 3 + (j - 1)].title }}</h5>
                                        <RouterLink :to="'/book/' + $props.books[(i - 1) * 3 + (j - 1)].id" class="btn btn-primary">View Book</RouterLink>
                                    </div>
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
  }
};
</script>
