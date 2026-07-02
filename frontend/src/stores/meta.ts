// Reference data (choices + seller list) loaded once for the whole app.

import { defineStore } from "pinia";
import { ref } from "vue";

import { accountsApi } from "../api/accounts";
import type { Meta } from "../types";

export const useMetaStore = defineStore("meta", () => {
  const meta = ref<Meta | null>(null);
  const loading = ref(false);

  async function load() {
    if (meta.value || loading.value) return;
    loading.value = true;
    try {
      meta.value = await accountsApi.meta();
    } finally {
      loading.value = false;
    }
  }

  return { meta, loading, load };
});
