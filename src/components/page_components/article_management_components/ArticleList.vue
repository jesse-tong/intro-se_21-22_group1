<template>
    <div class="table-reponsive-lg mt-3">
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>Article ID</th>
            <th colspan="3">Article category</th>
            <th colspan="5">Article title</th>
            <th colspan="2">Article last edited date</th>
            <th v-if="$props.actionVisible === true">Actions</th>
            <th v-else></th>
          </tr>
        </thead>
        <tbody>
          <tr  v-if="articles.length > 0" v-for="article in articles" :key="article.id" data-testid="articleTableRow">
            <td>{{ article.id }}</td>
            <td colspan="3">{{ article.category ? article.category : '' }}</td>
            <td colspan="5">{{ article.title }}</td> 
            <td colspan="2">{{ convertISODatetimeToLocal(article.date) }}</td>
            <td v-if="$props.actionVisible === true">
              <button class="btn btn-sm btn-primary me-2" @click="$emit('editArticle', article.id)">Edit</button>
              <button class="btn btn-sm btn-danger" @click="$emit('deleteArticle', article.id)" >Delete</button>
            </td>
            <td v-else>
              <RouterLink :to="'/article/' + article.id " role="btn btn-primary" class="btn btn-primary">Go to article</RouterLink>
            </td>
          </tr>
        </tbody>
      </table>
      <nav aria-label="Article list management navigation">
        <ul class="component-pagination">
            <li class="pagination-arrow arrow-left me-1">
                <a href="#" class="page-link" @click="$emit('update:currentPage', currentPage > 1 ? currentPage - 1 : 1)" id="prevPageButton"><i class="bi bi-chevron-left"></i></a>
            </li>
            <li class="page-item">
                <li class="pagination-number current-number" ><input type="number" style="margin: 0 5px; max-width: 50px;" 
                  @input="(e)=>$emit('update:currentPage', e.target.value)" :value="currentPage" min="1"/></li>
            </li>
            <li class="pagination-arrow arrow-left ms-1">
                <a href="#" class="page-link" @click="$emit('update:currentPage', currentPage < maxPage ? currentPage + 1 : 1)" id="nextPageButton"><i class="bi bi-chevron-right"></i></a>
            </li>
        </ul>
      </nav>
    </div>
    </template>
    
    <script>
import { RouterLink } from 'vue-router';

    export default {
      props: {
        articles:{
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
        },
        actionVisible: {
          type: Boolean,
          default: true
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
        convertISODatetimeToLocal(localDatetimeString){
            //Since input="local-datetime" only accept YYYY-mm-ddThh:ss, not YYYY-mm-ddThh:ssZ of ISO string
            let currentLocalDate = new Date();
            let localTimeOffset = currentLocalDate.getTimezoneOffset() * 60 * 1000; //Get local timezone offset to GMT by milliseconds

            let gmtTime = new Date(localDatetimeString); 
            let localTime = gmtTime - localTimeOffset; localTime = new Date(localTime);
            let localString = localTime.toLocaleString();

            return localString;
        },
      },
      emits: ['deleteArticle', 'editArticle', 'update:currentPage'],
    };
    </script>