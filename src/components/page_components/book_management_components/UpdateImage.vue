<template>
    <input accept="image/*" type="file" @change="previewFiles($event)" />
    <img alt="" :src="newImage || emptyImage" @error="" />
</template>

<script>
    //The blank image is licensed under CC-BY-SA: https://commons.wikimedia.org/wiki/File:No-Image-Placeholder.svg
    import emptyImage from '@/src/assets/BlankImage.svg'; 
    export default {
        data(){
            return {
                newImage: '',
                emptyImage
            }
        },
        methods: {
            previewFiles(event) {
            const file = event.target.files[0];

            const uploadImageReader = new FileReader();

            theReader.onloadend = async () => {
                this.newImage = await uploadImageReader.result;
            };
            theReader.readAsDataURL(file);
            }
        }
    }
</script>