<script setup lang="ts">
import { computed } from "vue";

import type { AccountStatus } from "../types";
import { statusStyle } from "../utils/status";

const props = defineProps<{ status: AccountStatus; label: string }>();

const style = computed(() => {
  const s = statusStyle(props.status);
  return { color: s.color, background: s.bg, borderColor: s.color };
});
</script>

<template>
  <span class="status" :style="style">
    <span class="status__dot" :style="{ background: style.color }" />
    {{ label }}
  </span>
</template>

<style scoped>
.status {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 5px 11px;
  border-radius: 999px;
  font-size: 12.5px;
  font-weight: 600;
  border: 1px solid;
  white-space: nowrap;
}

.status__dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}
</style>
