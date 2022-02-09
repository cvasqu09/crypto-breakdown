<template>
  <div class="flex justify-content-end">
<!--    <Button icon="pi pi-bars" type="button" @click="toggle"/>-->
    <Menu ref="menu" :model="menuItems" :popup="true"/>
  </div>
  <div v-for="account in accounts">
    {{ account.name }} {{ account.native_amount }}
  </div>
  <h3>Favorite Wallets</h3>
  <div v-for="favorite in favoriteWallets">
    <Button @click="navigateToWalletDetail(favorite.wallet.id)">{{favorite.wallet.name}}</Button>
  </div>
</template>

<script>
import {onMounted, ref, watch} from "@vue/runtime-core";
import httpClient from "../httpClient";
import {useRouter} from "vue-router";
import {useWallet} from "../store/useWallet";
import {storeToRefs} from "pinia";

export default {
  name: "HomePage",
  setup() {
    const accounts = ref([]);
    const router = useRouter()
    const walletStore = useWallet()
    const {favoriteWallets} = storeToRefs(walletStore);

    const menuItems = [{
      label: 'Account',
      command: () => {
        router.push('/wallet')
      }
    }]
    const menu = ref(null);

    const toggle = (event) => {
      menu.value.toggle(event);
    }

    const navigateToWalletDetail = (walletId) => {
      router.push({ name: 'wallet-detail', params: {id: walletId}})
    }

    onMounted(async () => {
      favoriteWallets.value = await walletStore.loadFavoriteWallets();
      const response = await httpClient.get('/accounts')
      accounts.value = response.data.filter(account => parseFloat(account["native_amount"]) !== 0)
    })

    return {
      accounts,
      favoriteWallets,
      menuItems,
      menu,
      navigateToWalletDetail,
      toggle
    }
  }
}
</script>

<style scoped>

</style>
