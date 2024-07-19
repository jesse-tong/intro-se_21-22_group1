<template>
    <div class="card">
        <div class="card-header">
            <h6>{{ 'Page view by country' }}</h6>
        </div>
        <div class="card-body">
            <Choropleth :chart-data="chartData" :options="options" v-if="loaded" />
        </div>
    </div>  
  </template>
  
  <script>
  import Choropleth from "./ChoroplethChart.vue";
  import { topojson } from "chartjs-chart-geo";
  import countriesTopoJson from "../../../assets/countries-110m.json";
  import axios from "axios";

  
  const countries = topojson.feature(
    countriesTopoJson,
    countriesTopoJson.objects.countries
  ).features;
  
  export default {
    name: "App",
    components: {
      Choropleth: Choropleth
    },
    data() {
      return {
        chartData: {
          labels: countries.map(d => d.properties.name),
          datasets: [
            {
              label: "Countries",
              backgroundColor: context => {
                if (context.dataIndex == null) {
                  return null;
                }
                const value = context.dataset.data[context.dataIndex];
                //Min value: rgb(5, 10, 110); max value: rgb(215, 220, 255)
                return `rgb(${parseInt(215 - (value.value / this.maxVal * 210))}, ${parseInt(220 - (value.value / this.maxVal * 210))}, ${parseInt(255 - (value.value / this.maxVal * 145))})`;
              },
              data: []
            }
          ]
        },
        options: {
          showOutline: true,
          showGraticule: false,
          responsive: true,
          legend: {
            display: false
          },
          scales: {
            projection: {
                axis: 'x',
                projection: "equirectangular"
            }
          }
        },
        loaded: false,
        maxVal: 1
      };
    },
    methods: {
        splitFetchData(fetchResult){
            var viewCount = new Map();
            var maxVal = 1;
            fetchResult.forEach((item)=> {
                if (item.type === 'country'){
                    viewCount.set(item.browserOrOs, item.count);
                    if (item.count > maxVal){
                        maxVal = item.count;
                    }
                }  
            });
            this.maxVal = maxVal;
            return viewCount;
        },    
        fetchMonthlySessionCount(){
            axios.get('/api/monthly-session-data').then(response=> {
                if (!response.data || response.data == undefined || !response.data.success){
                    this.$notify({
                        title: "Fetch country visit count since the start of this month failed",
                        text: "Fetch country visit count since the start of this month failed with unknown error",
                        type: "error"
                    });
                    return;
                }
                if (response.data.success === true){
                    
                    var viewCountByCountry = response.data.result;

                    viewCountByCountry = this.splitFetchData(viewCountByCountry);
                    console.log(viewCountByCountry);
                    this.chartData.datasets[0].data = countries.map(d => ({ feature: d, value: viewCountByCountry.get(d.id) ? viewCountByCountry.get(d.id) : 0 }));
                    this.loaded = true;
                }else{
                    this.$notify({
                        title: "Fetch country visit count since the start of this month failed",
                        text: "Fetch country visit count since the start of this month failed with error: " + response.data.error,
                        type: "error"
                    });
                    
                }   
            } ).catch(err=>{
                this.$notify({
                    title: "Fetch country visit count since the start of this month failed",
                    text: "Fetch country visit count since the start of this month failed with error: " + err.response.data.error,
                    type: "error"
                });
                
            })      
        }
    },
    created(){
        this.fetchMonthlySessionCount();
    }

  };
  </script>