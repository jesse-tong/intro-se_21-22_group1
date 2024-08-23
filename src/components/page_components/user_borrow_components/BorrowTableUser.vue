<template>
  <div class="row">
    <div v-if="selectedBorrowId !== null" class="col-12 col-md-9">
      <div><span>{{ 'Purchase with Paypal with borrow ID ' + selectedBorrowId +
       'and fee  ' + selectedBorrowFee }}</span></div>
    </div>
    <div class="col-12 col-md-9"><span>Select in the table below to purchase with Paypal :</span></div>
    <div class="col-12 col-md-3" id="paypal-button-container" ref="paypalContainer"></div>
  </div>
  <div class="table-responsive">
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>User ID</th>
          <th>Book Title</th>
          <th>Start Borrow</th>
          <th>End Borrow</th>
          <th>Returned</th>
          <th>Return Date</th>
          <th>Damaged/Lost</th>
          <th>Is Approved</th>
          <th>Payment has resolved</th>
          <th>Borrow fees</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="borrow in borrows" :key="borrow.id" >
          <td>{{ borrow.userId }}</td>
          <td>{{ borrow.bookId }}</td> 
          <td>{{ getDateString(borrow.startBorrow) }}</td>
          <td>{{ getDateString(borrow.endBorrow) }}</td>
          <td>{{ borrow.hasReturned ? 'Yes' : 'No' }}</td>
          <td>{{ borrow.returnDate ? getDateString(borrow.returnDate) : 'N/A'}}</td>
          <td>{{ borrow.isDamagedOrLost ? 'Yes' : 'No' }}</td>
          <td>{{ borrow.isApproved ? 'Yes' : 'No' }}</td>
          <td>{{ borrow.hasResolved ? 'Yes' : 'No' }}</td>
          <td>{{ borrow.fee }}</td>
          <td>
            <button v-if="borrow.isApproved == true && !borrow.hasReturned " class="btn btn-sm btn-primary me-2 mb-2" @click="onReturnBook(borrow.id)" data-bs-toggle="modal" data-bs-target="#returnModal">Return</button>
            <button v-if="borrow.isApproved == true && borrow.hasReturned == true && borrow.hasResolved != true" class="btn btn-sm btn-success me-2 mb-2" @click="()=>onCreateCheckoutSession(borrow.id)" >Pay borrow fee (Stripe)</button>
            <button v-if="borrow.isApproved == true && borrow.hasReturned == true && borrow.hasResolved != true" class="btn btn-sm btn-success" @click="()=>onCreateCheckoutSessionPaypal(borrow.id, borrow.fee)" >Select for Paypal</button>
          </td>
        </tr>
        <tr v-if="borrows == null || borrows.length === 0" >
          <td colspan="11" ><p class="text-center"><i>Currently no borrow status data</i></p></td>
        </tr>
      </tbody>
    </table>
    <ul class="pagination">
        <li class="page-item">
            <a href="#prevPage" id="prevPage" class="page-link" @click="currentPage = currentPage > 1 ? currentPage - 1 : 1"><span>Previous page</span></a>
        </li>
        <li class="page-item">
            <input class="page-link" v-model.number="currentPage" type="number" min="1" :max="maxPage" style="max-width: 75px"/>
        </li>
        <li class="page-item">
            <a href="#mextPage" id="nextPage" class="page-link" @click="currentPage = currentPage < maxPage ? currentPage + 1 : 1"><span>Next page</span></a>
        </li>
    </ul>
  </div>
  <ReturnModal ref="returnModal" :borrowId="returnBorrowId" @update:borrowList="currentPage = 1"/>
</template>
  
