import { createApp } from "vue";
import App from "./App.vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import Button from "primevue/button";
import Menu from "primevue/menu";
import Dialog from "primevue/dialog";
import TabMenu from "primevue/tabmenu";
import "primevue/resources/themes/md-dark-deeppurple/theme.css"; //theme
import "primevue/resources/primevue.min.css"; //core css
import "primeicons/primeicons.css"; //icons
import "primeflex/primeflex.css";
import HomePage from "./components/HomePage.vue";
import AccountPage from "./components/AccountPage.vue";
import AccountDetailPage from "./components/AccountDetailPage.vue";

import { createRouter, createWebHashHistory } from "vue-router";

const routes = [
  { path: "/", redirect: "/home" },
  { path: "/home", component: HomePage, name: "home" },
  { path: "/account", component: AccountPage, name: "account" },
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
app.use(router);
app.use(createPinia());
app.use(PrimeVue);
app.component("Button", Button);
app.component("Dialog", Dialog);
app.component("Menu", Menu);
app.component("TabMenu", TabMenu);
app.mount("#app");
