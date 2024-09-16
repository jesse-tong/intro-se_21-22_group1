<template>
<div class="row shadow-sm" style="width: 96%; max-height: 400px; margin: 18px 2% 15px 2%; border-radius: 12px;" 
v-if="$props.events && $props.events.length > 0">
    <div :class="['col-12', 'd-flex', 'g-0', $props.events.length >= 3 ? 'col-lg-8' : 'col-lg-12']" >
        <img class="" style="width: 50%; height: 100%; border-top-left-radius: 12px; border-bottom-left-radius: 12px" 
        :src="$props.events[0].thumbnail" :alt="'Image for artitle with title: ' + $props.events[0].title" @error="($event) => setAltImg($event)"/>
        <div style="width: 50%; height: 100%; background-color: #34ebcf;" class="right-border">
            <div class="m-auto px-3 py-4">
                <router-link :to="'/article/' + $props.events[0].id" class="text-decoration-none">
                    <h2 class="text-white">{{ $props.events[0].title }}</h2>
                </router-link>
                <p class="text-white mt-3" v-if="$props.events[0].note"><small>{{ $props.events[0].note }}</small></p>
            </div>
        </div>
    </div>
    <div class="col-12 col-lg-4 g-0 d-none d-lg-block" v-if="$props.events.length >= 3">
        <div class="col">
            <div class="row-6 d-flex align-items-stretch">
                <img class="align-self-stretch" style="width: 50%; border-left: 2px solid white;" :src="$props.events[1].thumbnail" :alt="'Image for artitle with title: ' + $props.events[1].title" @error="($event) => setAltImgSmall($event)"/>
                <div style="width: 50%; background-color: #34ebcf; border-top-right-radius: 12px; border-bottom: 1px solid white;" class=" px-3 py-2">
                    <div class="m-auto">
                        <router-link :to="'/article/' + $props.events[1].id" class="text-decoration-none">
                            <h5 class="text-white">{{ $props.events[1].title }}</h5>
                        </router-link>
                        <p class="text-white mt-3" v-if="$props.events[1].note"><small>{{ $props.events[1].note }}</small></p>
                    </div>
                </div>
            </div>
            <div class="row-6 d-flex align-items-stretch">
                <img class="align-self-stretch" style="width: 50%; border-left: 2px solid white;" :src="$props.events[2].thumbnail" :alt="'Image for artitle with title: ' + $props.events[2].title" @error="($event) => setAltImgSmall($event)"/>
                <div style="width: 50%; background-color: #34ebcf; border-bottom-right-radius: 12px; border-top: 1px solid white;" class="align-self-stretch px-3 py-2">
                    <div class="m-auto">
                        <router-link :to="'/article/' + $props.events[2].id" class="text-decoration-none">
                            <h5 class="text-white">{{ $props.events[2].title }}</h5>
                        </router-link>
                        <p class="text-white mt-3" v-if="$props.events[2].note"><small>{{ $props.events[2].note }}</small></p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

</template>
<script>
import EmptyImage from '../../../assets/empty_image.png';
export default {
    methods: {
        setAltImg(e) {
            e.target.onerror = null;
            e.target.src = EmptyImage;
            e.target.style.backgroundImage = 'linear-gradient(90deg, #06BBCC, #34ebcf)';
            e.target.alt = 'Image not found';
            e.target.title = 'Image not found';
        },
        setAltImgSmall(e){
            e.target.onerror = null;
            e.target.src = EmptyImage;
            e.target.style.backgroundImage = 'linear-gradient(90deg, #16dbcc, #34ebcf)';
            e.target.alt = 'Image not found';
            e.target.title = 'Image not found';
        }
    },
    created() {
        console.log(this.$props.events);
    },
    props: {
        events: {
            type: Array,
            required: true,
        }
    }
}

</script>

<style scoped lang="css">
@media (max-width: 992px) {
    .right-border {
        border-top-right-radius: 12px;
        border-bottom-right-radius: 12px;
    }
}
</style>