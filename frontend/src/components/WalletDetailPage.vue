<template>
  <h3>Wallet Detail</h3>
  <h4>Fees</h4>
  <div>{{ totalFees }}</div>
  <h4>Total {{ symbol }} bought</h4>
  <div>{{ totalAmountBought }}</div>
  <h4>Total cost</h4>
  <div>{{totalCost}}</div>
</template>

<script>
import {onMounted, ref} from "@vue/runtime-core";
import {useRoute} from "vue-router";
import {computed} from "@vue/reactivity";
import get from 'lodash/get';

export default {
  name: "WalletDetailPage.vue",
  setup() {
    const route = useRoute();
    const buys = ref([])
    const symbol = ref("");

    onMounted(async () => {
      const walletId = route.params.id;
      // const response = await httpClient.get(`/accounts/${walletId}/buys`)
      const response = {
        data: {
          "symbol": "DOT",
          "data": [{
            "id": "99297e16-c068-56f0-af56-29520ecccc6e",
            "status": "completed",
            "created_at": "2022-01-06T03:28:35Z",
            "fees": [{"type": "coinbase", "amount": {"amount": "3.42", "currency": "USD"}}, {
              "type": "bank",
              "amount": {"amount": "0.25", "currency": "USD"}
            }],
            "amount": {"amount": "9.4162304115", "currency": "DOT"},
            "subtotal": {"amount": "246.33", "currency": "USD"},
            "total": {"amount": "250.00", "currency": "USD"},
            "account": "05f5a4c4-75e6-5b34-bcfe-03195041120c"
          },
            {
              "id":
                  "02efc06e-7425-5075-978c-d7478a5ebf8b",
              "status":
                  "completed",
              "created_at":
                  "2021-12-18T17:44:35Z",
              "fees":
                  [{"type": "coinbase", "amount": {"amount": "10.47", "currency": "USD"}}, {
                    "type": "bank",
                    "amount": {"amount": "0.25", "currency": "USD"}
                  }],
              "amount":
                  {
                    "amount":
                        "28.4686353436", "currency":
                        "DOT"
                  }
              ,
              "subtotal":
                  {
                    "amount":
                        "719.28", "currency":
                        "USD"
                  }
              ,
              "total":
                  {
                    "amount":
                        "730.00", "currency":
                        "USD"
                  }
              ,
              "account":
                  "05f5a4c4-75e6-5b34-bcfe-03195041120c"
            }
          ]
        }
      }
      buys.value = response.data.data
      symbol.value = response.data.symbol
    })

    const totalCost = computed(() => {
      const amountList = buys.value.map(buy => get(buy, 'total.amount', 0))
      return amountList.reduce((prev, curr) => prev + parseFloat(curr), 0)
    })

    const totalAmountBought = computed(() => {
      const amountList = buys.value.map(buy => get(buy, 'amount.amount', 0));
      return amountList.reduce((prev, curr) => {
        return prev + parseFloat(curr)
      }, 0)
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

    return {buys, totalAmountBought, totalFees, totalCost, symbol}
  }
}
</script>

<style scoped>

</style>
