<template>
<Card>
  <template #title>
    {{title}}
  </template>
  <template #content>
    <div :class="gainLossClass">{{formattedValue}}</div>
  </template>
</Card>
</template>

<script lang="ts">
import {computed} from "@vue/reactivity";

export default {
  name: "GainLossCard.vue",
  props: {
    title: {
      type: String,
      required: true
    },
    value: {
      type: Number,
      required: true
    },
    type: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const valueType = {
      PERCENT: 'percent',
      DOLLAR: 'dollar'
    }

    const symbol = computed(() => {
      if (props.type === valueType.PERCENT) {
        return '%'
      } else {
        return '$'
      }
    })

    const formattedValue = computed(() => {
      if (props.value < 0) {
        let percent;
        if (valueType.PERCENT) {
          percent = (props.value * 100).toFixed(2)
        }
        return props.type === valueType.PERCENT ? `${percent}%` : `-$${props.value}`
      } else {
        return props.type === valueType.PERCENT ? `${props.value}%` : `${props.value}`
      }
    })

    const gainLossClass = computed(() => {
      return props.value < 0 ? 'loss' : 'gain'
    })

    return {
      formattedValue,
      gainLossClass,
      symbol
    }
  }
}
</script>

<style scoped>
.loss {
  color: red;
}

.gain {
  color: var(--green-400);
}
</style>
