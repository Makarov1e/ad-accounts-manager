// Call `handler` when a pointer event happens outside the referenced element.
// Small local replacement for the equivalent @vueuse/core helper.

import { onBeforeUnmount, onMounted, type Ref } from "vue";

export function onClickOutside(
  target: Ref<HTMLElement | null>,
  handler: (event: MouseEvent) => void,
): void {
  function listener(event: MouseEvent) {
    const el = target.value;
    if (el && !el.contains(event.target as Node)) {
      handler(event);
    }
  }

  onMounted(() => document.addEventListener("click", listener, true));
  onBeforeUnmount(() => document.removeEventListener("click", listener, true));
}
