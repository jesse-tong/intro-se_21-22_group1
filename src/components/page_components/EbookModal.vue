<template>
    <div class="modal" tabindex="-1" ref="modal" id="ebookModal">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Reading ebook</h5>
            <button type="button" class="btn-close" data-bs-toggle="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <PDFViewer :pdf="apiSite + '/ebook/' + bookId" />
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary"  @click="(e)=>hideModal()">Close</button>
          </div>
        </div>
      </div>
    </div>
    </template>
    
<script>
    import PDFViewer from './PDFViewer.vue';
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
            components: {
                PDFViewer: PDFViewer
            },
            data(){
                return{
                    endBorrow: 1,
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
                
                modalActive: function () {
                    this.modalInstance = new Modal(document.getElementById('ebookModal'), {
                        target: "#borrowModal",
                        backdrop: "static"
                    });
                    this.modalInstance.show();
                },
                hideModal: function () {
                    this.modalInstance.hide();
                    this.$emit('closeEbookModal');
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
            emits: ['closeEbookModal']
        }
    </script>