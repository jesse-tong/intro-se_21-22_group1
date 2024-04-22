<template>
    <table class="table table-striped">
      <thead>
        <tr>
          <th>User ID</th>
          <th>Book Title</th>
          <th>Start Borrow</th>
          <th>End Borrow</th>
          <th>Returned</th>
          <th>Return Date</th>
          <th>Damaged/Lost</th>
          <th>Is Approved</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="borrow in borrows" :key="borrow.id">
          <td>{{ borrow.userId }}</td>
          <td>{{ borrow.bookId }}</td> 
          <td>{{ getDateString(borrow.startBorrow) }}</td>
          <td>{{ getDateString(borrow.endBorrow) }}</td>
          <td>{{ borrow.hasReturned ? 'Yes' : 'No' }}</td>
          <td>{{ borrow.returnDate ? getDateString(borrow.returnDate) : 'N/A'}}</td>
          <td>{{ borrow.isDamagedOrLost ? 'Yes' : 'No' }}</td>
          <td>{{ borrow.isApproved ? 'Yes' : 'No' }}</td>
          <td>
            <button class="btn btn-sm btn-primary" @click="$emit('edit-borrow', borrow)">Edit</button>
            <button class="btn btn-sm btn-danger" @click="$emit('delete-borrow', borrow.id)" >Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </template>
  
  <script>
  export default {
    props: {
      borrows: Array,
    },
    methods: {
      getDateString(date){
        return Date(date).toLocaleString();
      }
    },
    emits: ['deleteBorrow', 'editBorrow'],
  };
  </script>
  