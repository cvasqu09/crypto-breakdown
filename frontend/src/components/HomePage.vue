<template>
  <div class="flex justify-content-end">
    <Menu ref="menu" :model="menuItems" :popup="true"/>
  </div>
  <FullAccountBreakdown></FullAccountBreakdown>
  <h1>Favorite Wallets</h1>
  <div class="flex flex-row p-3">
    <template v-for="favorite in favoriteWallets">
      <WalletCard :wallet="favorite.wallet"></WalletCard>

    </template>
  </div>
</template>

<script lang="ts">
import { onMounted, ref } from "@vue/runtime-core";
import { useRouter } from "vue-router";
import { useWallet } from "../store/useWallet";
import { storeToRefs } from "pinia";
import { useBreakdown } from "../store/useBreakdown";
import { Wallet } from '../types'
import FullAccountBreakdown from './FullAccountBreakdown.vue';
import WalletCard from './cards/WalletCard.vue';

export default {
  name: "HomePage",
  components: {FullAccountBreakdown, WalletCard},
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

    onMounted(async () => {
      const loadedWallets = await walletStore.loadFavoriteWallets() || [];
      await walletStore.loadBreakdown();
      await breakdownStore.loadBreakdown();
      // @ts-ignore
      const wallets = loadedWallets.map(wallet => wallet.wallet)
      await walletStore.loadBulkPrices(wallets)
    })

    return {
      accounts,
      breakdown,
      favoriteWallets,
      fullBreakdown,
      menuItems,
      menu,
    }
  }
}
</script>

<style scoped>

</style>
