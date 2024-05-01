<template>
    <table class="table table-striped table-responsive-md">
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
        <tr v-for="borrow in borrows" :key="borrow.id" >
          <td>{{ borrow.userId }}</td>
          <td>{{ borrow.bookId }}</td> 
          <td>{{ borrow.startBorrow ? getDateString(borrow.startBorrow): 'N/A' }}</td>
          <td>{{ borrow.endBorrow ? getDateString(borrow.endBorrow): 'N/A' }}</td>
          <td>{{ borrow.hasReturned ? 'Yes' : 'No' }}</td>
          <td>{{ borrow.returnDate ? getDateString(borrow.returnDate) : 'N/A'}}</td>
          <td>{{ borrow.isDamagedOrLost ? 'Yes' : 'No' }}</td>
          <td>{{ borrow.isApproved ? 'Yes' : 'No' }}</td>
          <td>
            <button class="btn btn-sm btn-primary" @click="$emit('editBorrow', borrow)">Edit</button>
            <button class="btn btn-sm btn-danger" @click="$emit('deleteBorrow', borrow.id)" >Delete</button>
          </td>
        </tr>
        <tr v-if="borrows == null || borrows.length === 0" >
          <td colspan="9" ><p class="text-center"><i>Currently no borrow status data</i></p></td>
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
        //console.log('Original date', date);
        return new Date(Date.parse(date)).toString();
      }
    },
    emits: ['deleteBorrow', 'editBorrow'],
  };
  </script>
  