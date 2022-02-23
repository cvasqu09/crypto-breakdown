<template>
  <div>
    <h1>Breakdown</h1>
    <PieChart :data="data" :labels="labels"></PieChart>
  </div>
</template>

<script>
import PieChart from "./charts/PieChart.vue";
import {useBreakdown} from "../store/useBreakdown";
import {computed} from "@vue/reactivity";
export default {
  name: "FullAccountBreakdown.vue",
  components: {PieChart},
  setup() {
    const breakdownStore = useBreakdown();
    const labels = computed(() => Object.keys(breakdownStore.breakdown))
    const data = computed(() => Object.keys(breakdownStore.breakdown).map(key => {
      const accountBreakdown = breakdownStore.breakdown[key]
      return accountBreakdown.fees + accountBreakdown.subtotal
    }))

    return {
      data,
      labels
    }
  }
}
</script>

<style scoped>

</style>
