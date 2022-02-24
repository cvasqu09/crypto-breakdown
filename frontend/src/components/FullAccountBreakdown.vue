<template>
  <div>
    <h1>Breakdown</h1>
    <div class="flex">
      <PieChart :data="data" :labels="labels"></PieChart>
      <div class="flex flex-column">
        <div class="flex">
          <PriceCard v-for="key in accountKeys" :symbol="getSymbol(key)" :price="getPrice(key)" class="mr-3">
            <template #text><div>Price</div></template>
          </PriceCard>
        </div>
        <div>
          Break even prices
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PieChart from "./charts/PieChart.vue";
import {useBreakdown} from "../store/useBreakdown";
import {computed} from "@vue/reactivity";
import PriceCard from "./cards/PriceCard.vue";
import {useWallet} from "../store/useWallet";
import get from "lodash/get";

export default {
  name: "FullAccountBreakdown.vue",
  components: {PriceCard, PieChart},
  setup() {
    const breakdownStore = useBreakdown();
    const walletStore = useWallet();
    const accountKeys = computed(() => Object.keys(breakdownStore.breakdown))
    const labels = computed(() => Object.keys(breakdownStore.breakdown)
        .map(accountId => breakdownStore.breakdown[accountId].symbol))
    const data = computed(() => Object.keys(breakdownStore.breakdown).map(key => {
      const accountBreakdown = breakdownStore.breakdown[key]
      return accountBreakdown.fees + accountBreakdown.subtotal
    }))

    const getPrice = (id) => {
      const amount = get(walletStore.prices, `${id}.amount`, 0);
      return parseFloat(amount)
    }


    const getSymbol = (id) => {
      const symbol = get(breakdownStore.breakdown, `${id}.symbol`, null)
      return symbol;
    }

    return {
      accountKeys,
      data,
      labels,
      getPrice,
      getSymbol,
    }
  }
}
</script>

<style scoped>

</style>
