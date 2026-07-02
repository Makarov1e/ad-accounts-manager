<script setup lang="ts">
import { ref } from "vue";

import { onClickOutside } from "../composables/onClickOutside";
import StatusBadge from "./StatusBadge.vue";
import type { Account, AccountStatus, Choice } from "../types";

const props = defineProps<{
  account: Account;
  statuses: Choice<AccountStatus>[];
}>();

const emit = defineEmits<{
  advance: [id: number];
  set: [id: number, status: AccountStatus];
}>();

const menuOpen = ref(false);
const root = ref<HTMLElement | null>(null);
onClickOutside(root, () => (menuOpen.value = false));

function pick(status: AccountStatus) {
  menuOpen.value = false;
  if (status !== props.account.status) emit("set", props.account.id, status);
}
</script>

<template>
  <div ref="root" class="control">
    <button
      class="control__badge"
      title="Клик — следующий статус"
      @click="emit('advance', account.id)"
    >
      <StatusBadge :status="account.status" :label="account.status_display" />
    </button>

    <button
      class="control__caret"
      title="Выбрать статус вручную"
      :aria-expanded="menuOpen"
      @click="menuOpen = !menuOpen"
    >
      ▾
    </button>

    <div v-if="menuOpen" class="menu">
      <button
        v-for="option in statuses"
        :key="option.value"
        class="menu__item"
        :class="{ 'is-current': option.value === account.status }"
        @click="pick(option.value)"
      >
        <StatusBadge :status="option.value" :label="option.label" />
      </button>
    </div>
  </div>
</template>

<style scoped>
.control {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 2px;
}

.control__badge {
  background: none;
  border: none;
  padding: 0;
  border-radius: 999px;
  transition: transform 0.08s ease;
}

.control__badge:hover {
  transform: translateY(-1px);
}

.control__caret {
  display: grid;
  place-items: center;
  width: 22px;
  height: 22px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--surface-2);
  color: var(--text-muted);
  font-size: 11px;
  line-height: 1;
}

.control__caret:hover {
  color: var(--text);
  border-color: var(--border-strong);
}

.menu {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  z-index: 30;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 6px;
  background: var(--bg-elevated);
  border: 1px solid var(--border-strong);
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow);
}

.menu__item {
  display: flex;
  padding: 4px;
  background: none;
  border: none;
  border-radius: 8px;
}

.menu__item:hover {
  background: var(--surface-2);
}

.menu__item.is-current {
  outline: 1px solid var(--border-strong);
}
</style>
