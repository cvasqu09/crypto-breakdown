import { defineStore } from "pinia";
import httpClient from "../httpClient";

export const useBreakdown = defineStore("breakdown", {
  state: () => {
    return {
      breakdown: {},
    };
  },
  actions: {
    async loadBreakdown() {
      try {
        const response = await httpClient.get("/breakdown/");
        this.breakdown = response.data;
      } catch (e) {
        console.log("Error retrieving breakdowns", e);
        this.breakdown = {};
      }
    },
  },
});
