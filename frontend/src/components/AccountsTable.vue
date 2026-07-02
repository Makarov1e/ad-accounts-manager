<script setup lang="ts">
import StatusBadge from "./StatusBadge.vue";
import StatusControl from "./StatusControl.vue";
import type { Account, AccountStatus, Choice } from "../types";
import { formatDate } from "../utils/format";

withDefaults(
  defineProps<{
    accounts: Account[];
    statuses: Choice<AccountStatus>[];
    loading?: boolean;
    interactive?: boolean;
    emptyText?: string;
  }>(),
  { loading: false, interactive: true, emptyText: "Кабинетов не найдено." },
);

const emit = defineEmits<{
  advance: [id: number];
  set: [id: number, status: AccountStatus];
  remove: [account: Account];
}>();
</script>

<template>
  <div class="table-wrap card">
    <table class="table">
      <thead>
        <tr>
          <th>ID кабинета</th>
          <th>Тип</th>
          <th>Селлер</th>
          <th>Отдел</th>
          <th>Статус</th>
          <th>Дата</th>
          <th v-if="interactive" class="col-actions"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="account in accounts" :key="account.id">
          <td class="mono">{{ account.account_id }}</td>
          <td><span class="pill">{{ account.type_display }}</span></td>
          <td>{{ account.seller }}</td>
          <td class="muted">{{ account.department_display }}</td>
          <td>
            <StatusControl
              v-if="interactive"
              :account="account"
              :statuses="statuses"
              @advance="emit('advance', $event)"
              @set="(id, status) => emit('set', id, status)"
            />
            <StatusBadge v-else :status="account.status" :label="account.status_display" />
          </td>
          <td class="muted nowrap">{{ formatDate(account.created_at) }}</td>
          <td v-if="interactive" class="col-actions">
            <button
              class="remove"
              title="Удалить кабинет"
              @click="emit('remove', account)"
            >
              ✕
            </button>
          </td>
        </tr>

        <tr v-if="!accounts.length && !loading">
          <td :colspan="interactive ? 7 : 6" class="empty">{{ emptyText }}</td>
        </tr>
      </tbody>
    </table>

    <div v-if="loading" class="loading">Загрузка…</div>
  </div>
</template>

<style scoped>
.table-wrap {
  overflow-x: auto;
}

.table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

thead th {
  position: sticky;
  top: 0;
  text-align: left;
  padding: 15px 18px;
  font-size: 11.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  border-bottom: 1px solid var(--border);
  background: var(--surface);
}

tbody td {
  padding: 13px 18px;
  border-bottom: 1px solid var(--border);
  vertical-align: middle;
}

tbody tr:last-child td {
  border-bottom: none;
}

tbody tr:hover td {
  background: rgba(255, 255, 255, 0.02);
}

.mono {
  font-family: ui-monospace, "SF Mono", Menlo, monospace;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.muted {
  color: var(--text-muted);
}

.nowrap {
  white-space: nowrap;
}

.col-actions {
  width: 44px;
  text-align: right;
}

.remove {
  width: 26px;
  height: 26px;
  border-radius: 7px;
  border: 1px solid var(--border);
  background: var(--surface-2);
  color: var(--text-muted);
  font-size: 12px;
  line-height: 1;
}

.remove:hover {
  color: #ff5468;
  border-color: #ff5468;
}

.empty {
  padding: 40px;
  text-align: center;
  color: var(--text-muted);
}

.loading {
  padding: 16px;
  text-align: center;
  color: var(--text-muted);
  font-size: 13px;
}
</style>
