<template>
  <h2>Import Page</h2>
  <template v-for="manualBuy in manualBuys" :key="manualBuy.id">
    <div>
      <span>{{manualBuy.amount.currency}}</span>
      <span>{{getAmount(manualBuy.amount.amount)}}</span>
    </div>
  </template>
</template>

<script>
import { onMounted, ref } from "@vue/runtime-core";
import httpClient from '../httpClient';

export default {
  name: "ImportPage",
  setup() {
    let manualBuys = ref([]);

    onMounted(async () => {
      const manualBuyResponse = await httpClient.get("/accounts/manual_buys/")
      manualBuys.value = manualBuyResponse.data
      console.log(manualBuys.value)
    })

    const getAmount = (amount) => {
      return parseFloat(amount).toFixed(5)
    }

    return {
      getAmount,
      manualBuys
    }
  }
}
</script>

<style scoped>

</style>
