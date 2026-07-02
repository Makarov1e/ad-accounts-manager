<script setup lang="ts">
import { storeToRefs } from "pinia";

import { useToastStore } from "../stores/toast";

const toastStore = useToastStore();
const { toasts } = storeToRefs(toastStore);
</script>

<template>
  <div class="toast-host">
    <TransitionGroup name="toast">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="toast"
        :class="`toast--${toast.kind}`"
        @click="toastStore.dismiss(toast.id)"
      >
        {{ toast.message }}
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.toast-host {
  position: fixed;
  right: 20px;
  bottom: 20px;
  z-index: 100;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.toast {
  padding: 12px 16px;
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  background: var(--surface-2);
  border: 1px solid var(--border-strong);
  box-shadow: var(--shadow);
  cursor: pointer;
  max-width: 340px;
}

.toast--success {
  border-color: var(--teal);
}

.toast--error {
  border-color: #ff5468;
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.25s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
