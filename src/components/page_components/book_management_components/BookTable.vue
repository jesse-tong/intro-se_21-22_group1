<template>
  <div class="table-reponsive-lg">
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Book ID</th>
          <th>Book Title</th>
          <th>Publish year</th>
          <th>ISBN</th>
          <th>Stock</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="book in books" :key="book.id" data-testid="bookTableRow">
          <td>{{ book.id }}</td>
          <td>{{ book.title }}</td> 
          <td>{{ book.publish_year }}</td>
          <td>{{ book.isbn }}</td>
          <td>{{ book.stock }}</td>
          <td>
            <button class="btn btn-sm btn-primary me-2" @click="$emit('editBook', book.id)">Edit</button>
            <button class="btn btn-sm btn-danger" @click="$emit('deleteBook', book.id)" >Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
    <nav aria-label="Book table navigation">
        
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
  export default {
    props: {
      books:{
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

    emits: ['deleteBook', 'editBook', 'update:currentPage'],
  };
  </script>