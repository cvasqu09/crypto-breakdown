import { createApp } from "vue";
import App from "./App.vue";
import ToastService from "primevue/toastservice";

import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import Button from "primevue/button";
import Menu from "primevue/menu";
import Dialog from "primevue/dialog";
import Card from "primevue/card";
import Calendar from "primevue/calendar";
import Column from "primevue/column";
import DataTable from "primevue/datatable";
import ConfirmationService from "primevue/confirmationservice";
import ConfirmDialog from "primevue/confirmdialog";

import TabMenu from "primevue/tabmenu";
import InputText from "primevue/inputtext";

import "primevue/resources/themes/md-dark-deeppurple/theme.css"; //theme
import "primevue/resources/primevue.min.css"; //core css
import "primeicons/primeicons.css"; //icons
import "primeflex/primeflex.css";
import HomePage from "./components/HomePage.vue";
import WalletDetailPage from "./components/WalletDetailPage.vue";
import AccountDetailPage from "./components/AccountDetailPage.vue";
import ImportPage from "./components/ImportPage.vue";

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
  {
    path: "/imports",
    component: ImportPage,
    name: "imports",
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

const app = createApp(App);
app.use(ToastService);
app.use(ConfirmationService);
app.use(router);
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);
app.use(pinia);
app.use(PrimeVue);
app.component("Button", Button);
app.component("Dialog", Dialog);
app.component("Menu", Menu);
app.component("InputText", InputText);
app.component("TabMenu", TabMenu);
app.component("Card", Card);
app.component("Calendar", Calendar);
app.component("DataTable", DataTable);
app.component("Column", Column);
app.component("ConfirmDialog", ConfirmDialog);
app.mount("#app");
