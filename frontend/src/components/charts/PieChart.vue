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
            ],
            hoverOffset: 4
          }]
        }
      });
    }

    watch(props, () => {
      console.log(props.data)
      buildChart(props.labels, props.data)
    })
  }
}


</script>