<script>
import axios from 'axios';
import ReturnModal from './ReturnModal.vue';
import Stripe from 'stripe';
import { loadScript } from "@paypal/paypal-js";

  export default {
    components: {
        ReturnModal: ReturnModal
    },
    props: {
      bookId: {
        type: [Number, null],
        default: null,
        required: false
      },
      pageLimit: {
        type: Number,
        default: 10,
        required: false
      },
      maxPage: {
        type: Number,
        default: 50
      }
    },
    data(){
        return {
            currentPage: 1,
            addUserId: null,
            addBookId: null,
            addStartBorrow: null,
            addEndBorrow: null,

            borrows: [],
            returnBorrowId: null,
            isDamagedOrLost: null,
            stripeSession: null,
            currency: null,

            paypalClientId: null,
            selectedBorrowId: null,
            selectedBorrowFee: null
        }
    },
    methods: {
      getDateString(date){
        return Date(date).toLocaleString();
      },
      onReturnBook(borrowId){
        this.returnBorrowId = borrowId;
        
      },
      onCreateCheckoutSessionPaypal(borrowId, fee){
        this.selectedBorrowFee = fee; //Fee should be before borrow ID since it'll be used in watch
        this.selectedBorrowId = borrowId;
        this.$refs.paypalContainer.innerHTML = '';
        if (borrowId && borrowId !== null && this.paypalClientId !== null && 
            this.currency !== null && fee && fee !== null){
              loadScript({ "client-id": this.paypalClientId, "currency": this.currency })
                .then((paypal) => {
                    // start to use the PayPal JS SDK script
                  paypal.Buttons({
                    style: {
                      layout: 'horizontal',
                      color:  'blue',
                      shape:  'rect',
                      label:  'paypal'
                    },
                    createOrder: function(data, actions) {
                      return actions.order.create({
                        purchase_units: [{
                          amount: {
                            value: fee.toString()
                          }
                        }],
                        application_context: {
                          shipping_preference: 'NO_SHIPPING'
                        }
                      });
                    },
                    onApprove: (data, actions) => {
                        return axios.post(`/create-checkout-session-paypal/${borrowId}/${data.orderID}`)
                              .then((orderData) => {
                                  if (orderData.data && orderData.data.success && orderData.data.success === true){
                                    this.$notify({
                                      title: 'Payment success',
                                      text: orderData.data.status,
                                      type: 'success'
                                    });
                                  }else {
                                    this.$notify({
                                      title: 'Payment failed',
                                      text: orderData.data.status,
                                      type: 'error'
                                    });
                                  }
                                  
                              }).catch(err => {
                                if (err.response && err.response.data && err.response.data.status){
                                  this.$notify({
                                    title: 'Payment failed',
                                    text: err.response.data.status,
                                    type: 'error'
                                  });
                                }
                                
                              });
                      },
                    }).render('#paypal-button-container');
                  
                })
                .catch((err) => {
                    console.error("failed to load the PayPal JS SDK script", err);
                });
            }else {
              this.$notify({
                title: 'Cannot load Paypal payment',
                text: 'Cannot load Paypal payment, please check your Paypal client ID, currency, and fee',
                type: 'error'
              });
            }
      },
      getStripePublishableKey(){
        axios.get('/get-stripe-key').then(response => {
          this.stripeSession = Stripe(response.data.publicKey);
        }).catch(err => {
          this.$notify({
            title: 'Failed to get payment session key!',
            text: 'Failed to get payment session key, cannot purchase from Stripe',
            type: 'error'
          });
        })
      },
      getPaypalPublishableKey(){
        axios.get('/get-paypal-key').then(response => {
          this.paypalClientId = response.data.publicKey;
        }).catch(err => {
          this.$notify({
            title: 'Failed to get payment session key!',
            text: 'Failed to get payment session key, cannot purchase from Paypal',
            type: 'error'
          });
        });
      },
      onCreateCheckoutSession(borrowId){
        axios.get('/create-checkout-session/' + borrowId).then(response => {
          window.location.href = response.data.url;
        }).catch(err => {
          if (err.response && err.response.data && err.response.data.error){
            this.$notify({
              title: 'Get Stripe session and redirect to Stripe payment failed!',
                  text: 'Get Stripe session and redirect to Stripe payment failed with error: ' + err.response.data.error,
                  type: 'error'
              });
          }
        })
      },
      fetchBorrow(newCurrentPage){
        let searchParams = {};
                if (this.$props.bookId !== null){
                    searchParams.book_id = this.$props.bookId;
                }
                searchParams.page = newCurrentPage; searchParams.limit = this.$props.pageLimit;
                axios.get('/api/borrow', {
                    params: searchParams
                }).then(response => {
                    if (!response.data || !response.data.success){
                        this.$notify({
                        title: "Unknown error",
                        text: "Unknown error, this can be server or network error.",
                        type: "error"
                        });
                        return;
                    }
                    if (response.data.success === true){
                        this.borrows = response.data.result;
                    }else {
                        this.$notify({
                        title: "Fetch borrow your borrow list error",
                        text: "Fetch borrow your borrow list error: " + response.data.error,
                        type: "error"
                        });
                        return;
                    }
                }).catch(err=>{
                    this.$notify({
                        title: "Fetch borrow your borrow list error",
                        text: "Fetch borrow your borrow list error: " + err.response.data.error,
                        type: "error"
                    });
                    return;
                }).finally(()=>{
                    
                })
      },
      fetchBorrowPolicies(){
          axios.get('/api/borrow-policies?noPolicyText=true').then(response => {
              if (response.data != undefined && response.data.success != undefined && response.data.success === true){    
                  this.currency = response.data.result.currency;
              }
          });
      }
    },
    watch: {
        currentPage: {
            handler(newCurrentPage, oldCurrentPage){
                this.fetchBorrow(newCurrentPage);
            },
            immediate: true
        },
        selectedBorrowId: {
          handler(newBorrowId, oldBorrowId){
            
          },
          immediate: false
        }
    },
    created(){
      this.getStripePublishableKey();
      this.getPaypalPublishableKey();
      this.fetchBorrowPolicies();
    },
    
  };
  </script>