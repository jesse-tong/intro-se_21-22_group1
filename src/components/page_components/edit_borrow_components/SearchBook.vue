<template>
    <div class="row-md-6">
      <div class="form-group">
        <label for="searchBookTitle">Search Book Title:</label>
        <input  :value="searchBookTitle" @input="$emit('update:searchBookTitle', $event.target.value)"  type="text" class="form-control" id="searchBookTitle" placeholder="Enter book title">
      </div>
      <div class="form-group">
        <label for="searchBookIsbn">Search Book ISBN (Optional):</label>
        <input :value="searchBookIsbn" @input="$emit('update:searchBookIsbn', $event.target.value)" type="text" class="form-control" id="searchBookIsbn" placeholder="Enter book ISBN">
      </div>
      <button @click="$emit('search-book')" class="btn btn-primary mt-3">Search Book</button>
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
    },
    emits: ['search-book', 'update:searchBookTitle', 'update:searchBookIsbn'],
  };
  </script>
  