<template>
    <div>
        <div class="col">
            <div class="row-1">
                <h3 class="ms-3 mt-2">Report Dashboard</h3>
            </div>
            <div class="row-11">
                <div class="row">
                    <div class="col-12 col-md-7 col-xl-8">
                        <div class="ps-2 ps-lg-2 pe-lg-1">
                            <div class="col">
                                <div class="row-7">
                                    <BorrowCountChart id="borrowCountChart" />
                                </div>
                                <div class="row-5 mt-2">
                                    <div class="row">
                                        <div class="col-12 col-lg-6">
                                            <OSBrowserCountMonthlyChart :chartType="'os'" />
                                        </div>
                                        <div class="col-12 col-lg-6 mt-2 mt-lg-0">
                                            <OSBrowserCountMonthlyChart :chartType="'browser'" />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col">
                        <div class="p-2 pe-lg-2">
                            <MostRecentBorrow id="mostRecentBorrow" />
                        </div>
                    </div>
                </div>
            </div>
            
        </div>
    </div>
</template>
<script>
    import BorrowCountChart from './BorrowCountChart.vue';
    import MostRecentBorrow from './MostRecentBorrow.vue';
    import OSBrowserCountMonthlyChart from './OSBrowserCountMonthlyChart.vue';
    export default {
        components: {
            BorrowCountChart: BorrowCountChart,
            MostRecentBorrow: MostRecentBorrow,
            OSBrowserCountMonthlyChart: OSBrowserCountMonthlyChart
        }
    }
</script>