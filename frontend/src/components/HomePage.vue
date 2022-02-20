<template>
  <div class="flex justify-content-end">
    <Menu ref="menu" :model="menuItems" :popup="true"/>
  </div>
  <div v-for="account in accounts">
    {{ account.name }} {{ account.native_amount }}
  </div>
  <h1>Favorite Wallets</h1>
  <div class="flex flex-row p-3">
    <Card v-for="favorite in favoriteWallets" class="mr-5">
      <template #title>
        <div class="flex align-content-center">
          <img class="mr-2"
              :src="`node_modules/cryptocurrency-icons/svg/color/${favorite.wallet.balance_currency}.svg`"
              height="32"
              width="32">
          <span>{{ favorite.wallet.name }}</span>
        </div>
      </template>
      <template #content>
        <Button @click="navigateToWalletDetail(favorite.wallet.id)">Wallet</Button>
      </template>
    </Card>
  </div>
</template>

<script lang="ts">
import { onMounted, ref } from "@vue/runtime-core";
import { useRouter } from "vue-router";
import { useWallet } from "../store/useWallet";
import { storeToRefs } from "pinia";
import { useBreakdown } from "../store/useBreakdown";
import { Wallet } from '../types'

export default {
  name: "HomePage",
  setup() {
    const accounts = ref([]);
    const router = useRouter()
    const walletStore = useWallet();
    const breakdownStore = useBreakdown();
    const {breakdown} = storeToRefs(walletStore);
    const favoriteWallets: Wallet[] = walletStore.favoriteWallets;
    const {breakdown: fullBreakdown} = storeToRefs(breakdownStore);

    const menuItems = [{
      label: 'Account',
      command: () => {
        router.push('/wallet')
      }
    }]
    const menu = ref(null);

    const navigateToWalletDetail = (walletId) => {
      router.push({name: 'wallet-detail', params: {id: walletId}})
    }

    onMounted(async () => {
      await walletStore.loadFavoriteWallets();
      await walletStore.loadBreakdown();
      await breakdownStore.loadBreakdown();
      console.log('breakdown', fullBreakdown)
    })

    return {
      accounts,
      breakdown,
      favoriteWallets,
      fullBreakdown,
      menuItems,
      menu,
      navigateToWalletDetail,
    }
  }
}
</script>

<style scoped>

</style>
