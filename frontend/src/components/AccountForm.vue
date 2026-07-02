<script setup lang="ts">
import { reactive, ref } from "vue";
import { storeToRefs } from "pinia";

import { useAccountsStore } from "../stores/accounts";
import { useMetaStore } from "../stores/meta";
import { useToastStore } from "../stores/toast";
import { ApiError } from "../api/client";
import type { AccountType, Department, NewAccount } from "../types";

const accountsStore = useAccountsStore();
const metaStore = useMetaStore();
const toast = useToastStore();
const { meta } = storeToRefs(metaStore);

const form = reactive<NewAccount>({
  account_id: "",
  type: "agency",
  seller: "",
  department: "dep_1",
});

const submitting = ref(false);

function randomId() {
  form.account_id = `act_${Math.floor(100000 + Math.random() * 900000)}`;
}

async function submit() {
  if (!form.account_id.trim() || !form.seller) {
    toast.error("Заполните ID кабинета и селлера.");
    return;
  }
  submitting.value = true;
  try {
    await accountsStore.create({ ...form, account_id: form.account_id.trim() });
    toast.success(`Кабинет ${form.account_id.trim()} добавлен.`);
    // Keep type/seller/department to add several in a row, reset only the ID.
    form.account_id = "";
  } catch (err) {
    toast.error(err instanceof ApiError ? err.message : "Не удалось добавить кабинет.");
  } finally {
    submitting.value = false;
  }
}
</script>

<template>
  <form class="card form" @submit.prevent="submit">
    <div class="form__head">
      <h2>Добавить кабинет</h2>
      <p>Данные тестовые — можно добавить несколько подряд.</p>
    </div>

    <div class="grid">
      <div class="field field--id">
        <label class="label" for="account_id">ID кабинета</label>
        <div class="id-row">
          <input
            id="account_id"
            v-model="form.account_id"
            class="input"
            placeholder="act_123456"
            autocomplete="off"
          />
          <button type="button" class="btn btn--ghost" title="Случайный ID" @click="randomId">
            ⟲
          </button>
        </div>
      </div>

      <div class="field">
        <label class="label" for="type">Тип</label>
        <select id="type" v-model="form.type" class="select">
          <option v-for="opt in meta?.types" :key="opt.value" :value="opt.value as AccountType">
            {{ opt.label }}
          </option>
        </select>
      </div>

      <div class="field">
        <label class="label" for="seller">Селлер</label>
        <select id="seller" v-model="form.seller" class="select">
          <option value="" disabled>Выберите селлера</option>
          <option v-for="name in meta?.sellers" :key="name" :value="name">{{ name }}</option>
        </select>
      </div>

      <div class="field">
        <label class="label" for="department">Отдел</label>
        <select id="department" v-model="form.department" class="select">
          <option
            v-for="opt in meta?.departments"
            :key="opt.value"
            :value="opt.value as Department"
          >
            {{ opt.label }}
          </option>
        </select>
      </div>

      <div class="field field--submit">
        <button class="btn btn--primary" type="submit" :disabled="submitting">
          {{ submitting ? "Добавляем…" : "Добавить" }}
        </button>
      </div>
    </div>
  </form>
</template>

<style scoped>
.form {
  padding: 22px 24px;
}

.form__head h2 {
  font-size: 18px;
}

.form__head p {
  margin: 4px 0 18px;
  font-size: 13px;
  color: var(--text-muted);
}

.grid {
  display: grid;
  grid-template-columns: 1.4fr 1fr 1.2fr 1fr auto;
  gap: 16px;
  align-items: end;
}

.id-row {
  display: flex;
  gap: 8px;
}

.id-row .btn {
  padding: 11px 14px;
  flex-shrink: 0;
}

.field--submit .btn {
  width: 100%;
  padding: 12px 22px;
}

@media (max-width: 900px) {
  .grid {
    grid-template-columns: 1fr 1fr;
  }
  .field--id,
  .field--submit {
    grid-column: 1 / -1;
  }
}
</style>
