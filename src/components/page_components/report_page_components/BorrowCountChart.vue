<template>
    <div class="card">
        <div class="card-header">
            <h5>Borrow count</h5>
        </div>
        <div class="card-body">
            <Line
                id="my-chart-id"
                :options="chartOptions"
                :data="chartData"
                v-if="loaded"
            />
            <h5 class="card-text mt-2">{{ 'Borrow count from ' + startDate + ' to ' + endDate + ': ' + borrowCount }}</h5>
        </div>
    </div>  
</template>
  
  <script>
  import { Line } from 'vue-chartjs';
  import axios from 'axios';
  
  export default {
    name: 'BorrowCountByMonth',
    components: { Line },
    data() {
      return {
        loaded: false,
        borrowCount: 'N/A',
        startDate: 'N/A',
        endDate: 'N/A',
        chartData: {
          labels: [],
          datasets: [
            {
                label: 'Borrow request count',
                backgroundColor: '#1433d6',
                borderColor: '#1433d6',
                data: [],
            },
          ]
        },
        chartOptions: {
          responsive: true,
          lineTension: 0.3,
        }
      }
    },
    methods: {
        splitFetchData(fetchResult){
            var borrowCount = [], timeLabels = [], sum = 0;
            fetchResult.forEach((item)=> {
                borrowCount.push(item.borrow_count);
                sum = sum + item.borrow_count;
                timeLabels.push(item.month + '/' + item.year);
            });
            return [timeLabels, borrowCount, sum];
        },
        nextMonth(month, year){
            if (month < 12 && month >= 1){
                return [month + 1, year];
            }else if (month === 12) {
                return [1, year + 1];
            }else if (month < 1){
                return [1, year];
            }else {
                return [1, year + 1];
            }
        },
        fetchBorrowCount(){
            
            axios.get('/api/borrow-count-by-month').then(response=> {
                if (!response.data || response.data == undefined || !response.data.success){
                    this.$notify({
                        title: "Fetch borrow count by month failed",
                        text: "Fetch borrow count by month failed with unknown error, this can be from network or server",
                        type: "error"
                    });

                    return;
                }
                if (response.data.success === true){
                    
                    var data = response.data.result;
                    data.reverse();
                    this.startDate = data.at(0).month + '/' + data.at(0).year;
                    this.endDate = data.at(-1).month + '/' + data.at(-1).year;

                    var chartData = this.splitFetchData(data);
                    var timeLabels = chartData[0], borrowCount = chartData[1], totalBorrowCount = chartData[2];
                    this.borrowCount = totalBorrowCount;
                    this.chartData.labels = timeLabels; this.chartData.datasets[0].data = borrowCount;
                    this.loaded = true;
                }else{
                    this.$notify({
                        title: "Fetch borrow count by month failed",
                        text: "Fetch borrow count by month failed with error: " + response.data.error,
                        type: "error"
                    });
                    
                }   
            } ).catch(err=>{
                this.$notify({
                    title: "Fetch borrow count by month failed",
                    text: "Fetch borrow count by month failed with error: " + err.response.data.error,
                    type: "error"
                });
                
            })   
            
        }
    },
    created(){
        this.fetchBorrowCount();
    }
  }
  </script>
  