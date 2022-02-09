<template>
  <TabMenu :model="tabs">
  </TabMenu>
</template>

<script>
export default {
  name: "TheNavBar",
  setup() {
    const tabs = [
      {label: 'Home', icon: 'pi pi-home', to: '/'},
      {label: 'Wallets', icon: 'pi pi-wallet', to: '/wallet'},
    ]
    return {
      tabs
    }
  }

}
</script>

<style scoped>

</style>
