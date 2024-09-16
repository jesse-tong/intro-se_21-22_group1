<template>
    <div class="" :id="'myCarousel' + $props.carouselId"  >
        <carousel v-bind="settings" :breakpoints="breakpoints" :wrap-around="true" >      
            <slide v-for="article in $props.articles" :key="article.id" class="px-2">
                <div class="card mb-3" style="max-width: 320px;">
                    <img class="card-img-top" style="height: 180px;" :src="article.thumbnail" :alt="'Image for artitle with title: ' + article.title" @error="($event) => setAltImg($event)"/>
                    <div class="card-body" style="height: 200px; overflow: auto">
                        <p style="font-weight: 700; text-align: left;" class="text-secondary ms-1"><small>{{ article.category }}</small></p>
                        <router-link :to="'/article/' + article.id" class="card-title link-underline link-underline-opacity-0 link-underline-opacity-75-hover">
                            <h5 style="text-align: left">{{ article.title }}</h5>
                        </router-link>
                        <p class="text-body-secondary mb-2 card-subtitle"><i class="bi bi-calendar3"></i><span class="ms-2">{{ article.date }}</span></p>
                        <RouterLink :to="'/article/' + article.id" class="btn btn-primary">View Article</RouterLink>
                    </div>
                </div>
            </slide>  
            <template #addons>
                <navigation />
                <pagination />
            </template>          
        </carousel>  
    </div>

</template>

<script>
import 'vue3-carousel/dist/carousel.css';
import { Carousel, Slide, Pagination, Navigation } from 'vue3-carousel';
import { v4 as uuidv4 } from 'uuid';
import emptyImage from '../../../assets/empty_image.png';

export default {
  components: {
    Carousel,
    Slide,
    Pagination,
    Navigation,
  },
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
      emptyImage,
      settings: {
        itemsToShow: 1,
        snapAlign: 'center',
      },
      breakpoints: {
        // 700px and up
            
            768: {
                itemsToShow: 2,
                snapAlign: 'center',
            },
            // 1024 and up
            1024: {
                itemsToShow: 3,
                snapAlign: 'start',
            },
            1200: {
                itemsToShow: 4,
                snapAlign: 'start',
            },
            1680: {
                itemsToShow: 5,
                snapAlign: 'start',
            }
        }
    };
  },
  computed: {
    
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
