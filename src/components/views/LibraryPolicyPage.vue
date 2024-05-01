<template>
    <div class="mx-2 mb-2 mt-2 rounded border border-secondary border-2 px-2">
        <h3 class="mt-2" >
            Policies when using library services
        </h3>
        <div class="collapse" id="serviceUsagePolicyText">

        </div>
        <h3 class="mt-2" >
            Overdue policies and fines
        </h3>
        <div class="" id="overduePolicyText">
            <ul v-if="borrow_policy_constants !== null">
                <li><span>Overdue fines will be applicable if the item(s) is/are not returned before 1 hours after the end borrow date.
                </span></li>
                <li><span>For each day overdue (the 12 first hours overdue is also counted if the items aren't returned before that time)
                    will be {{ borrow_policy_constants.currency + " " + borrow_policy_constants.overdue_fine }}/day.
                </span></li>
                <li><span>After {{ borrow_policy_constants.overdue_time_limit }} days, the overdue items are treated as lost.</span></li>
                <li><span>A nonrefundable {{ borrow_policy_constants.currency + " " + borrow_policy_constants.damage_and_lost_fine }} 
                    processing fee will be charged for each lost or irrepairably damaged item.</span></li> 
            </ul>
            <span>The library will notify the customer of the replacement cost for a damaged
        or lost item based upon publication date.</span>
            <ul>
                <li><span>Full replacement cost of the item for materials published in the last
        5 years</span></li>
                <li><span>Double the replacement cost for materials published more than 5 years
        ago.</span></li>
                <li><span>Full replacement costs for DVDs, video games and CDs released
        within the last year and one half the cost for items released more
        than a year ago.</span></li>
            </ul>
        </div>
        
    </div>
    
</template>

<script>
    import axios from 'axios';
    export default {
        data(){
            return {
                borrow_policy_constants: null
            } 
        },
        methods: {
            getBorrowPolicies(){
                axios.get('/api/borrow-policies').then(response => {
                  if (response.data.success === true){    
                    this.borrow_policy_constants = response.data.result;
                  }else {
                    this.$notify({
                      title: "Get borrow policies failed, some part may be unavailable",
                      text: "Get borrow policies failed, some part may be unavailable",
                      type: "error"
                    });
                  }
                }).catch(err=>{
                    this.$notify({
                      title: "Get borrow policies failed, some part may be unavailable",
                      text: "Get borrow policies failed, some part may be unavailable",
                      type: "error"
                    });
                })
            }
        },
        created(){
            this.getBorrowPolicies();
        }
    }
</script>