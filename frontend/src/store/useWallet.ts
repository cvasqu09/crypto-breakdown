import { defineStore } from "pinia";
import httpClient from "../httpClient";

export const useWallet = defineStore("wallet", {
  state: () => {
    return {
      favoriteWallets: [],
    };
  },
  actions: {
    async loadFavoriteWallets() {
      try {
        const response = await httpClient.get("accounts/favorites/");
        this.favoriteWallets = response.data;
        return this.favoriteWallets;
      } catch (e) {
        console.log("Error retrieving favorite wallets", e);
        this.favoriteWallets = [];
      }
    },
  },
});
