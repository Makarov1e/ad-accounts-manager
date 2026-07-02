<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import StatCard from "../components/StatCard.vue";
import { accountsApi } from "../api/accounts";
import { statusStyle } from "../utils/status";
import type { Stats } from "../types";

const stats = ref<Stats | null>(null);
const loading = ref(true);

const maxStatus = computed(() =>
  Math.max(1, ...(stats.value?.by_status.map((s) => s.count) ?? [1])),
);

onMounted(async () => {
  try {
    stats.value = await accountsApi.stats();
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <section>
    <header class="page-head">
      <div>
        <h1>Дашборд</h1>
        <p>Сводка по рекламным кабинетам.</p>
      </div>
      <RouterLink to="/accounts" class="btn btn--primary">Все кабинеты →</RouterLink>
    </header>

    <p v-if="loading" class="muted">Загрузка…</p>

    <template v-else-if="stats">
      <div class="cards">
        <StatCard label="Всего кабинетов" :value="stats.total" accent="var(--teal)" />
        <StatCard
          label="Живых"
          :value="stats.alive"
          accent="#0abab5"
          hint="Выдан + В работе"
        />
        <StatCard label="В бане" :value="stats.banned" accent="#ff5468" />
        <StatCard label="Возвраты" :value="stats.returned" accent="#f5a623" />
      </div>

      <div class="panels">
        <div class="card panel">
          <h2>По статусам</h2>
          <ul class="bars">
            <li v-for="row in stats.by_status" :key="row.value">
              <div class="bars__top">
                <span>{{ row.label }}</span>
                <strong>{{ row.count }}</strong>
              </div>
              <div class="bars__track">
                <span
                  class="bars__fill"
                  :style="{
                    width: `${(row.count / maxStatus) * 100}%`,
                    background: statusStyle(row.value).color,
                  }"
                />
              </div>
            </li>
          </ul>
        </div>

        <div class="card panel">
          <h2>По отделам</h2>
          <div class="dept">
            <div v-for="dep in stats.by_department" :key="dep.value" class="dept__row">
              <div class="dept__head">
                <strong>{{ dep.label }}</strong>
                <span class="muted">{{ dep.total }} всего</span>
              </div>
              <div class="dept__meter">
                <span
                  class="dept__alive"
                  :style="{ width: `${dep.total ? (dep.alive / dep.total) * 100 : 0}%` }"
                />
              </div>
              <div class="dept__legend">
                <span class="dot dot--alive" /> {{ dep.alive }} живых
                <span class="dot dot--dead" /> {{ dep.inactive }} бан/возврат
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </section>
</template>

<style scoped>
.page-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 26px;
}

.page-head h1 {
  font-size: 26px;
}

.page-head p {
  margin: 6px 0 0;
  color: var(--text-muted);
  font-size: 14px;
}

.muted {
  color: var(--text-muted);
}

.cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.panels {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.panel {
  padding: 22px 24px;
}

.panel h2 {
  font-size: 16px;
  margin-bottom: 18px;
}

.bars {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.bars__top {
  display: flex;
  justify-content: space-between;
  font-size: 13.5px;
  margin-bottom: 6px;
}

.bars__track {
  height: 8px;
  border-radius: 999px;
  background: var(--surface-2);
  overflow: hidden;
}

.bars__fill {
  display: block;
  height: 100%;
  border-radius: 999px;
  transition: width 0.4s ease;
}

.dept {
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.dept__head {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  margin-bottom: 8px;
}

.dept__meter {
  height: 10px;
  border-radius: 999px;
  background: rgba(255, 84, 104, 0.35);
  overflow: hidden;
}

.dept__alive {
  display: block;
  height: 100%;
  background: var(--teal);
  transition: width 0.4s ease;
}

.dept__legend {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 8px;
  font-size: 12.5px;
  color: var(--text-muted);
}

.dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  display: inline-block;
}

.dot--alive {
  background: var(--teal);
}

.dot--dead {
  background: #ff5468;
  margin-left: 10px;
}

@media (max-width: 900px) {
  .cards {
    grid-template-columns: repeat(2, 1fr);
  }
  .panels {
    grid-template-columns: 1fr;
  }
}
</style>
