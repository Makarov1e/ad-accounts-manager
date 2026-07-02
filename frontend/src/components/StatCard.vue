<script setup lang="ts">
defineProps<{
  label: string;
  value: number;
  accent?: string;
  hint?: string;
}>();
</script>

<template>
  <div class="stat card">
    <span class="stat__bar" :style="{ background: accent ?? 'var(--gradient)' }" />
    <span class="stat__label">{{ label }}</span>
    <span class="stat__value" :style="{ color: accent ?? 'var(--text)' }">{{ value }}</span>
    <span v-if="hint" class="stat__hint">{{ hint }}</span>
  </div>
</template>

<style scoped>
.stat {
  position: relative;
  overflow: hidden;
  padding: 22px 22px 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.stat__bar {
  position: absolute;
  inset: 0 auto 0 0;
  width: 4px;
}

.stat__label {
  font-size: 13px;
  color: var(--text-muted);
  font-weight: 600;
}

.stat__value {
  font-size: 40px;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -0.02em;
}

.stat__hint {
  font-size: 12px;
  color: var(--text-dim);
}
</style>
