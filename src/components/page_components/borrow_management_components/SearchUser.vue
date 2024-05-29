<template>
    <div class="row-md-6">
      <div class="row">
        <div class="col-12 col-md-8">
          <div class="form-group">
            <label for="searchUserEmail">Search User Email:</label>
            <input :value="searchUserEmail" @input="$emit('update:searchUserEmail', $event.target.value)" type="email" class="form-control" id="searchUserEmail" placeholder="Enter user email">
          </div>
          <div class="form-group">
            <label for="searchUserName">Search User Name (Optional):</label>
            <input :value="searchUserName" @input="$emit('update:searchUserName', $event.target.value)" type="text" class="form-control" id="searchUserName" placeholder="Enter user name">
          </div>
        </div>
        <div class="col-12 col-md-4">
          <div class="form-group">
            <label for="searchUserId">Search User ID (Optional):</label>
            <input :value="searchUserId" type="number" min="1" @input="$emit('update:searchUserId', $event.target.value)"  class="form-control" id="searchUserId" placeholder="Enter user ID">
          </div>
          <button @click="$emit('search-user')" class="btn btn-primary mt-4" id="searchUserButton">Search User</button>
        </div>
      </div>
      
    </div>
  </template>
  
  <script>
  export default {
    props: {
      searchUserEmail: {
        type: String,
        default: '',
      },
      searchUserName: {
        type: String,
        default: '',
      },
      searchUserId: {
        type: [Number, null],
        default: null,
        required: false
      }
    },
    emits: ['search-user', 'update:searchUserEmail', 'update:searchUserName','update:searchUserId'],
  };
  </script>
  