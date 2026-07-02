// Minimal transient notification store.

import { defineStore } from "pinia";
import { ref } from "vue";

export interface Toast {
  id: number;
  message: string;
  kind: "success" | "error";
}

export const useToastStore = defineStore("toast", () => {
  const toasts = ref<Toast[]>([]);
  let counter = 0;

  function push(message: string, kind: Toast["kind"] = "success") {
    const id = ++counter;
    toasts.value.push({ id, message, kind });
    setTimeout(() => dismiss(id), 3200);
  }

  function dismiss(id: number) {
    toasts.value = toasts.value.filter((t) => t.id !== id);
  }

  return {
    toasts,
    dismiss,
    success: (m: string) => push(m, "success"),
    error: (m: string) => push(m, "error"),
  };
});
