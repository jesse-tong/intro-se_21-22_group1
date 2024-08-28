<template>
    <div class="carousel slide" data-bs-ride="carousel" :id="'myCarousel' + $props.carouselId"  >
        <div class="carousel-indicators" v-if="numSlides > 1">
            <button v-for="i in numSlides" :key="i" type="button" :data-bs-target="'#myCarousel' + $props.carouselId" :data-bs-slide-to="(i-1)" :class="{ active: i === 1 }" :aria-label="'Slide ' + i"></button>        
        </div>

        <div class="carousel-inner" >
            <div v-for="i in numSlides" :key="articles.id" style="padding-left: 10%; padding-right: 10%">
                <div v-if="i <= numSlides" class="carousel-item" :class="{ active: i === 1 }">
                    <div class="row mx-3">
                        <div class="col-12 col-md-6 col-lg-4" v-for="j in 3" :key="j">
                            <div v-if="(i - 1) * 3 + (j - 1) <= articles.length - 1">
                                <div class="card mb-3" >
                                    <img class="card-img-top" style="height: 180px;" :src="$props.articles[(i - 1) * 3 + (j - 1)].thumbnail" :alt="'Image for artitle with title: ' + $props.articles[(i - 1) * 3 + (j - 1)].title" @error="($event) => setAltImg($event)"/>
                                    <div class="card-body" style="height: 200px; overflow: auto">
                                        <router-link :to="'/article/' + $props.articles[(i - 1) * 3 + (j - 1)].id" class="card-title link-underline link-underline-opacity-0 link-underline-opacity-75-hover">
                                            <h5 class="">{{ $props.articles[(i - 1) * 3 + (j - 1)].title }}</h5>
                                        </router-link>
                                        <p class="text-body-secondary mb-2 card-subtitle"><i class="bi bi-calendar3"></i><span class="ms-2">{{ $props.articles[(i - 1) * 3 + (j - 1)].date }}</span></p>
                                        <RouterLink :to="'/article/' + $props.articles[(i - 1) * 3 + (j - 1)].id" class="btn btn-primary">View Article</RouterLink>
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
import emptyImage from '../../../assets/empty_image.png';

export default {
  props: {
    articles: {
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
  data() {
    return {
      emptyImage
    };
  },
  computed: {
    numSlides() {
        let numSlides = Math.ceil(this.$props.articles.length / 4);
        return numSlides;
    },
    getRandomId(){
        //This will generated a random uuid and added to img src as a query 
        //so that Vue will not use the cached image but the updated one instead
        return uuidv4();
    },
    
  },
  methods: {
    setAltImg(e){
        e.target.onerror = null;
        e.target.src = emptyImage;
        e.target.style.backgroundImage = 'linear-gradient(135deg, #e66465, #9198e5)';
        e.target.alt = 'Image not found';
        e.target.title = 'Image not found';
    }
  }
};
</script>
