<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { storeToRefs } from "pinia";

import AccountsTable from "../components/AccountsTable.vue";
import { accountsApi } from "../api/accounts";
import { useMetaStore } from "../stores/meta";
import type { Account, AccountStatus } from "../types";

const RETURNS_FILTER: AccountStatus[] = ["ban", "return"];

const metaStore = useMetaStore();
const { meta } = storeToRefs(metaStore);

const accounts = ref<Account[]>([]);
const loading = ref(true);

const statuses = computed(() => meta.value?.statuses ?? []);
const exportHref = computed(() => accountsApi.exportUrl({ status: RETURNS_FILTER }));

onMounted(async () => {
  try {
    const page = await accountsApi.list({ status: RETURNS_FILTER, ordering: "-created_at" });
    accounts.value = page.results;
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <section>
    <header class="page-head">
      <div>
        <h1>Возвраты</h1>
        <p>Кабинеты со статусом «Бан» или «Возврат» — {{ accounts.length }} шт.</p>
      </div>
      <a class="btn btn--primary" :href="exportHref">↓ Экспорт в CSV</a>
    </header>

    <AccountsTable
      :accounts="accounts"
      :statuses="statuses"
      :loading="loading"
      :interactive="false"
      empty-text="Нет кабинетов в бане или возврате."
    />
  </section>
</template>

<style scoped>
.page-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 22px;
}

.page-head h1 {
  font-size: 26px;
}

.page-head p {
  margin: 6px 0 0;
  color: var(--text-muted);
  font-size: 14px;
}
</style>
