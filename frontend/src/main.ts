import { createApp } from "vue";
import App from "./App.vue";
import ToastService from "primevue/toastservice";

import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import Button from "primevue/button";
import Menu from "primevue/menu";
import Dialog from "primevue/dialog";
import Card from "primevue/card";
import TabMenu from "primevue/tabmenu";
import "primevue/resources/themes/md-dark-deeppurple/theme.css"; //theme
import "primevue/resources/primevue.min.css"; //core css
import "primeicons/primeicons.css"; //icons
import "primeflex/primeflex.css";
import HomePage from "./components/HomePage.vue";
import WalletDetailPage from "./components/WalletDetailPage.vue";
import AccountDetailPage from "./components/AccountDetailPage.vue";

import { createRouter, createWebHashHistory } from "vue-router";
import WalletPage from "./components/WalletPage.vue";

const routes = [
  { path: "/", redirect: "/home" },
  { path: "/home", component: HomePage, name: "home" },
  { path: "/wallet", component: WalletPage, name: "wallet" },
  { path: "/wallet/:id", component: WalletDetailPage, name: "wallet-detail" },
  {
    path: "/account/:id",
    component: AccountDetailPage,
    name: "account-detail",
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

const app = createApp(App);
app.use(ToastService);
app.use(router);
app.use(createPinia());
app.use(PrimeVue);
app.component("Button", Button);
app.component("Dialog", Dialog);
app.component("Menu", Menu);
app.component("TabMenu", TabMenu);
app.component("Card", Card);
app.mount("#app");
