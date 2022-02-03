<template>
  <h3>Account Page</h3>
  <div v-for="account in accounts">
    <Button @click="goToAccountDetailPage(account.id)">{{account.name}}</Button>
  </div>
</template>

<script lang="ts">
import { onMounted, ref, Ref } from "@vue/runtime-core";
import httpClient from "../httpClient";
import { useRouter } from 'vue-router';
import { Account } from '../types';

export default {
  name: "AccountPage",
  setup() {
    const accounts: Ref<Account[]> = ref([]);
    const router = useRouter();
    const goToAccountDetailPage = (id: string) => {
      router.push({name: 'account-detail', params: {id}})
    }

    onMounted(async () => {
      const response = await httpClient.get('/accounts/')
      accounts.value = response.data
    })
    return {
      accounts,
      goToAccountDetailPage
    }
  }
}
</script>

<style scoped>

</style>
