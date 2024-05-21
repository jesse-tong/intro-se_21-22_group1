<template>
    <div>
        <div class="col">
            <div class="row-1">
                <h3 class="ms-3 mt-2">Report Dashboard</h3>
            </div>
            <div class="row-7">
                <div class="row">
                    <div class="col-12 col-md-7">
                        <div class="p-2 p-lg-3">
                            <BorrowCountChart id="borrowCountChart" />
                        </div>
                    </div>
                    <div class="col">
                        <div class="p-2 p-lg-3">
                            <MostRecentBorrow id="mostRecentBorrow" />
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div>

                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import BorrowCountChart from './BorrowCountChart.vue';
    import MostRecentBorrow from './MostRecentBorrow.vue';
    export default {
        components: {
            BorrowCountChart: BorrowCountChart,
            MostRecentBorrow: MostRecentBorrow
        }
    }
</script>