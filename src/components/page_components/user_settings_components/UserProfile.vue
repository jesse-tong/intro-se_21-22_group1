<template>
    <ImageUpdateModal :showModal="imageModalShow" @closeModal="imageModalShow = false" ref="updateImageModal" :userId="$props.userId !== null ? $props.userId : accountStore.userId" />
    <h5 class="section-title bg-light-subtle text-center text-primary px-3 mt-3">User Profile</h5>
    <div class="row ms-3 me-3">
        <div class="col-md-3 border-right">
            <div class=" wow fadeInUp" data-wow-delay="0.5s">
                <div class="team-item bg-light">
                    <div class="overflow-hidden">
                        <img class="img-fluid" style="aspect-ratio: 1/1;" :src="apiSite + '/api/profile_image/' + ($props.userId !== null ? $props.userId : accountStore.userId) + '?session=' + getRandomId || emptyImage" />
                    </div>
                    <div class="position-relative d-flex justify-content-center" style="margin-top: -23px;">
                        <div class="bg-light d-flex justify-content-center pt-2 px-1">
                            <a class="btn btn-sm-square btn-primary mx-1" :href="'mailto:' + (userInfo || userInfo.email ? userInfo.email : '')"><i class="bi bi-envelope-at"></i></a>
                            <router-link class="btn btn-sm-square btn-primary mx-1" role="button" title="User settings" alt="User settings"
                            to="/user/settings" v-if="$props.userId === null || accountStore.userId === $props.userId"><i class="bi bi-gear"></i></router-link>
                            <button class="btn btn-sm-square btn-primary mx-1" title="Change account image" alt="Change account image"
                             role="button" @click="imageModalShow = true" v-if="$props.userId === null || accountStore.userId === $props.userId"><i class="bi bi-image"></i></button>
                        </div>
                    </div>
                    <div class="text-center p-4 d-block">
                        <p class="font-weight-bold">{{ userInfo !== null ? userInfo.name : 'N/A' }}</p>
                        <p class="text-black-50">{{ userInfo !== null ? (userInfo.email !== null ? userInfo.email : 'N/A') : 'N/A' }}</p>
                    </div>
                </div>
            </div>
            <h5 class="section-title bg-light-subtle text-center text-primary px-3 me-3 mt-2 ">Send verification email</h5>
            <div class="ms-3 me-3" >
                <button class="btn btn-primary mb-2 mx-auto" @click="sendVerificationEmail"><span>Send verification email</span></button>
            </div>
        </div>
        <div class="col-12 col-md-4">
            <div class=" mb-2">
                <label for="userId" class="form-label"><span>User ID: </span></label>
                <input type="text" readonly aria-readonly="true" :value="userInfo !== null ? userInfo.userId : 'N/A' " class="form-control" id="userId"/>
            </div>
            <div class=" mb-2">
                <label for="userEmail" class="form-label"><span>Email: </span></label>
                <input type="text" readonly aria-readonly="true" :value="userInfo !== null ? userInfo.email : 'N/A'" class="form-control" id="userEmail"/>
            </div>
            <div class=" mb-2">
                <label for="userName" class="form-label"><span>Username: </span></label>
                <input type="text" readonly aria-readonly="true" :value="userInfo !== null ? userInfo.name : 'N/A'" class="form-control" id="userName"/>
            </div>
            <div class=" mb-2">
                <label for="userAddress" class="form-label"><span>Address: </span></label>
                <input type="text" readonly aria-readonly="true" :value="userInfo !== null ? userInfo.address : 'N/A'" class="form-control" id="userAddress"/>
            </div>
            
            <div class=" mb-2">
                <label for="userRole" class="form-label"><span>Account role: </span></label>
                <input type="text" readonly aria-readonly="true" :value="userInfo !== null ? userInfo.role : 'N/A'" class="form-control" id="userRole"/>
            </div>
            <div class=" mb-2">
                <label for="alternatePhone" class="form-label"><span>Alternate phone number: </span></label>
                <input type="text" readonly aria-readonly="true" :value="userInfo.alternatePhone ? userInfo.alternatePhone : 'N/A'" class="form-control" id="userRole"/>
            </div>
        </div>
        <div class="col-12 col-md-4">
            <div class=" mb-2">
                <label for="userAge" class="form-label"><span>Age: </span></label>
                <input type="text" readonly aria-readonly="true" :value="userInfo !== null ? userInfo.age : 'N/A'" class="form-control" id="userAge"/>
            </div>
            <div class="mb-2">
                <label for="userGender" class="form-label"><span>Gender: </span></label>
                <input type="text" readonly aria-readonly="true" :value="userInfo !== null ? (userInfo.gender ? userInfo.gender : 'Prefer not to say') : 'N/A' " class="form-control" id="userGender"/>
            </div>
            <div class=" mb-2">
                <label for="userPhoneNumber" class="form-label"><span>Phone number: </span></label>
                <input type="text" readonly aria-readonly="true" :value="userInfo !== null ? userInfo.phone: 'N/A'" class="form-control" id="userPhoneNumber"/>
            </div>
            <div class=" mb-2">
                <label for="isAccountVerified" class="form-label"><span>Is account verified: </span></label>
                <input type="text" readonly aria-readonly="true" :value="userInfo !== null ? userInfo.isVerified: 'N/A'" class="form-control" id="isAccountVerified"/>
            </div>
            <div class=" mb-2">
                <label for="alternateEmail" class="form-label"><span>Alternate email: </span></label>
                <input type="text" readonly aria-readonly="true" :value="userInfo.alternateEmail ? userInfo.alternateEmail : 'N/A'" class="form-control" id="alternateEmail"/>
            </div>
            <div class=" mb-2">
                <label for="zipCode" class="form-label"><span>Zip code: </span></label>
                <input type="text" readonly aria-readonly="true" :value="userInfo.zipCode ? userInfo.zipCode : 'N/A'" class="form-control" id="zipCode"/>
            </div>
            <!--<div class=" mb-2">
                <label for="userBorrowCount" class="form-label"><span>Borrow: </span></label>
                <input type="text" disabled :value="userInfo !== null ? (userInfo.borrowLeft + ' / ' + userInfo.maxBorrow) : 'N/A'" class="form-control" id="userBorrowCount"/>
            </div> -->
        </div>
    </div>
    
