<template>
    <div>
      <table class="table">
        <thead>
          <tr>
            <th>Title</th>
            <th>Publish Year</th>
            <th>ISBN</th>
            <th>Stock in library</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="book in data" :key="book.id">
            <td>{{ book.title }}</td>
            <td>{{ book.publish_year }}</td>
            <td>{{ book.isbn }}</td>
            <td>{{ book.stock }}</td>
            <td>{{ book.description }}</td>
          </tr>
        </tbody>
      </table>
      <nav>
        <ul class="pagination">
          <li class="page-item" v-for="pageNumber in totalPages" :key="pageNumber" @click="setPage(pageNumber)">
            <a :class="['page-link', pageNumber === page ? 'active' : '']" href="#"> {{ pageNumber }} </a>
          </li>
        </ul>
      </nav>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      page: {
        type: Number,
        required: true
      },
      data: {
        type: Array,
        required: true
      },
      totalPages: {
        type: Number,
        required: true
      }
    },
    computed: {
      paginatedData() {
        const startIndex = (this.page - 1) * 10;
        const endIndex = this.page * 10;
        
        return this.data.slice(startIndex, endIndex);
      }
    },
    methods: {
      setPage(pageNumber) {
        this.$emit('update:page', pageNumber);
      }
    }
  };
  </script>