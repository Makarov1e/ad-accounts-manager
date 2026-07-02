// State for the main accounts table: the list plus its active filters.

import { defineStore } from "pinia";
import { reactive, ref } from "vue";

import { accountsApi } from "../api/accounts";
import type { Account, AccountQuery, AccountStatus, Department, NewAccount } from "../types";

interface Filters {
  search: string;
  department: Department | "";
  status: AccountStatus | "";
  ordering: string;
}

export const useAccountsStore = defineStore("accounts", () => {
  const accounts = ref<Account[]>([]);
  const count = ref(0);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const filters = reactive<Filters>({
    search: "",
    department: "",
    status: "",
    ordering: "-created_at",
  });

  function query(): AccountQuery {
    return {
      search: filters.search.trim(),
      department: filters.department,
      status: filters.status,
      ordering: filters.ordering,
    };
  }

  async function fetch() {
    loading.value = true;
    error.value = null;
    try {
      const page = await accountsApi.list(query());
      accounts.value = page.results;
      count.value = page.count;
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Не удалось загрузить кабинеты.";
    } finally {
      loading.value = false;
    }
  }

  function resetFilters() {
    filters.search = "";
    filters.department = "";
    filters.status = "";
    filters.ordering = "-created_at";
    return fetch();
  }

  // When a status filter is active, changing a row's status may drop it from
  // the current view, so refetch. Otherwise patch it in place for instant UX.
  function applyChange(updated: Account) {
    if (filters.status) {
      return fetch();
    }
    const index = accounts.value.findIndex((a) => a.id === updated.id);
    if (index !== -1) accounts.value[index] = updated;
  }

  async function create(payload: NewAccount) {
    await accountsApi.create(payload);
    await fetch();
  }

  async function advance(id: number) {
    applyChange(await accountsApi.advance(id));
  }

  async function setStatus(id: number, status: AccountStatus) {
    applyChange(await accountsApi.setStatus(id, status));
  }

  async function remove(id: number) {
    await accountsApi.remove(id);
    await fetch();
  }

  return {
    accounts,
    count,
    loading,
    error,
    filters,
    fetch,
    resetFilters,
    create,
    advance,
    setStatus,
    remove,
  };
});
