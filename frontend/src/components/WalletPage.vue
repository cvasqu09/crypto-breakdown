<template>
  <Toast position="top-right"></Toast>
  <Dialog v-model:visible="displayModal" :modal="true">
    <template #header>
      <h3>Import Manual Buy</h3>
    </template>

    <div>
      <div class="flex mb-4">
        <label for="coin" class="mr-4 align-self-center">Coin</label>
        <InputText id="coin" type="text" v-model="balance_currency"></InputText>
      </div>
      <div class="flex mb-4">
        <label for="cost" class="mr-4 align-self-center">Cost</label>
        <InputText id="cost" type="text" v-model="cost"></InputText>
      </div>
      <div class="flex mb-4">
        <label for="fees" class="mr-4 align-self-center">Fees</label>
        <InputText id="fees" type="text" v-model="fees"></InputText>
      </div>
      <div class="flex mb-4">
        <label for="fees" class="mr-4 align-self-center">Amount</label>
        <InputText id="amount" type="text" v-model="amount"></InputText>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-content-end">
        <Button class="p-button-danger" @click="displayModal=false">Close</Button>
        <Button @click="importBuy">Import</Button>
      </div>
    </template>
  </Dialog>
  <div class="flex justify-content-center">
    <h3 class="mr-2">Wallets</h3>
    <Button class="align-self-center" @click="openManualImportModal">Manual Import</Button>
  </div>

  <div class="flex justify-content-center flex-wrap">
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
import WalletCard from './cards/WalletCard.vue';
import { useToast } from 'primevue/usetoast';
import Toast from 'primevue/toast';
import get from 'lodash/get';

export default {
  name: "WalletPage",
  components: { WalletCard, Toast },
  setup() {
    const accounts: Ref<Wallet[]> = ref([]);
    const displayModal: Ref<boolean> = ref(false);
    const balance_currency: Ref<string> = ref('');
    const fees: Ref<number> = ref(0);
    const cost: Ref<number> = ref(0);
    const amount: Ref<number> = ref(0);
    const router = useRouter();
    const toast = useToast();
    const { favoriteWallets } = storeToRefs(useWallet())

    const goToAccountDetailPage = (id: string) => {
      router.push({name: 'wallet-detail', params: {id}})
    }

    const openManualImportModal = () => {
      displayModal.value = true;
    }

    const importBuy = async() => {
      try {
        const body = {
          balance_currency: balance_currency.value,
          cost: parseFloat(cost.value),
          fees: parseFloat(fees.value),
          amount: parseFloat(amount.value),
        }
        await httpClient.post('/accounts/import_buy/', body);
        toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Buy successfully imported',
          life: 4000
        })
      } catch(e) {
        const responseErrorMessage = get(e, "response.data.message", "")
        toast.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Could not import buy. ' + responseErrorMessage,
          life: 4000
        })
      }
    }

    onMounted(async () => {
      const response = await httpClient.get('/accounts/')
      accounts.value = response.data
    })
    return {
      accounts,
      amount,
      balance_currency,
      cost,
      displayModal,
      favoriteWallets,
      fees,
      goToAccountDetailPage,
      importBuy,
      openManualImportModal,
    }
  }
}
</script>

<style scoped>

</style>
