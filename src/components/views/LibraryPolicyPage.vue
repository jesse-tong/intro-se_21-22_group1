<template>
    <div class="mx-2 mb-2 mt-2 rounded border border-secondary border-2 px-2">
        <h3 class="mt-2" >
            Policies when using library services
        </h3>
        <div class="" id="serviceUsagePolicyText">
            <ul>
                <li>Customers shall engage in activities associated with the use of a public
                library. Customers not reading, studying or using library materials may be
                required to leave the building, library program or approved community
                event.</li>
                <li>Any customer not abiding by these or other regulations and regulations of
                the library may be required to leave the library premises and may forfeit
                their library privileges. Library employees will contact the police if
                deemed advisable.</li>
                <li>The library board of trustees authorizes library staff and law enforcement
                officers to enforce the library’s published code of conduct policy up to
                and including long-term suspension of library privileges, permanent
                banning from the library or prosecution.</li>
                <li>Customers shall not assault, harass or annoy others in the library. This
                includes noisy or boisterous activities, staring at another person with the
                intent to annoy that person, following another person about the building
                with the intent to annoy that person, playing audio equipment so that
                others can hear it, singing or talking loudly to others or in monologues,
                using profanity, displaying print or nonprint materials of an offensive
                nature to others or by behaving in a manner that can be reasonably
                expected to disturb others.</li>
                <li>Customers shall not interfere with the use of the library by other
                customers or with library employees’ performance of their duties.</li>
                <li>Customers shall not deface or mar library materials including books,
                magazines, newspapers, recordings or other items of the library
                collection. Nor shall they deface, mar or in any way destroy or damage
                library furnishings, walls, machines, or other library property.</li>
            </ul>
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
    //Most of the above text are based on these policies: https://www.ala.org/united/trustees/policies
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