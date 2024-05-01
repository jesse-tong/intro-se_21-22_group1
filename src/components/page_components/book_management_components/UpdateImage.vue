<template>
    <div class="col max-width-vh-100">
        <img alt="" :src="newImage || '/image/' + $props.bookId || emptyImage" class="row-10"/>
        <input accept="image/*" type="file" @change="previewFiles($event)" class="row-1"/>
        <button class="btn btn-primary" @click="updateImage"><span>Update book image</span></button>
    </div>
    
    
</template>

<script>
    //The blank image is licensed under CC-BY-SA: https://commons.wikimedia.org/wiki/File:No-Image-Placeholder.svg
    import emptyImage from '@/src/assets/BlankImage.svg'; 
    export default {
        props: {
            bookId: {
                type: [Number, String],
                required: true
            }
        },
        data(){
            return {
                newImage: '',
                emptyImage,
                image: null,
                apiSite: 'http://localhost:5000'
            }
        },
        methods: {
            previewFiles(event) {

                const file = event.target.files[0];
                if (event.target.files.length >= 0){
                    this.image = event.target.files[0];
                }else {
                    this.image = null;
                }
                const uploadImageReader = new FileReader();

                theReader.onloadend = async () => {
                    this.newImage = uploadImageReader.result;
                };
                theReader.readAsDataURL(file);
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
                      title: "Register error",
                      text: "Register failed with error: " + response.data.error
                    })
                  }
                }).catch(err=>{
                  this.$notify({
                    title: "Register error",
                    text: "Register failed with error: "+ err.response.data.error,
                    type: "error"
                  })
                }).finally(()=>{
                    this.image = null;
                    this.newImage = '';
                })
                    
                }
            }
        }
    }
</script>