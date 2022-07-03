<template>
  <canvas id="chart" ref="chart" width="400" height="400"></canvas>
</template>

<script>
import {onMounted, ref} from "@vue/runtime-core";
import {Chart, registerables} from "chart.js";
import {toRefs, watch} from "vue";

Chart.register(...registerables);

export default {
  name: "PieChart",
  components: {},
  props: {
    labels: {
      type: Array,
      required: true
    },
    data: {
      type: Array,
      required: true
    }
  },
  setup(props) {
    let myChart = null;

    const buildChart = (labels, data) => {
      const ctx = document.getElementById('chart');
      Chart.defaults.plugins.legend.labels.color = '#ffffff';
      myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: [
            ...labels
          ],
          datasets: [{
            label: 'My First Dataset',
            data: [...data],
            backgroundColor: [
              'rgb(255, 99, 132)',
              'rgb(54, 162, 235)',
              'rgb(128, 255, 0)',
              'rgb(255, 153, 255)',
              'rgb(153, 153, 255)',
              'rgb(255, 255, 103)'
            ],
            hoverOffset: 4,
            color: '#ffffff'
          }],
        },
        options: {
          responsive: false,

        }
      });
    }

    watch(props, () => {
      buildChart(props.labels, props.data)
    })
  }
}


</script>
