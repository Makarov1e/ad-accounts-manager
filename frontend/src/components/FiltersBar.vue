<script setup lang="ts">
import { storeToRefs } from "pinia";

import { useAccountsStore } from "../stores/accounts";
import { useMetaStore } from "../stores/meta";

let searchTimer: ReturnType<typeof setTimeout> | undefined;

const accountsStore = useAccountsStore();
const metaStore = useMetaStore();
const { filters } = storeToRefs(accountsStore);
const { meta } = storeToRefs(metaStore);

function onSearch() {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => accountsStore.fetch(), 300);
}
</script>

<template>
  <div class="filters">
    <div class="filters__search">
      <span class="filters__icon">⌕</span>
      <input
        v-model="filters.search"
        class="input"
        placeholder="Поиск по ID кабинета"
        autocomplete="off"
        @input="onSearch"
      />
    </div>

    <select v-model="filters.department" class="select" @change="accountsStore.fetch()">
      <option value="">Все отделы</option>
      <option v-for="opt in meta?.departments" :key="opt.value" :value="opt.value">
        {{ opt.label }}
      </option>
    </select>

    <select v-model="filters.status" class="select" @change="accountsStore.fetch()">
      <option value="">Все статусы</option>
      <option v-for="opt in meta?.statuses" :key="opt.value" :value="opt.value">
        {{ opt.label }}
      </option>
    </select>

    <button class="btn btn--ghost" @click="accountsStore.resetFilters()">Сбросить</button>
  </div>
</template>

<style scoped>
.filters {
  display: grid;
  grid-template-columns: 1fr 190px 190px auto;
  gap: 12px;
  align-items: center;
}

.filters__search {
  position: relative;
}

.filters__search .input {
  padding-left: 38px;
}

.filters__icon {
  position: absolute;
  left: 13px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  font-size: 17px;
  pointer-events: none;
}

@media (max-width: 800px) {
  .filters {
    grid-template-columns: 1fr 1fr;
  }
  .filters__search {
    grid-column: 1 / -1;
  }
}
</style>
