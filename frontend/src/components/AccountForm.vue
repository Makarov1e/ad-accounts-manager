<script setup lang="ts">
import { reactive, ref } from "vue";
import { storeToRefs } from "pinia";

import { useAccountsStore } from "../stores/accounts";
import { useMetaStore } from "../stores/meta";
import { useToastStore } from "../stores/toast";
import { ApiError } from "../api/client";
import type { AccountType, Department } from "../types";

const accountsStore = useAccountsStore();
const metaStore = useMetaStore();
const toast = useToastStore();
const { meta } = storeToRefs(metaStore);

const form = reactive({
  type: "agency" as AccountType,
  seller: "",
  department: "dep_1" as Department,
});

const idsText = ref("");
const submitting = ref(false);

/** Split the textarea into a de-duplicated list of ids (newline or comma separated). */
function parseIds(): string[] {
  const ids = idsText.value
    .split(/[\n,]+/)
    .map((value) => value.trim())
    .filter(Boolean);
  return [...new Set(ids)];
}

function appendRandomId() {
  const id = `act_${Math.floor(100000 + Math.random() * 900000)}`;
  idsText.value = idsText.value.trim() ? `${idsText.value.trim()}\n${id}` : id;
}

async function submit() {
  const account_ids = parseIds();
  if (!account_ids.length || !form.seller) {
    toast.error("Укажите хотя бы один ID кабинета и селлера.");
    return;
  }
  submitting.value = true;
  try {
    const created = await accountsStore.createMany({ account_ids, ...form });
    toast.success(`Добавлено кабинетов: ${created}`);
    idsText.value = ""; // keep type/seller/department to add more in a row
  } catch (err) {
    toast.error(err instanceof ApiError ? err.message : "Не удалось добавить кабинеты.");
  } finally {
    submitting.value = false;
  }
}
</script>

<template>
  <form class="card form" @submit.prevent="submit">
    <div class="form__head">
      <h2>Добавить кабинет</h2>
      <p>Данные тестовые. Можно добавить несколько за раз — по одному ID на строку.</p>
    </div>

    <div class="ids">
      <label class="label" for="account_ids">
        ID кабинета <span class="hint">— один или несколько (по строке / через запятую)</span>
      </label>
      <div class="id-row">
        <textarea
          id="account_ids"
          v-model="idsText"
          class="input ids__field"
          rows="2"
          placeholder="act_123456&#10;act_654321"
          autocomplete="off"
        ></textarea>
        <button type="button" class="btn btn--ghost id-row__rand" title="Добавить случайный ID" @click="appendRandomId">
          ⟲
        </button>
      </div>
    </div>

    <div class="grid">
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

.hint {
  font-weight: 500;
  text-transform: none;
  letter-spacing: 0;
  color: var(--text-dim);
}

.ids {
  margin-bottom: 16px;
}

.id-row {
  display: flex;
  gap: 8px;
  align-items: stretch;
}

.ids__field {
  resize: vertical;
  min-height: 46px;
  line-height: 1.5;
  font-family: ui-monospace, "SF Mono", Menlo, monospace;
}

.id-row__rand {
  padding: 0 16px;
  flex-shrink: 0;
}

.grid {
  display: grid;
  grid-template-columns: 1fr 1.3fr 1fr auto;
  gap: 16px;
  align-items: end;
}

.field--submit .btn {
  width: 100%;
  padding: 12px 26px;
}

@media (max-width: 900px) {
  .grid {
    grid-template-columns: 1fr 1fr;
  }
  .field--submit {
    grid-column: 1 / -1;
  }
}
</style>
