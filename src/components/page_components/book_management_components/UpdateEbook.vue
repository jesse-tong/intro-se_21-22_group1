<template>
    <div class="col mt-3">
        <h4 class="row-1">Update ebook (accept PDF):</h4>
        <span>Uploaded ebook: {{ uploadedEbookFileName !== null ? uploadedEbookFileName : 'None' }}</span>
        <input accept="application/pdf" type="file" @change="setEbookFile($event)" class="row-1 my-2 ms-2 ms-lg-0"/>
        <button class="btn btn-primary row ms-1" @click="updateEbook"><span>Update ebook</span></button>
    </div>
 
</template>

<script>
   
    import axios from 'axios';
    export default {
        props: {
            bookId: {
                type: [Number, String],
                required: true
            }
        },
        data(){
            return {
                ebookFile: null,
                uploadedEbookFileName: null
                
            }
        },
        methods: {
            checkUploadedEbookFileName(){
                axios.get('/api/upload-ebook/' + this.$props.bookId).then(response => {
                    if (response.data !== undefined 
                    && response.data.result !== undefined && response.data.result !== null){
                        this.uploadedEbookFileName = response.data.result.fileSrc;
                    }
                })
            },
            setEmptyImage(){
                this.newImage = this.emptyImage;
            },
            setEbookFile(event) {

                const file = event.target.files[0];
                if (event.target.files.length >= 0){
                    this.ebookFile = file;
                }else {
                    this.ebookFile = null;
                }
                
            },
            updateEbook(){
                if (this.ebookFile === null){
                    this.$notify({
                        title: "No file selected!",
                        text: "No file selected",
                        type: "error"
                    });
                    return;
                }else {
                    axios.postForm('/api/upload-ebook/' + this.$props.bookId, {
                        ebook: this.ebookFile
                    }).then(response => {
                  if (response.data.success === true){    
                    this.$notify({
                        title: "Update ebook successfully",
                        text: "Update ebook successfully!",
                        type: "success"
                    });
                  }else {
                    this.$notify({
                      title: "Update ebook failed",
                      text: "Update ebook failed with error: " + response.data.error
                    });
                    this.$emit('updateEditBookData')
                  }
                }).catch(err=>{
                  this.$notify({
                    title: "Update ebook failed",
                    text: "Update ebook failed with error: "+ err.response.data.error,
                    type: "error"
                  })
                }).finally(()=>{
                    this.ebookFile = null;
                    
                })
                    
                }
            }
        },
        created(){
            this.checkUploadedEbookFileName();
        }, 
        emits: ['updateEditBookData']
    }
</script>