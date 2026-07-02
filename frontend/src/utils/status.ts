// Visual styling for each account status (colours picked from the brand palette).

import type { AccountStatus } from "../types";

interface StatusStyle {
  color: string;
  bg: string;
}

const STATUS_STYLES: Record<AccountStatus, StatusStyle> = {
  issued: { color: "#0abab5", bg: "rgba(10, 186, 181, 0.14)" },
  in_work: { color: "#ff058c", bg: "rgba(255, 5, 140, 0.14)" },
  ban: { color: "#ff5468", bg: "rgba(255, 84, 104, 0.14)" },
  return: { color: "#f5a623", bg: "rgba(245, 166, 35, 0.16)" },
};

export function statusStyle(status: AccountStatus): StatusStyle {
  return STATUS_STYLES[status] ?? { color: "var(--text)", bg: "var(--surface-2)" };
}
