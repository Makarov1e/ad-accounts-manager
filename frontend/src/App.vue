<script setup lang="ts">
import { onMounted } from "vue";

import ToastHost from "./components/ToastHost.vue";
import { useMetaStore } from "./stores/meta";

const nav = [
  { to: "/", label: "Дашборд" },
  { to: "/accounts", label: "Кабинеты" },
  { to: "/returns", label: "Возвраты" },
];

onMounted(() => useMetaStore().load());
</script>

<template>
  <div class="app">
    <header class="topbar">
      <div class="brand">
        <span class="brand__mark">L</span>
        <div class="brand__text">
          <strong>Lidera</strong>
          <span>Учёт рекламных кабинетов</span>
        </div>
      </div>
      <nav class="nav">
        <RouterLink
          v-for="item in nav"
          :key="item.to"
          :to="item.to"
          class="nav__link"
        >
          {{ item.label }}
        </RouterLink>
      </nav>
    </header>

    <main class="content">
      <RouterView />
    </main>

    <ToastHost />
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 20;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 16px clamp(16px, 5vw, 56px);
  background: rgba(5, 5, 6, 0.72);
  backdrop-filter: blur(14px);
  border-bottom: 1px solid var(--border);
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand__mark {
  display: grid;
  place-items: center;
  width: 40px;
  height: 40px;
  border-radius: 11px;
  font-weight: 800;
  font-size: 20px;
  color: #fff;
  background: var(--gradient);
  box-shadow: 0 8px 22px rgba(255, 5, 140, 0.35);
}

.brand__text {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.brand__text strong {
  font-size: 16px;
  letter-spacing: 0.04em;
}

.brand__text span {
  font-size: 12px;
  color: var(--text-muted);
}

.nav {
  display: flex;
  gap: 6px;
  padding: 5px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 999px;
}

.nav__link {
  padding: 8px 18px;
  border-radius: 999px;
  font-size: 14px;
  font-weight: 600;
  color: var(--text-muted);
  transition: color 0.15s ease, background 0.15s ease;
}

.nav__link:hover {
  color: var(--text);
}

.nav__link.is-active {
  color: #fff;
  background: var(--gradient);
}

.content {
  max-width: 1180px;
  margin: 0 auto;
  padding: clamp(20px, 4vw, 40px) clamp(16px, 5vw, 56px) 72px;
}

@media (max-width: 640px) {
  .topbar {
    flex-direction: column;
    align-items: stretch;
    gap: 14px;
  }
  .nav {
    justify-content: center;
  }
}
</style>
