<template>
    <Choropleth :data="chartData" />
  </template>

<script>
import { createTypedChart } from "vue-chartjs";
import { Chart, Tooltip } from 'chart.js';
import { ChoroplethController, GeoFeature, ColorScale, ProjectionScale } from 'chartjs-chart-geo';

Chart.register(ChoroplethController, GeoFeature, ColorScale, ProjectionScale, Tooltip);

const Choropleth = createTypedChart("choropleth", "choropleth");

export default {
  name: 'MapChart',
  components: { Choropleth },
  props: {
        chartData: {
            type: Object,
            default: ()=> {},
        },
    },
  
}

</script>