</template>
<script>
    import axios from 'axios';
    import { mapStores } from 'pinia';
    import { useAccountStore } from '../../stores/LoginInfoStore';
    import emptyImage from '../../../assets/BlankImage.svg';
    import ImageUpdateModal from './ImageUpdateModal.vue';
    import { v4 as uuidv4 } from 'uuid';

    
    export default {
        data(){
            return {
                userInfo: {
                    address: 'N/A',
                    age: 'N/A',
                    borrowLeft: 'N/A',
                    email: 'N/A',
                    gender: 'N/A',
                    email: 'N/A',
                    userId: 'N/A',
                    maxBorrow: 'N/A',
                    name: 'N/A',
                    phone: 'N/A',
                    role: 'N/A',
                    isVerified: 'N/A' 
                },
                emptyImage,
                imageModalShow: false
            }
        },
        components: {
            ImageUpdateModal
        },
        props: {
            userId: {
                type: [String, null],
                default: null
            }
        },
        created(){
            if (!this.accountStore.loggedIn){
                this.$router.push({ path: '/login', query: { error: 'You must log in first before update profile!' } });
            }
            document.title = "User profile";
        },
        computed: {
            ...mapStores(useAccountStore)
        },
        created(){
            this.getUserProfile();
        },
        methods: {
            sendVerificationEmail(){
                axios.post('/auth/send-verification-email/' + this.userInfo.id).then(response => {
                    if (response.data.success === true){
                        this.$notify({
                            title: "Send verification email successfully!",
                            text: "Send verification email successfully!",
                            type: "success"
                        });
                    }else {
                        this.$notify({
                            title: "Send verification email failed",
                            text: "Send verification email failed with error: " + response.data.error,
                            type: "error"
                        });
                    }
                }).catch(err=>{
                    this.$notify({
                        title: "Send verification email failed",
                        text: "Send verification email failed with error: "+ err.response.data.error,
                        type: "error"
                    });
                });
            },
            getUserProfile(){
                //Default will get current logged user profile userId prop is null
                axios.get('/auth/profile' + (this.$props.userId !== null ? '/' + this.$props.userId : '')).then(response => {
                  if (response.data.success === true){    
                    this.userInfo = response.data.result;
                  }else {
                    this.$notify({
                      title: "Fetch user information failed",
                      text: "Fetch user information failed with error: " + response.data.error,
                      type: "error"
                    })
                  }
                }).catch(err=>{
                  this.$notify({
                    title: "Fetch user information failed",
                    text: "Fetch user information failed with error: "+ err.response.data.error,
                    type: "error"
                  })
                })
            }
        },
        computed: {
            ...mapStores(useAccountStore),
            getRandomId(){
                return uuidv4();
            }
        },
        
    }
</script>