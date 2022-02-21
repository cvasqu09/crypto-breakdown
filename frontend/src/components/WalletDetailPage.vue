<template>
  <div class="flex justify-content-end">
    <Toast position="top-right"></Toast>
    <Button class="mt-3 p-button-info" @click="refreshAccount">Refresh accounts</Button>
  </div>
  <h1>Wallet Detail</h1>
  <div class="flex">
    <GainLossCard title="Total Gain/Loss (%)" :value="gainLossPercent" type="percent"></GainLossCard>
  </div>
  <div class="flex justify-content-center">
    <Card class="mr-3 cost-card">
      <template #title>
        <h4>Fees</h4>
      </template>
      <template #content>
        <div>{{ `$${totalFees.toFixed(2)}` }}</div>
      </template>
    </Card>
    <Card class="mr-3 cost-card">
      <template #title>
        <h4>Total {{ symbol }} bought</h4>
      </template>
      <template #content>
        <div>{{ `${totalAmountBought.toFixed(5)}` }}</div>
      </template>
    </Card>
    <Card class="cost-card">
      <template #title>
        <h4>Total cost</h4>
      </template>
      <template #content>
        <div>{{ `$${totalCost.toFixed(2)}` }}</div>
      </template>
    </Card>
  </div>
  <PieChart :labels="labels" :data="data"></PieChart>
  <Button @click="favoriteWallet">{{ getFavoriteButtonText }}</Button>
</template>

<script>
import {onMounted, ref} from "@vue/runtime-core";
import {useRoute} from "vue-router";
import {computed} from "@vue/reactivity";
import get from 'lodash/get';
import {useWallet} from "../store/useWallet";
import httpClient from "../httpClient";
import PieChart from "./charts/PieChart.vue";
import {useToast} from "primevue/usetoast";
import Toast from "primevue/toast";
import GainLossCard from "./GainLossCard.vue";

export default {
  name: "WalletDetailPage.vue",
  components: {GainLossCard, PieChart, Toast},
  setup() {
    const route = useRoute();
    const toast = useToast();
    const buys = ref([])
    const symbol = ref("");
    const walletStore = useWallet();
    const walletId = route.params.id;
    const labels = ['Fees', 'Cost']

    const favoriteWallet = async () => {
      await walletStore.toggleFavoriteWallet(walletId);
    }

    const getFavoriteButtonText = computed(() => {
      const favoriteWallets = walletStore.favoriteWallets.map(favoriteWallet => favoriteWallet.wallet.id);
      if (favoriteWallets.includes(walletId)) {
        return 'Unfavorite'
      } else {
        return 'Favorite'
      }
    })

    onMounted(async () => {
      const walletId = route.params.id;
      await walletStore.refreshWallet(walletId);
      await walletStore.loadWallet(walletId);
      const wallet = walletStore.wallet;
      await walletStore.loadPrice(wallet);
      const response = await httpClient.get(`/accounts/${walletId}/buys`)
      buys.value = response.data.data
      symbol.value = response.data.symbol
    })

    const totalCost = computed(() => {
      const amountList = buys.value.map(buy => get(buy, 'total.amount', 0))
      return amountList.reduce((prev, curr) => prev + parseFloat(curr), 0)
    })


    const totalSubCost = computed(() => {
      const amountList = buys.value.map(buy => get(buy, 'subtotal.amount', 0))
      return amountList.reduce((prev, curr) => prev + parseFloat(curr), 0);
    })

    const totalAmountBought = computed(() => {
      const amountList = buys.value.map(buy => get(buy, 'amount.amount', 0));
      return amountList.reduce((prev, curr) => {
        return prev + parseFloat(curr)
      }, 0)
    })

    const gainLossPercent = computed(() => {
      const currentPrice = walletStore.getPrice(walletId);

      const priceAmount = get(currentPrice, 'amount', 0);
      const currentWorth = totalAmountBought.value * priceAmount;

      return (currentWorth / totalSubCost.value) - 1;
    })

    const data = computed(() => {
      return [totalFees.value, totalSubCost.value]
    })

    const totalFees = computed(() => {
      let totalFeeAmount = 0
      buys.value.forEach((buy) => {
        const buyFees = get(buy, 'fees', []);
        buyFees.forEach((buyFee) => {
          const amount = get(buyFee, 'amount.amount', 0);
          totalFeeAmount += parseFloat(amount);
        })
      })
      return totalFeeAmount
    })

    const refreshAccount = async () => {
      try {
        const walletId = route.params.id;
        await httpClient.post('/refresh/buys/', {}, {params: {account_id: walletId}});
        toast.add({severity: 'success', summary: 'Success', detail: 'Account refreshed', life: 4000})
      } catch (e) {
        toast.add({severity: 'error', summary: 'Error', detail: 'Could not refresh account info', life: 4000})
      }
    }

    return {
      buys,
      data,
      gainLossPercent,
      totalAmountBought,
      totalFees,
      totalSubCost,
      totalCost,
      labels,
      symbol,
      favoriteWallet,
      getFavoriteButtonText,
      refreshAccount
    }
  }
}
</script>

<style scoped>
.cost-card {
}
</style>
