<template>
  <h3>Wallets</h3>
  <div class="flex flex-wrap">

    <template v-for="account in accounts">
      <WalletCard :wallet="account"></WalletCard>
    </template>
  </div>
</template>

<script lang="ts">
import { onMounted, ref, Ref } from "@vue/runtime-core";
import httpClient from "../httpClient";
import { useRouter } from 'vue-router';
import { Wallet } from '../types';
import { storeToRefs } from 'pinia';
import { useWallet } from '../store/useWallet';
import WalletCard from './WalletCard.vue';

export default {
  name: "WalletPage",
  components: { WalletCard },
  setup() {
    const accounts: Ref<Wallet[]> = ref([]);
    const router = useRouter();
    const { favoriteWallets } = storeToRefs(useWallet())

    const goToAccountDetailPage = (id: string) => {
      router.push({name: 'wallet-detail', params: {id}})
    }

    onMounted(async () => {
      const response = await httpClient.get('/accounts/')
      accounts.value = response.data
    })
    return {
      accounts,
      favoriteWallets,
      goToAccountDetailPage
    }
  }
}
</script>

<style scoped>

</style>
