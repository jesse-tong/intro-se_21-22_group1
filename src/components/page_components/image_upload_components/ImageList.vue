<template>
    <div class="">
        <div class="row">
          <div class="col-12 col-md-6 col-lg-4 col-xl-3 " v-if="images.length > 0" v-for="image in images" :key="image.id" data-testid="imageCard">
            <div class="mx-2 h-100 p-1">
              <div class="card h-100 mx-1 my-1 p-1" >
                  <div class="card-img-top">
                    <img :src="apiSite + '/uploaded-image/' + image.id" class="thumbnail" :alt="image.imagePath" >
                  </div>
                  
                  <h6 class="card-title">{{ image.imagePath }}</h6> 
                  <p class="card-text">{{ 'ID: ' + image.id }}</p>
                  <div>
                  <button class="btn btn-sm btn-primary me-3 mb-1 mb-md-0" @click="()=>onSelectImage(image)">Select</button>
                  <button class="btn btn-sm btn-danger" @click="$emit('deleteImage', image.id)" >Delete</button>
                  </div>
              </div>
            </div>
            
          </div>
            
        </div>
      <nav aria-label="Image list management navigation" class="mt-3 ms-2">
          <ul class="pagination">
              <li class="page-item">
                  <div role="button" class="page-link cursor-pointer" @click="$emit('update:currentPage', currentPage > 1 ? currentPage - 1 : 1)" id="prevPageButton"><span>Previous page</span></div>
              </li>
              <li class="page-item">
                  <input @input="(e)=>$emit('update:currentPage', e.target.value)" type="number" min="1" :max="maxPage" class="page-link" style="max-width: 95px" :value="currentPage">
              </li>
              <li class="page-item">
                  <div role="button" class="page-link cursor-pointer" @click="$emit('update:currentPage', currentPage < maxPage ? currentPage + 1 : 1)" id="nextPageButton"><span >Next page</span></div>
              </li>
          </ul>
      </nav>
    </div>
    </template>
    
    <script>
    export default {
      props: {
        images:{
          type: Array,
          required: true
        },
        maxPage: {
          type: Number,
          default: 10
        },
        currentPage: {
          type: Number,
          required: true
        }
      },
      data(){
          return {}
      },
      watch: {
          currentPage: {
              handler(newPage){
                  this.$emit('update:currentPage', newPage);
              }
          }
      },
      methods: {
        onSelectImage(image){
          this.$emit('selectImage', { id: image.id, fileName: image.imagePath});
        }
      },
  
      emits: ['deleteImage', 'selectImage', 'update:currentPage'],
    };
    </script>