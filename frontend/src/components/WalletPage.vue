<template>
  <h3>Wallets</h3>
  <div v-for="account in accounts">
    <Button @click="goToAccountDetailPage(account.id)">{{account.name}}</Button>
  </div>
</template>

<script lang="ts">
import { onMounted, ref, Ref } from "@vue/runtime-core";
import httpClient from "../httpClient";
import { useRouter } from 'vue-router';
import { Account } from '../types';
import { storeToRefs } from 'pinia';
import { useWallet } from '../store/useWallet';

export default {
  name: "WalletPage",
  setup() {
    const accounts: Ref<Account[]> = ref([]);
    const router = useRouter();
    const { favoriteWallets } = storeToRefs(useWallet())

    const goToAccountDetailPage = (id: string) => {
      router.push({name: 'account-detail', params: {id}})
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
