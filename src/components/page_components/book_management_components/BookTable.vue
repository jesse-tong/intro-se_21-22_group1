<template>
  <div class="table-reponsive-lg">
    <table class="table table-striped">
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
        <ul class="pagination">
            <li class="page-item">
                <a href="#prevPageButton" class="page-link" @click="$emit('update:currentPage', currentPage > 1 ? currentPage - 1 : 1)" id="prevPageButton"><span>Previous page</span></a>
            </li>
            <li class="page-item">
                <input @input="(e)=>$emit('update:currentPage', e.target.value)" type="number" min="1" :max="maxPage" class="page-link" style="max-width: 95px" :value="currentPage">
            </li>
            <li class="page-item">
                <a href="#nextPageButton" class="page-link" @click="$emit('update:currentPage', currentPage < maxPage ? currentPage + 1 : 1)" id="nextPageButton"><span >Next page</span></a>
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