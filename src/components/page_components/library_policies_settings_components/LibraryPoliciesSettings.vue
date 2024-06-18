<template>
    <h4 class="ms-4 me-3 mt-2 ">Borrow policies</h4>
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
            <select class="form-control" id="currency" v-model="currency">
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
            <MdEditor v-model="libraryPolicyText" :language="en-US" :codeTheme="a11y"/>
        </div>
        <div class="col-12 mt-2">
            <button @click="updateBorrowSettings" class="mb-2 btn btn-success"><span>Update borrow policies</span></button>
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
                libraryPolicyText: 'Enter other policy text (such as other borrow policies, data policies, policies when using library,...) here'
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
                            type: "success"
                        });
                    }
                }).catch(err => {
                    this.$notify({
                            title: "Update borrow policies failed!",
                            text: "Update borrow policies failed!",
                            type: "success"
                    });
                })
            },
            updateOtherPolicies(){

            }
        },
        created(){
            this.getBorrowSettings();
        }
    }
</script>