<!-- A component to display book data in a carousel -->
<template>
    <div class="carousel slide" data-bs-ride="carousel" data-bs-theme="dark" id="myCarousel"  >
        <div class="carousel-indicators">
            <button v-for="i in numSlides" :key="i" type="button" data-bs-target="#myCarousel" :data-bs-slide-to="(i-1)" :class="{ active: i === 1 }" :aria-label="'Slide ' + i"></button>        
        </div>

        <div class="carousel-inner" >
            <div v-for="i in numSlides" :key="books.id" style="padding-left: 10%; padding-right: 10%">
                <div v-if="i <= numSlides" class="carousel-item" data-bs-theme="light" :class="{ active: i === 1 }">
                    <div class="row">
                        <div class="col-md-4" v-for="j in 3" :key="j">
                            <div v-if="(i - 1) * 3 + (j - 1) <= books.length - 1">
                                <div class="card mb-3">
                                    <img :src="apiSite + '/image/' + $props.books[(i - 1) * 3 + (j - 1)].id" class="card-img-top" 
                                    :style="{ minHeight: $props.imgHeight + 'px', maxHeight: $props.imgHeight + 'px'} " :alt="'Book Cover for ' + books[(i - 1) * 3 + (j - 1)].title" :title="'Book Cover for ' + books[(i - 1) * 3 + (j - 1)].title"/>
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
        <button class="carousel-control-prev" type="button" data-bs-target="#myCarousel" data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#myCarousel"  data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Next</span>
        </button>
    </div>
</template>

<script>
import { RouterLink } from 'vue-router';

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
    }
  },
  computed: {
    numSlides() {
        let numSlides = Math.ceil(this.$props.books.length / 3);
        return numSlides;
    }
  }
};
</script>
