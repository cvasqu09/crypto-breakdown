import { defineStore } from "pinia";
import httpClient from "../httpClient";

export const useWallet = defineStore("wallet", {
  state: () => {
    return {
      favoriteWallets: [],
      breakdown: {},
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
    async toggleFavoriteWallet(id: string) {
      try {
        await httpClient.post("/accounts/favorites/", { ids: [id] });
        await this.loadFavoriteWallets();
      } catch (e) {
        console.log("Error toggling favorite wallets", e);
      }
    },
    async loadBreakdown() {
      try {
        const response = await httpClient.get("/accounts/breakdown/");
        this.breakdown = response.data;
      } catch (e) {
        console.log("Error toggling favorite wallets", e);
      }
    },
    async refreshWallet(id: string) {
      try {
        await httpClient.post(`/refresh/buys/?account_id=${id}`);
      } catch (e) {
        console.log("Error refreshing buys for ", id);
      }
    },
  },
});
