import { defineStore } from "pinia";
import httpClient from "../httpClient";
import { Wallet } from "../types";
import get from "lodash/get";

export const useWallet = defineStore("wallet", {
  state: () => {
    return {
      favoriteWallets: {},
      wallet: {},
      breakdown: {},
      prices: {},
    };
  },
  getters: {
    getPrice() {
      return (walletId: string) => get(this.prices, walletId, null);
    },
  },
  actions: {
    async loadWallet(walletId: string) {
      const response = await httpClient.get(`/accounts/${walletId}`);
      const data = response["data"];
      this.wallet = data;
      await this.loadPrice(this.wallet as Wallet);
    },
    async loadPrice(wallet: Wallet) {
      try {
        // @ts-ignore
        if (!this.prices[wallet.id]) {
          const response = await httpClient.get(`/price/`, {
            params: {
              crypto: wallet.balance_currency,
              native: wallet.native_currency,
            },
          });
          // @ts-ignore
          this.prices[wallet.id] = response.data;
          return response.data;
        }
      } catch (e) {
        console.log("Error loading price", e);
      }
    },
    async loadBulkPrices(wallets: Wallet[]) {
      try {
        const symbols = wallets.map((wallet) => wallet.balance_currency);
        const response = await httpClient.post("/price/bulk/", {
          symbols: symbols,
        });
        const price_data = response.data;
        Object.keys(price_data).forEach((priceKey, i) => {
          const symbol = symbols[i];
          const wallet = wallets[i];
          // @ts-ignore
          this.prices[wallet.id] = price_data[symbol];
        });
        return this.prices;
      } catch (e) {
        console.log("Error loading bulk prices", e);
      }
    },
    async loadFavoriteWallets() {
      try {
        const response = await httpClient.get("accounts/favorites/");
        this.favoriteWallets = response.data;
        return this.favoriteWallets;
      } catch (e) {
        console.log("Error retrieving favorite wallets", e);
        this.favoriteWallets = {};
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
