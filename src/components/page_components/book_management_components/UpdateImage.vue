<template>
    <div class="col max-width-vh-100 mt-3 border-2 rounded">
        <h4 class="row-1">Update image:</h4>
        <img alt="" :src="newImage" class="row-9" @error="setEmptyImage" style="max-width: 100%; max-height: 100vh;" v-if="newImage !== null && newImage !== ''"/>
        <img alt="" :src="apiSite + '/image/' + $props.bookId + '?id=' + getRandomUuid || emptyImage" class="row-9" @error="setEmptyImage" style="max-width: 100%; max-height: 100vh;" v-else/>
        <input accept="image/*" type="file" @change="previewFiles($event)" class="row-1 my-2 ms-2 ms-lg-0"/>
        <button class="btn btn-primary row" @click="updateImage"><span>Update book image</span></button>
    </div>
</template>

<script>
    //The blank image is licensed under CC-BY-SA: https://commons.wikimedia.org/wiki/File:No-Image-Placeholder.svg
    import emptyImage from '../../../assets/BlankImage.svg'; 
    import axios from 'axios';
    import { v4 as uuidv4 } from 'uuid';
    export default {
        props: {
            bookId: {
                type: [Number, String],
                required: true
            }
        },
        data(){
            return {
                newImage: null,
                emptyImage,
                image: null,
                
            }
        },
        computed: {
            getRandomUuid(){
                return uuidv4();
            }
        },
        methods: {
            setEmptyImage(){
                this.newImage = this.emptyImage;
            },
            previewFiles(event) {

                const file = event.target.files[0];
                if (event.target.files.length >= 0){
                    this.image = event.target.files[0];
                }else {
                    this.image = null;
                }
                const uploadImageReader = new FileReader();

                uploadImageReader.onloadend = async () => {
                    this.newImage = uploadImageReader.result;
                };
                uploadImageReader.readAsDataURL(file);
            },
            updateImage(){
                if (this.image === null){
                    this.$notify({
                        title: "No file selected!",
                        text: "No file selected",
                        type: "error"
                    });
                    return;
                }else {
                    axios.postForm('/api/upload-image/' + this.$props.bookId, {
                        image: this.image
                    }).then(response => {
                  if (response.data.success === true){    
                    this.$notify({
                        title: "Update book image successfully",
                        text: "Update book image successfully!",
                        type: "success"
                    });
                  }else {
                    this.$notify({
                      title: "Update image of book failed",
                      text: "Update image of book failed with error: " + response.data.error
                    });
                    this.$emit('updateEditBookData')
                  }
                }).catch(err=>{
                  this.$notify({
                    title: "Update image of book failed",
                    text: "Update image of book failed with error: "+ err.response.data.error,
                    type: "error"
                  })
                }).finally(()=>{
                    this.image = null;
                    this.newImage = '';
                })
                    
                }
            }
        },
        emits: ['updateEditBookData']
    }
</script>