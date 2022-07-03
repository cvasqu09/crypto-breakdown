<template>
  <h2>Import Page</h2>
  <DataTable :value="currencyAmounts">
    <Column field="currency" header="Currency"></Column>
    <Column field="amount" header="Amount"></Column>
    <Column header="Delete">
      <template #body="slotProps">
        <Button icon="pi pi-trash" @click="confirmManualBuyDelete(slotProps.data.id)"></Button>
      </template>
    </Column>
    <template #empty>
      No manual buys.
    </template>
  </DataTable>
  <ConfirmDialog></ConfirmDialog>
</template>

<script>
import {onMounted, ref} from "@vue/runtime-core";
import httpClient from '../httpClient';
import get from "lodash/get";
import {computed} from "@vue/reactivity";
import {useConfirm} from "primevue/useconfirm";


export default {
  name: "ImportPage",
  setup() {
    const manualBuys = ref([]);
    const displayDeleteModal = ref(false);
    const confirm = useConfirm();
    const manualBuysUrl = "/manual_buys";

    const loadManualBuys = async () => {
      const manualBuyResponse = await httpClient.get(manualBuysUrl)
      manualBuys.value = manualBuyResponse.data
    }

    onMounted(async () => {
      await loadManualBuys()
    })

    const currencyAmounts = computed(() => {
      return manualBuys.value.map(buy => ({
        "id": buy.id,
        "amount": get(buy, 'amount.amount', 0),
        "currency": get(buy, 'amount.currency', 'None')
      }))
    })

    const getAmount = (amount) => {
      return parseFloat(amount).toFixed(5)
    }

    const confirmManualBuyDelete = (id) => {
      confirm.require({
        header: "Confirm deletion",
        message: "Do you want to delete this manual import?",
        icon: 'pi pi-exclamation-triangle',
        accept: async () => {
          await httpClient.delete(`${manualBuysUrl}/${id}`)
          await loadManualBuys();
        }
      })
    }

    return {
      confirmManualBuyDelete,
      currencyAmounts,
      displayDeleteModal,
      getAmount,
      loadManualBuys,
      manualBuys
    }
  }
}
</script>

<style scoped>

</style>
