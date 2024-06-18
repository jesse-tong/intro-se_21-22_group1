<template>
    <div class="modal" tabindex="-1" ref="modal" id="borrowModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Borrow book</h5>
            <button type="button" class="btn-close" data-bs-toggle="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="form-floating">
                <input class="form-control" type="number" id="borrowBookIdInput" v-model.number="borrowBookId" >
                <label for="borrowBookIdInput">Book ID</label>
            </div>

            <div class="form-floating mt-3">
                <input type="number" class="form-control" v-model.number="endBorrow" id="endBorrowDateInput" min="0" max="30"/>
                <label for="endBorrowDateInput"><span>Day to return book/material from today (max 30 days)</span></label>
            </div>
            <div>
                <span class="mt-2"><b>Start borrow date:</b> {{ getStartBorrowDate }}</span>
            </div>
            <div>
                <span class=""><b>End borrow date:</b> {{ getEndBorrowDate }}</span>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary"  @click="(e)=>hideModal()">Close</button>
            <button type="button" class="btn btn-primary" @click="(e)=>onBookBorrow()">Borrow book</button>
          </div>
        </div>
      </div>
    </div>
    </template>
    
<script>
    import axios from 'axios';
    import { Modal } from 'bootstrap';
    
        export default {
            props: {
                bookId: {
                    type: [Number, null],
                    required: false,
                    default: null
                },
                showModal: {
                    type: Boolean,
                    default: false
                }
            },
            data(){
                return{
                    endBorrow: 14,
                    borrowBookId: this.$props.bookId,
                    modalInstance: null,
                }
                
            },
            watch: {
                showModal(newValue, oldValue) {
                    if (newValue === true) {
                        this.modalActive();
                    }
                }
            },
            methods: {
                onBookBorrow(){
                    let today = new Date();
                    
                    let borrowParams = {};
                    if (this.endBorrow >=0 && this.endBorrow !== null){
                        let endBorrowDate = new Date();
                        endBorrowDate = endBorrowDate.setDate(today.getDate() + this.endBorrow);
                        endBorrowDate = new Date(endBorrowDate).setHours(23, 59, 59);
                        borrowParams.end_borrow = new Date(endBorrowDate).toISOString();        
                    }else {
                        this.$notify({
                            title: "Invalid date",
                            text: "Invalid date interval, check again.",
                            type: "error"
                        });
                        return;
                    }
                    borrowParams.start_borrow = today.toISOString();
                    borrowParams.book_id = this.borrowBookId;
                    axios.postForm('/api/borrow', borrowParams ).then(response => {
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
                            title: "Borrow book request sent successfully!",
                            text: "You have sent a request to borrow the book with ID " + response.data.result.bookId 
                            + " successfully with end borrow date " + response.data.result.endBorrow + " and borrow ID: " + response.data.result.id,
                            type: "success"
                            });
                        }else {
                            this.$notify({
                            title: "Borrow book request sent failed",
                            text: "Borrow book request sent failed with error: " + response.data.error,
                            type: "error"
                            });
                            return;
                        }
                    }).catch(err=>{
                        this.$notify({
                            title: "Borrow book request sent failed",
                            text: "Borrow book request sent failed with error: " + err.response.data.error,
                            type: "error"
                        });
                        return;
                    }).finally(()=>{
                        this.$emit('update:borrowList');
                        
                    })
                },
                modalActive: function () {
                    this.modalInstance = new Modal(document.getElementById('borrowModal'), {
                        target: "#borrowModal",
                        backdrop: "static"
                    });
                    this.modalInstance.show();
                },
                hideModal: function () {
                    this.modalInstance.hide();
                    this.$emit('closeModal');
                }
            },
            computed: {
                getEndBorrowDate(){
                    let today = new Date();
                    if (this.endBorrow !== null){
                        let endBorrowDate = new Date();
                        endBorrowDate = endBorrowDate.setDate(today.getDate() + this.endBorrow);
                        endBorrowDate = new Date(endBorrowDate).setHours(23, 59, 59);
                        return new Date(endBorrowDate).toString();  
                    }else {
                        return 'Invalid date string';
                    }
                },
                getStartBorrowDate(){
                    let today = new Date();
                    return today.toString()
                }
            },
            emits: ['update:borrowList', 'closeModal']
        }
    </script>