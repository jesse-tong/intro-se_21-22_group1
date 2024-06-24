<template>
    <div class="modal" tabindex="-1" ref="modal" id="updateUserImageModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Update user profile image:</h5>
            <button type="button" class="btn-close" @click="(e)=>hideModal()"></button>
          </div>
          <div class="modal-body">
            <p class="row-1">Update user profile image:</p>
            <img alt="" :src="newImage" class="row-9" @error="setEmptyImage" style="max-width: 300px; max-height: 100vh;" v-if="newImage !== null && newImage !== ''"/>
            <img alt="" :src="apiSite + '/image/' + $props.bookId || emptyImage" class="row-9" @error="setEmptyImage" style="max-height: 100%;" v-else/>
            <input accept="image/*" type="file" @change="previewFiles($event)" class="row-1 my-2 ms-2 ms-lg-0"/>
            <button class="btn btn-primary row" @click="updateImage"><span>Update profile image</span></button>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary"  @click="(e)=>hideModal()">Close</button>
          </div>
        </div>
      </div>
    </div>
    </template>
    
<script>
    import axios from 'axios';
    import { Modal } from 'bootstrap';
    import emptyImage from '../../../assets/BlankImage.svg';
    
        export default {
            props: {
                userId: {
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
                    newImage: null,
                    emptyImage,
                    image: null,
                    
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
                        axios.postForm('/api/profile_image/' + this.$props.userId, {
                            user_image: this.image
                        }).then(response => {
                    if (response.data.success === true){    
                        this.$notify({
                            title: "Update user profile image successfully",
                            text: "Update user profile image successfully!",
                            type: "success"
                        });
                    }else {
                        this.$notify({
                        title: "Update user profile image failed",
                        text: "Update user profile image failed with error: " + response.data.error
                        });
                        this.$emit('updateEditBookData')
                    }
                    }).catch(err=>{
                    this.$notify({
                        title: "Update user profile image failed",
                        text: "Update user profile image failed with error: "+ err.response.data.error,
                        type: "error"
                    })
                    }).finally(()=>{
                        this.image = null;
                        this.newImage = '';
                    })
                        
                    }
                },
                modalActive: function () {
                    this.modalInstance = new Modal(document.getElementById('updateUserImageModal'), {
                        target: "#updateUserImageModal",
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
                
            },
            emits: ['closeModal']
        }
    </script>