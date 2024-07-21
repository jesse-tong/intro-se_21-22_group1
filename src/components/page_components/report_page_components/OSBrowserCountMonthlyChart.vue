<template>
    <div class="card">
        <div class="card-header">
            <h6>{{ ($props.chartType === 'os' ? 'OS' : 'Browser') + ' session count' }}</h6>
        </div>
        <div class="card-body">
            <Bar
                id="os-browser-chart"
                :options="chartOptions"
                :data="chartData"
                v-if="loaded"
            />
        </div>
    </div>  
</template>
  
  <script>
  import { Bar } from 'vue-chartjs';
  import axios from 'axios';
  
  export default {
    name: 'BorrowCountByMonth',
    components: { Bar },
    props: {
        chartType: {
            type: String,
            default: 'os'
        }
    },
    data() {
      return {
        loaded: false,
        chartData: {
          labels: [],
          datasets: [
            {
                label: (this.$props.chartType === 'os' ? 'OS': 'Browser') + ' logged in session count',
                backgroundColor: this.$props.chartType === 'os' ? '#643A71' : '#FF7F51',
                data: [],
            },
          ]
        },
        chartOptions: {
          responsive: true,
          maintainAspectRatio: false
        }
      }
    },
    methods: {
        splitFetchData(fetchResult){
            var sessionCounts = [], labels = [];
            fetchResult.forEach((item)=> {
                if (item.type === this.$props.chartType){
                    sessionCounts.push(item.count); labels.push(item.browserOrOs);
                }  
            });
            return [sessionCounts, labels];
        },    
        fetchMonthlySessionCount(){
            axios.get('/api/monthly-session-data').then(response=> {
                if (!response.data || response.data == undefined || !response.data.success){
                    this.$notify({
                        title: "Fetch OS/browser count since the start of this month failed",
                        text: "Fetch OS/browser count since the start of this month failed with unknown error",
                        type: "error"
                    });

                    return;
                }
                if (response.data.success === true){
                    
                    var data = response.data.result;

                    data = this.splitFetchData(data);
                    this.chartData.labels = data[1]; this.chartData.datasets[0].data = data[0];
                    this.loaded = true;
                }else{
                    this.$notify({
                        title: "Fetch OS/browser count since the start of this month failed",
                        text: "Fetch OS/browser count since the start of this month failed with error: " + response.data.error,
                        type: "error"
                    });
                    
                }   
            } ).catch(err=>{
                this.$notify({
                    title: "Fetch OS/browser count since the start of this month failed",
                    text: "Fetch OS/browser count since the start of this month failed with error: " + err.response.data.error,
                    type: "error"
                });
                
            })      
        }
    },
    created(){
        this.fetchMonthlySessionCount();
    }
  }
  </script>
  