<template>
    <div>
        <div class="col">
            <div class="row-1">
                <h5 class="section-title bg-light-subtle text-center text-primary px-3 mt-3">Report dashboard</h5>
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
                                        <div class="col-12 col-lg-12 mt-2">
                                            <LocationMapChart />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-12 col-md-5 col-xl-4">
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
    import LocationMapChart from './LocationMapChart.vue';

    export default {
        components: {
            BorrowCountChart: BorrowCountChart,
            MostRecentBorrow: MostRecentBorrow,
            OSBrowserCountMonthlyChart: OSBrowserCountMonthlyChart,
            LocationMapChart: LocationMapChart
        }
    }
</script>