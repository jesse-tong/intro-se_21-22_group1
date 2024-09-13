<!-- A component to display book data in a carousel -->
<template>
    <div class="carousel slide" data-bs-ride="carousel" :id="'myCarousel' + $props.carouselId"  >
        <carousel v-bind="settings" :breakpoints="breakpoints" :wrap-around="true" >
            <slide class="px-2" v-for="book in $props.books">
                <div class="course-item bg-light d-flex flex-column" style="max-width: 375px;">
                    <div class="position-relative overflow-hidden">
                        <img :src="apiSite + '/image/' + book.id + '?id=' + getRandomId" class="card-img-top" 
                        :style="{ minHeight: $props.imgHeight + 'px', maxHeight: $props.imgHeight + 'px'} " :alt="'Book Cover for ' + book.title" 
                        :title="'Book Cover for ' + book.title"/>
                        <div class="w-100 d-flex justify-content-center position-absolute bottom-0 start-0 mb-4">
                            <RouterLink :to="'/book/' + book.id" 
                                class="flex-shrink-0 btn btn-sm btn-primary px-3 border-end" style="border-radius: 30px 0 0 30px;">Read More</RouterLink>

                            <a href="#" @click="favoriteBook(book.id)" class="flex-shrink-0 btn btn-sm btn-primary px-3" style="border-radius: 0 30px 30px 0;">Favorite</a>
                        </div>
                    </div>
                    <div class="text-center p-4 pb-0">
                        <h5 class="mb-4">{{ book.title }}</h5>
                    </div>
                    <div class="d-flex border-top">
                        <small class="flex-fill text-center border-end py-2"><i class="bi bi-bookmarks-fill me-2"></i><div class="sr-only">Remaining books</div>{{ book.stock }}</small>
                        <small class="flex-fill text-center border-end py-2"><i class="bi bi-clock text-primary me-2"></i><div class="sr-only">Publish year</div>{{ book.publish_year}}</small>
                        <small class="flex-fill text-center py-2"><i class="bi bi-bookmark me-2"></i><div class="sr-only">ISBN</div>{{book.isbn}}</small>
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
import axios from 'axios';
import emptyImage from '../../../assets/empty_image.png';
export default {
  props: {
    books: {
      type: Array,
      required: true,
      default: [],
      emptyImage
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
  components: {
    Carousel,
    Slide,
    Pagination,
    Navigation,
  },
  computed: {
    getRandomId(){
        //This will generated a random uuid and added to img src as a query 
        //so that Vue will not use the cached image but the updated one instead
        return uuidv4();
    }
  },
  data() {
    return {
        settings: {
            itemsToShow: 1,
            snapAlign: 'center',
        },
        breakpoints: {            
            900: {
                itemsToShow: 2,
                snapAlign: 'center',
            },
            // 1024 and up
            1024: {
                itemsToShow: 3,
                snapAlign: 'start',
            },
            1200: {
                itemsToShow: 3,
                snapAlign: 'start',
            },
            1680: {
                itemsToShow: 4,
                snapAlign: 'start',
            }
        }
    }
  },
  methods: {
    favoriteBook(bookId){
        axios.post('/api/favorite/' + bookId);
    }
  }
};
</script>
