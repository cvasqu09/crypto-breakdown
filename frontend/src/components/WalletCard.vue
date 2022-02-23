<template>
  <Card class="mr-5 mb-3 wallet-card">
    <template #title>
      <div class="flex align-content-center">
        <img
class="mr-2"
             :src="`node_modules/cryptocurrency-icons/svg/color/${wallet.balance_currency}.svg`"
             height="32"
             width="32"
             @error="setDefaultImage($event)">
        <span>{{ wallet.name }}</span>
      </div>
    </template>
    <template #content>
      <Button @click="navigateToWalletDetail(wallet.id)">Wallet</Button>
    </template>
  </Card>
</template>

<script lang="ts">
import { useRouter } from 'vue-router';

export default {
  name: "WalletCard",
  props: {
    wallet: {
      type: Object,
      required: true,
    }
  },
  setup() {
    const router = useRouter();

    const navigateToWalletDetail = (walletId) => {
      router.push({name: 'wallet-detail', params: {id: walletId}})
    }

    const setDefaultImage = ($event) => {
      $event.target.src = 'node_modules/cryptocurrency-icons/svg/white/btc.svg'
    }

    return {
      navigateToWalletDetail,
      setDefaultImage
    }
  }
}
</script>

<style scoped>
.wallet-card {
  width: 240px;
}
</style>
