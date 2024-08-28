<template>
    <h4 class="ms-4 me-3" style="margin-top: 3.8rem">Borrow policies</h4>
    <div class="row ms-3 me-3">
        <div class="col-12 col-md-6 col-lg-4 mb-2">
            <label for="overdueFine" class="form-label"><span>Overdue fine (per day): </span></label>
            <input type="number" min="0" class="form-control" id="overdueFine" v-model.number="overdueFine"/>
        </div>
        <div class="col-12 col-md-6 col-lg-4 mb-2">
            <label for="overdueLimit" class="form-label"><span>Overdue limit (before the borrow is treated as lost) </span></label>
            <input type="number" min="0" class="form-control" id="overdueLimit" v-model.number="overdueLimit"/>
        </div>
        <div class="col-12 col-md-6 col-lg-4 mb-2">
            <label for="damageAndLostFine" class="form-label"><span>Irrecoverable damage/lost book fine: </span></label>
            <input type="number" min="0" class="form-control" id="damageAndLostFine" v-model.number="damageAndLostFine"/>
        </div>
        <div class="col mb-2">
            <label for="currency" class="form-label"><span>Currency: </span></label>
            <select class="form-select" id="currency" v-model="currency">
                <option value="USD">US Dollar (USD)</option>
                <option value="EUR">Euro (EUR)</option>
                <option value="JPY">Japanese Yen (JPY)</option>
                <option value="GBP">British Pound (GBP)</option>
                <option value="AUD">Australian Dollar (AUD)</option>
                <option value="CAD">Canadian Dollar (CAD)</option>
                <option value="CHF">Swiss Franc (CHF)</option>
                <option value="CNY">Chinese Yuan (CNY)</option>
                <option value="SEK">Swedish Krona (SEK)</option>
                <option value="NZD">New Zealand Dollar (NZD)</option>
                <option value="SGD">Singapore Dollar (SGD)</option>
                <option value="MXN">Mexican Peso (MXN)</option>
                <option value="BRL">Brazilian Real (BRL)</option>
                <option value="INR">Indian Rupee (INR)</option>
                <option value="RUB">Russian Ruble (RUB)</option>
                <option value="VND">Vietnamese Dong (VND)</option>
            </select>
        </div>
        <div class="col-12 mt-3">
            <p class="form-text">Enter other policy text (such as other borrow policies, data policies, policies when using library,...) here</p>
            <MdEditor v-model="libraryPolicyText" :language="en-US" :codeTheme="a11y" :noMermaid="true" :noKatex="true"/>
        </div>
        <div class="col-12 mt-2">
            <button @click="updateBorrowSettings" class="mb-2 btn btn-success"><span>Update borrow policies</span></button>
        </div>
        
    </div>
    <h4 class="ms-4 me-3 mt-3 ">Library timings</h4>
    <div class="row ms-3 me-3">
        <div class="col-12 col-md-6 col-xl-3 mb-2">
            <label for="normalDayOpen" class="form-label"><span>Normal day open time: </span></label>
            <input type="time" step="60" class="form-control" id="normalDayOpen" v-model="normalDayOpen"/>
            
        </div>
        <div class="col-12 col-md-6 col-xl-3 mb-2">
            <label for="normalDayClose" class="form-label"><span>Normal day close time: </span></label>
            <input type="time" step="60" class="form-control" id="normalDayClose" v-model="normalDayClose"/>
            
        </div>
        <div class="col-12 col-md-6 col-xl-3 mb-2">
            <label for="weekendOpen" class="form-label"><span>Weekend open time: </span></label>
            <input type="time" step="60" class="form-control" id="weekendOpen" v-model="weekendOpen"/>    
        </div>

        <div class="col-12 col-md-6 col-xl-3 mb-2">
            <label for="weekendClose" class="form-label"><span>Weekend close time: </span></label>
            <input type="time" step="60" class="form-control" id="weekendClose" v-model="weekendClose"/>    
        </div>

        <div class="col-12 col-md-6">
            <label for="weekendStart" class="form-label"><span>Weekend start at: </span></label>
            <select class="form-select" id="weekendStart" v-model.number="weekendStart">
                <option :value="index + 2" v-for="(dayName, index) in daysOfWeek">{{ dayName }}</option>
            </select>
        </div>
        <div class="col-12 col-md-6">
            <label for="weekendEnd" class="form-label"><span>Weekend end at: </span></label>
            <select class="form-select" id="weekendEnd" v-model.number="weekendEnd">
                <option :value="index + 2" v-for="(dayName, index) in daysOfWeek">{{ dayName }}</option>
            </select>
        </div>
        
        <div class="col-12 mt-2">
            <button @click="updateLibraryTimings" class="mb-2 btn btn-success"><span>Update library timings</span></button>
        </div>
        
    </div>

    <h4 class="ms-4 me-3 mt-2 ">Contact information</h4>
    <div class="row ms-3 me-3">
        <div class="col-12 col-xl-6 mb-2">
            <label for="contactEmail" class="form-label"><span>Contact email </span></label>
            <input type="text" class="form-control" id="contactEmail" v-model="contactEmail"/>
            <div class="form-check">
                <input class="form-check-input" type="checkbox" v-model="notUpdateContactEmail" id="notUpdateContactEmail">
                <label for="notUpdateContactEmail" class="form-check-label"><span>Not updating contact email</span></label>
            </div>
        </div>
        <div class="col-12 col-xl-6 mb-2">
            <label for="contactAddress" class="form-label"><span>Contact address </span></label>
            <input type="text" class="form-control" id="contactAddress" v-model="contactAddress"/>
            <div class="form-check">
                <input class="form-check-input" type="checkbox" v-model="notUpdateContactAddress" id="notUpdateContactAddress">
                <label for="notUpdateContactAddress" class="form-check-label"><span>Not updating contact address</span></label>
            </div>
        </div>
        <div class="col-12 col-xl-6 mb-2">
            <label for="contactPhoneNumber" class="form-label"><span>Contact phone number: </span></label>
            <input type="text" class="form-control" id="contactPhoneNumber" v-model="contactPhoneNumber"/>
            <div class="form-check">
                <input class="form-check-input" type="checkbox" v-model="notUpdateContactPhoneNumber" id="notUpdateContactPhoneNumber">
                <label for="notUpdateContactPhoneNumber" class="form-check-label"><span>Not updating contact phone number</span></label>
            </div>
        </div>
        
        <div class="col-12 mt-2">
            <button @click="updateContacts" class="mb-2 btn btn-success"><span>Update contacts</span></button>
        </div>
        
    </div>
