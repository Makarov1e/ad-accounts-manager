import { createRouter, createWebHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "dashboard",
    component: () => import("../views/DashboardView.vue"),
    meta: { title: "Дашборд" },
  },
  {
    path: "/accounts",
    name: "accounts",
    component: () => import("../views/AccountsView.vue"),
    meta: { title: "Кабинеты" },
  },
  {
    path: "/returns",
    name: "returns",
    component: () => import("../views/ReturnsView.vue"),
    meta: { title: "Возвраты" },
  },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
  linkExactActiveClass: "is-active",
});
