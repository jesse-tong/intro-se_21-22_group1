<template>
    <div class="mx-2 mt-3">
        <div class="row">
            <div class="col-12 col-md-9 col-xl-9 col-xxl-8">
                <ImageList :images="images" @update:currentPage="(page) => { currentPage = page }" :currentPage="currentPage" 
                    @deleteImage="onDeleteImage" @selectImage="onSelectImage" @selectThumbnail="onSelectImageThumbnail"/>
            </div>
            <div class="col-12 col-md-3 col-xl-3 col-xxl-4 border-md-start">
                <div class="ps-3 ps-md-1 pe-1 col">
                    <input accept="image/*" type="file" @change="onFileChange($event)" class="form-control row" ref="imageInput"/>
                    <button class="btn btn-primary row my-2" @click="onUploadImage"><span>Upload image</span></button>
                    <button class="btn btn-primary row" @click="(e) => removeImage()"><span>Remove pending upload image</span></button>
                </div>
            </div>
        </div>     
    </div>   
</template>
<script>
    import axios from 'axios';
    import ImageList from './ImageList.vue';

    export default {
        data(){
            return {
                images: [],
                currentPage: 1,

                uploadImage: ''
            }
        },
        components: {
            ImageList: ImageList,
        },
        watch: {
            currentPage: {
                handler(newCurrentPage){
                    this.fetchUploadedImages(newCurrentPage);
                },
                immediate: true
            },
            
        },
        methods: {
            onFileChange(e) {
                var files = e.target.files || e.dataTransfer.files;
                if (!files.length)
                    return;
                this.createImage(files[0]);
            },
            createImage(file) {
                /*var image = new Image();
                var reader = new FileReader();

                reader.onload = (e) => {
                    this.uploadImage = e.target.result;
                };
                reader.readAsDataURL(file);*/
                this.uploadImage = file;
            },
            removeImage: function (e) {
                this.uploadImage = null;
                this.$refs.imageInput.value = null;
            },
            fetchUploadedImages(page){
                axios.get('/api/upload-user-image', {params: { page: page, limit: 6} })
                .then(response => {
                    if (response.data !== undefined && response.data.success === true){
                        this.images = response.data.result;
                    }else if (response.data.success === false){
                        this.$notify({
                            title: 'Fetching your image list at page ' + page + ' failed',
                            text: 'Fetching your image list at page ' + page + ' failed with error: ' + response.data.error,
                            type: 'error'
                        });
                    }
                }).catch(err => {
                    if (err.response){
                        if (err.response.data && err.response.data.error){
                            this.$notify({
                                title: 'Fetching your image list at page ' + page + ' failed',
                                text: 'Fetching your image list at page ' + page + ' failed with error: ' + err.response.data.error,
                                type: 'error'
                            });
                        }else {
                            this.$notify({
                                title: 'Fetching your image list at page' + page + ' failed',
                                text: 'Fetching your image list failed with unknown error',
                                type: 'error'
                            });
                        }
                    }
                })
            },
            onUploadImage(){
                axios.postForm('/api/upload-user-image', { file: this.uploadImage })
                .then(response => {
                    if (response.data !== undefined && response.data.success === true){
                        this.$notify({
                            title: 'Upload new image successfully!' ,
                            text: 'Upload new image with ID' + response.data.response.id + 'successfully!',
                            type: 'success'
                        });
                    }else if (response.data.success === false){
                        this.$notify({
                            title: 'Upload new image failed!',
                            text: 'Upload new image failed with error: ' + response.data.error,
                            type: 'error'
                        });
                    }
                }).catch(err => {
                    if (err.response){
                        if (err.response.data && err.response.data.error){
                            this.$notify({
                                title: 'Upload new image failed!',
                                text: 'Upload new image failed with error: ' + err.response.data.error,
                                type: 'error'
                            });
                        }else {
                            this.$notify({
                                title: 'Upload new image failed',
                                text: 'Upload new image failed with unknown error',
                                type: 'error'
                            });
                        }
                    }
                }).finally(() => { 
                    this.fetchUploadedImages(this.currentPage); 
                    this.removeImage();
                });
            },
            onDeleteImage(imageId){
                axios.delete('/api/upload-user-image/' + imageId)
                .then(response => {
                    if (response.data !== undefined && response.data.success === true){
                        this.$notify({
                            title: 'Deleting image with ID ' + imageId + ' successfully!' ,
                            text: 'Deleting image with ID ' + imageId + ' successfully!',
                            type: 'success'
                        });
                    }else if (response.data.success === false){
                        this.$notify({
                            title: 'Error deleting image with ID ' + imageId + ' failed',
                            text: 'Error deleting image: ' + response.data.error,
                            type: 'error'
                        });
                    }
                }).catch(err => {
                    if (err.response){
                        if (err.response.data && err.response.data.error){
                            this.$notify({
                                title: 'Deleting image with ID ' + articleId + ' failed',
                                text: 'Error deleting image: ' + err.response.data.error,
                                type: 'error'
                            });
                        }else {
                            this.$notify({
                                title: 'Deleting image with ID ' + articleId + ' failed',
                                text: 'Deleting image failed with unknown error',
                                type: 'error'
                            });
                        }
                    }
                }).finally(() => { 
                    this.fetchUploadedImages(this.currentPage); 
                    this.removeImage();
                });
            },
            onSelectImage({id, fileName}){
                this.$emit('selectImage', '![' + fileName + '](' + this.apiSite + '/uploaded-image/' + id + ' "' + fileName + '")');
            },
            onSelectImageThumbnail({id, fileName}){
                this.$emit('selectImageThumbnail', this.apiSite + '/uploaded-image/' + id);
            }
            
        },
        emits: ['selectImage']
    }
</script>