</template>
<script>
    import axios from 'axios';
    import { MdEditor } from 'md-editor-v3';
    import 'md-editor-v3/lib/style.css';
    export default {
        data(){
            return {
                overdueFine: null,
                overdueLimit: null,
                damageAndLostFine: null,
                currency: null,
                libraryPolicyText: '',

                contactEmail: '',
                contactPhoneNumber: '',
                contactAddress: '',
                notUpdateContactEmail: false,
                notUpdateContactAddress: false,
                notUpdateContactPhoneNumber: false,

                normalDayOpen: null,
                normalDayClose: null,
                weekendOpen: null,
                weekendClose: null,
                weekendStart: null,
                weekendEnd: null,

            } 
        },
        components: {
            MdEditor: MdEditor
        },
        methods: {
            getBorrowSettings(){
                axios.get('/api/borrow-policies').then(response => {
                  if (response.data != undefined && response.data.success != undefined && response.data.success === true){    
                    this.overdueFine = response.data.result.overdue_fine;
                    this.overdueLimit = response.data.result.overdue_time_limit;
                    this.damageAndLostFine = response.data.result.damage_and_lost_fine;
                    this.currency = response.data.result.currency;
                    this.libraryPolicyText = response.data.result.other_policies;
                  }else {
                    this.$notify({
                      title: "Get current borrow settings failed",
                      text: "Get current borrow settings failed",
                      type: "error"
                    });
                  }
                }).catch(err=> {
                    this.$notify({
                      title: "Get current borrow settings failed",
                      text: "Get current borrow settings failed",
                      type: "error"
                    });
                })
            },
            updateBorrowSettings(){
                var borrowSettings = {}
                if (this.overdueFine == undefined  || parseFloat(this.overdueFine) < 0){
                    this.$notify({
                      title: "Invalid overdue fine",
                      text: "Invalid overdue fine",
                      type: "warning"
                    });
                    return;
                }else if (this.overdueFine == null || this.overdueFine == ''){
                    borrowSettings.overdue_fine = null;
                }else {
                    borrowSettings.overdue_fine = parseFloat(this.overdueFine);
                }

                if (this.overdueLimit == undefined  || parseInt(this.overdueLimit) < 0){
                    this.$notify({
                      title: "Invalid overdue limit",
                      text: "Invalid overdue limit",
                      type: "warning"
                    });
                    return;
                }else if (this.overdueLimit == null || this.overdueLimit == ''){
                    borrowSettings.overdue_limit = null;
                }else {
                    borrowSettings.overdue_limit = parseInt(this.overdueLimit);
                }

                if (this.damageAndLostFine == undefined  || parseInt(this.damageAndLostFine) < 0){
                    this.$notify({
                      title: "Invalid damaged/lost fine",
                      text: "Invalid damaged/lost fine",
                      type: "warning"
                    });
                    return;
                }else if (this.damageAndLostFine == null || this.damageAndLostFine == ''){
                    borrowSettings.damage_and_lost_fine = null;
                }else {
                    borrowSettings.damage_and_lost_fine = parseFloat(this.damageAndLostFine);
                }

                borrowSettings.currency = this.currency;
                borrowSettings.other_policies = this.libraryPolicyText;

                axios.postForm('/api/borrow-policies', borrowSettings).then(response => {
                    if (response.data != undefined && response.data.success != undefined 
                    && response.data !== null && response.data.success === true){
                        this.$notify({
                            title: "Update borrow policies successfully!",
                            text: "Update borrow policies successfully!",
                            type: "success"
                        });
                    }else {
                        this.$notify({
                            title: "Update borrow policies failed!",
                            text: "Update borrow policies failed!",
                            type: "error"
                        });
                    }
                }).catch(err => {
                    this.$notify({
                            title: "Update borrow policies failed!",
                            text: "Update borrow policies failed!",
                            type: "error"
                    });
                })
            },
            getContacts(){
                axios.get('/api/contacts').then(response => {
                  if (response.data.success === true){    
                    this.contactAddress = response.data.result.address;
                    this.contactEmail = response.data.result.email;
                    this.contactPhoneNumber = response.data.result.phone_number;
                  }else {
                    this.$notify({
                      title: "Get contacts failed",
                      text: "Get contacts failed",
                      type: "error"
                    });
                  }
                }).catch(err=>{
                    this.$notify({
                      title: "Get contacts failed",
                      text: "Get contacts failed",
                      type: "error"
                    });
                })
            },
            updateContacts(){
                var contactSettings = {};

                if (this.notUpdateContactAddress){
                    contactSettings.address = null;
                }else {
                    contactSettings.address = this.contactAddress;
                }

                if (this.notUpdateContactEmail){
                    contactSettings.email = null;
                }else {
                    contactSettings.email = this.contactEmail;
                }
                
                if (this.notUpdateContactPhoneNumber){
                    contactSettings.phone_number = null;
                }else {
                    contactSettings.phone_number = this.contactPhoneNumber;
                }

                axios.postForm('/api/contacts', contactSettings).then(response => {
                    if (response.data != undefined && response.data.success != undefined 
                    && response.data !== null && response.data.success === true){
                        this.$notify({
                            title: "Update library contacts successfully!",
                            text: "Update library contacts successfully!",
                            type: "success"
                        });
                    }else {
                        this.$notify({
                            title: "Update library contacts failed!",
                            text: "Update library contacts failed!",
                            type: "error"
                        });
                    }
                }).catch(err => {
                    this.$notify({
                            title: "Update library contacts failed!",
                            text: "Update library contacts failed!",
                            type: "error"
                    });
                })
            },
            getLibraryTimings(){
                axios.get('/api/timings').then(response => {
                  if (response.data.success === true){    
                    this.normalDayOpen = response.data.result.normal_open;
                    this.normalDayClose = response.data.result.normal_close;
                    this.weekendOpen = response.data.result.weekend_open;
                    this.weekendClose = response.data.result.weekend_close;
                    this.weekendStart = response.data.result.weekend_start;
                    this.weekendEnd = response.data.result.weekend_end;

                  }else {
                    this.$notify({
                      title: "Get library timings failed",
                      text: "Get library timings failed",
                      type: "error"
                    });
                  }
                }).catch(err=>{
                    this.$notify({
                      title: "Get library timings failed",
                      text: "Get library timings failed",
                      type: "error"
                    });
                })
            },
            updateLibraryTimings(){
                var libraryTimings = {};
                if (this.normalDayOpen !== null && this.normalDayOpen !== ''){
                    libraryTimings.normal_open = this.normalDayOpen;
                }
                if (this.normalDayClose !== null && this.normalDayClose !== ''){
                    libraryTimings.normal_close = this.normalDayClose;
                }
                if (this.weekendOpen !== null && this.weekendOpen !== ''){
                    libraryTimings.weekend_open = this.weekendOpen;
                }
                if (this.weekendClose !== null && this.weekendClose !== ''){
                    libraryTimings.weekend_close = this.weekendClose;
                }
                if (this.weekendStart !== null && this.weekendStart !== ''){
                    libraryTimings.weekend_start = this.weekendStart;
                }
                if (this.weekendEnd !== null && this.weekendEnd !== ''){
                    libraryTimings.weekend_end = this.weekendEnd;
                }
                axios.postForm('/api/timings', libraryTimings).then(response => {
                    if (response.data != undefined && response.data.success != undefined 
                    && response.data !== null && response.data.success === true){
                        this.$notify({
                            title: "Update library timings successfully!",
                            text: "Update library timings successfully!",
                            type: "success"
                        });
                    }else {
                        this.$notify({
                            title: "Update library timings failed!",
                            text: "Update library timings failed!",
                            type: "error"
                        });
                    }
                }).catch(err => {
                    this.$notify({
                            title: "Update library contacts failed!",
                            text: "Update library contacts failed!",
                            type: "error"
                    });
                })
            }
        },

        created(){
            this.getBorrowSettings();
            this.getContacts(); this.getLibraryTimings();
            document.title = "Library policies settings";
        }
    }
</script>