<template>
<div class="card">
    <div class="card-header">
        <h5>Most recent borrows</h5>
    </div>
    <div class="card-body">
        <div v-for="borrow, idx in mostRecentBorrows" class="card-text">
            <p class="mb-0 pb-0 ms-0 ps-0" ><i :class="['bi', 'bi-circle-fill', 'text-' + colorClasses[idx % 6]]"></i> 
                <span class="ms-1">
                    {{ 'User with ID ' + borrow.userId + ' (' + borrow.username + ') has sent a borrow request to borrow book with ID ' + borrow.bookId + ' (' + borrow.title + ')'}}
                </span>
            </p>
            <div class="vr ms-2" v-if="idx !== mostRecentBorrows.length - 1"></div>
        </div>
        
    </div>
</div>
</template>
<script>
import axios from 'axios';
export default {
    data(){
        return {
            mostRecentBorrows: [],
            colorClasses: ['primary', 'success', 'info', 'warning', 'danger', 'secondary']
        }
        
    },
    methods: {
        fetchMostRecentBorrows(){
            axios.get('/api/most-recent-borrows').then(response=> {
                    if (!response.data || response.data == undefined || !response.data.success){
                        this.$notify({
                            title: "Fetch most recent borrow failed",
                            text: "Fetch most recent borrow failed with unknown error, this can be from network or server",
                            type: "error"
                        });
  
                        return;
                    }
                    if (response.data.success === true){
                        
                        this.mostRecentBorrows = response.data.result;
                    }else{
                        this.$notify({
                            title: "Fetch most recent borrows failed",
                            text: "Fetch most recent borrows failed with error: " + response.data.error,
                            type: "error"
                        });
                        
                    }   
                } ).catch(err=>{
                    this.$notify({
                        title: "Fetch most recent borrows failed",
                        text: "Fetch most recent borrows failed with error: " + err.response.data.error,
                        type: "error"
                    });
                    
                }).finally(()=>{
                })   
        }
    },
    created(){
        this.fetchMostRecentBorrows();
    }

}
</script>