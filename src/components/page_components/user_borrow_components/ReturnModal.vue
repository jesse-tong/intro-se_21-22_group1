<template>
<div class="modal" tabindex="-1" ref="modal" id="returnModal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Return Book</h5>
        <button type="button" class="btn-close" data-bs-toggle="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <div class="form-floating">
            <input type="datetime-local" class="form-control" v-model="returnDate"/>
            <label for="returnDateInput"><span>Return date</span></label>
        </div>
        <div class="form-check form-switch">
            <input class="form-check-input" type="checkbox" role="switch" id="damagedOrLostChecked" v-model="isDamagedOrLost">
            <label class="form-check-label" for="damagedOrLostChecked">Is the book damaged/lost</label>
        </div>

      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="(e)=>onCloseModal()">Close</button>
        <button type="button" class="btn btn-primary" @click="(e)=>onReturnBook()">Return book</button>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import axios from 'axios';

    export default {
        props: {
            borrowId: {
                type: Number,
                required: true
            }
        },
        data(){
            return{
                returnDate: '',
                isDamagedOrLost: false,
            }
            
        },
        methods: {
            convertLocalDatetimeToISOString(localDatetimeString){
                //Since the value of <input type="datetime-local" /> is always YYYY-mm-ddThh:ss
                //and does not denotes any timezone, so parse it with new Date() and use toISOString() method will not work correctly
                let timeWithTimezone = new Date(localDatetimeString);
                return timeWithTimezone.toISOString();
            },
            onReturnBook(){
                let returnParams = {};
                if (this.returnDate !== '' && this.returnDate !== null){
                    returnParams.return_date = this.convertLocalDatetimeToISOString(this.returnDate);        
                }
                returnParams.damaged_or_lost = this.isDamagedOrLost;
                axios.get('/api/return/' + this.$props.borrowId, {
                    params: returnParams
                }).then(response => {
                    if (!response.data || response.data.success == undefined){
                        this.$notify({
                        title: "Unknown error",
                        text: "Unknown error, this can be server or network error.",
                        type: "error"
                        });
                        return;
                    }
                    
                    if (response.data.success === true){
                        this.$notify({
                        title: "Return book successfully!",
                        text: "You have returned the book with ID " + response.data.result.bookId + " successfully at " + response.data.result.returnDate,
                        type: "success"
                        });
                    }else {
                        this.$notify({
                        title: "Fetch borrow your borrow list error",
                        text: "Fetch borrow your borrow list error: " + response.data.error,
                        type: "error"
                        });
                        return;
                    }
                }).catch(err=>{
                    this.$notify({
                        title: "Fetch borrow your borrow list error",
                        text: "Fetch borrow your borrow list error: " + err.response.data.error,
                        type: "error"
                    });
                    return;
                }).finally(()=>{
                    this.$emit('update:borrowList')
                })
            },
            onCloseModal(){
                this.returnDate = '';
                this.isDamagedOrLost = false;
            },
            openModal(){
                this.$refs.modal.show();
            }
        },
        emits: ['update:borrowList']
    }
</script>