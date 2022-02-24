<template>
  <Card class="fit">
    <template #title>
      <div>
        <img
            :src="`node_modules/cryptocurrency-icons/svg/color/${symbol.toLowerCase()}.svg`"
            height="32"
            width="32"
            @error="setDefaultImage($event)">
      </div>
    </template>
    <template #content>
      <div>
        <slot name="text"></slot>
        <div>{{formattedCurrency(price)}}</div>
      </div>
    </template>
  </Card>
</template>

<script>
export default {
  name: "PriceCard",
  props: {
    symbol: {
      type: String,
      required: true
    },
    price: {
      type: Number,
      required: true
    }
  },
  setup() {
    const setDefaultImage = ($event) => {
      $event.target.src = 'node_modules/cryptocurrency-icons/svg/white/btc.svg'
    }

    const formattedCurrency = (p) => {
      return `$${p.toFixed(5)}`
    }

    return {
      formattedCurrency,
      setDefaultImage
    }
  }
}
</script>

<style scoped>
.fit {
  height: fit-content;
}
</style>
