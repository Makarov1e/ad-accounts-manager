<script setup lang="ts">
import { computed, onMounted } from "vue";
import { storeToRefs } from "pinia";

import AccountForm from "../components/AccountForm.vue";
import AccountsTable from "../components/AccountsTable.vue";
import FiltersBar from "../components/FiltersBar.vue";
import { accountsApi } from "../api/accounts";
import { useAccountsStore } from "../stores/accounts";
import { useMetaStore } from "../stores/meta";
import { useToastStore } from "../stores/toast";
import type { Account, AccountStatus } from "../types";

const accountsStore = useAccountsStore();
const metaStore = useMetaStore();
const toast = useToastStore();

const { accounts, count, loading, error, filters } = storeToRefs(accountsStore);
const { meta } = storeToRefs(metaStore);

const statuses = computed(() => meta.value?.statuses ?? []);
const exportHref = computed(() =>
  accountsApi.exportUrl({
    search: filters.value.search.trim(),
    department: filters.value.department,
    status: filters.value.status,
    ordering: filters.value.ordering,
  }),
);

onMounted(() => accountsStore.fetch());

async function advance(id: number) {
  try {
    await accountsStore.advance(id);
  } catch {
    toast.error("Не удалось изменить статус.");
  }
}

async function setStatus(id: number, status: AccountStatus) {
  try {
    await accountsStore.setStatus(id, status);
  } catch {
    toast.error("Не удалось изменить статус.");
  }
}

async function remove(account: Account) {
  if (!confirm(`Удалить кабинет ${account.account_id}?`)) return;
  try {
    await accountsStore.remove(account.id);
    toast.success("Кабинет удалён.");
  } catch {
    toast.error("Не удалось удалить кабинет.");
  }
}
</script>

<template>
  <section>
    <header class="page-head">
      <div>
        <h1>Кабинеты</h1>
        <p>Всего: {{ count }}</p>
      </div>
      <a class="btn" :href="exportHref">↓ Экспорт CSV</a>
    </header>

    <AccountForm />

    <div class="toolbar">
      <FiltersBar />
    </div>

    <p v-if="error" class="error">{{ error }}</p>

    <AccountsTable
      :accounts="accounts"
      :statuses="statuses"
      :loading="loading"
      @advance="advance"
      @set="setStatus"
      @remove="remove"
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

.toolbar {
  margin: 22px 0 16px;
}

.error {
  color: #ff5468;
  font-size: 14px;
  margin: 0 0 14px;
}
</style>
