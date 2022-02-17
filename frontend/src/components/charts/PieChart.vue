<template>
  <canvas id="chart" ref="chart" width="400" height="400"></canvas>
</template>

<script>
import {onMounted, ref} from "@vue/runtime-core";
import {Chart, registerables} from "chart.js";

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
    const chart = ref(null);

    onMounted(() => {
      console.log('props', props)
      const ctx = document.getElementById('chart');

      const myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: [
            ...props.labels
          ],
          datasets: [{
            label: 'My First Dataset',
            data: [...props.data],
            backgroundColor: [
              'rgb(255, 99, 132)',
              'rgb(54, 162, 235)',
            ],
            hoverOffset: 4
          }]
        }
      });
    })

    return {
      chart
    }
  }
}


</script>
