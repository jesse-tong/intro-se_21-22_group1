<template>
    <div class="row-md-6">
      <div class="row">
        <div class="col-12 col-md-8">
          <div class="form-group">
            <label for="searchBookTitle">Search Book Title:</label>
            <input :value="searchBookTitle" @input="$emit('update:searchBookTitle', $event.target.value)"  type="text" class="form-control" id="searchBookTitle" placeholder="Enter book title">
          </div>
          <div class="form-group">
            <label for="searchBookIsbn">Search Book ISBN (Optional):</label>
            <input :value="searchBookIsbn" @input="$emit('update:searchBookIsbn', $event.target.value)" type="text" class="form-control" id="searchBookIsbn" placeholder="Enter book ISBN">
          </div>
        </div>
        <div class="col-12 col-md-4">
          <div class="form-group">
            <label for="searchBookId">Search Book ID (Optional):</label>
            <input :value="searchBookId" type="number" min="1" @input="$emit('update:searchBookId', $event.target.value)"  class="form-control" id="searchBookId" placeholder="Enter book ID">
          </div>
          <button @click="$emit('search-book')" class="btn btn-primary mt-4">Search Book</button>
        </div>
      </div>
      
      
    </div>
  </template>
  
  <script>
  export default {
    props: {
      searchBookTitle: {
        type: String,
        default: '',
      },
      searchBookIsbn: {
        type: String,
        default: '',
      },
      searchBookId: {
        type: [Number, null],
        default: null,
        required: false
      }
    },
    emits: ['search-book', 'update:searchBookTitle', 'update:searchBookIsbn', 'update:searchBookId'],
  };
  </script>
  