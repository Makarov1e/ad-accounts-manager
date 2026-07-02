// API calls for accounts, dashboard stats and CSV export.

import { api, apiUrl } from "./client";
import type {
  Account,
  AccountQuery,
  Meta,
  NewAccount,
  Paginated,
  Stats,
} from "../types";

/** Build a query string, expanding array values (e.g. repeated `status`). */
function buildQuery(params: AccountQuery): string {
  const search = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value === undefined || value === null || value === "") continue;
    if (Array.isArray(value)) {
      value.forEach((item) => search.append(key, item));
    } else {
      search.append(key, String(value));
    }
  }
  const qs = search.toString();
  return qs ? `?${qs}` : "";
}

export const accountsApi = {
  list: (params: AccountQuery = {}) =>
    api.get<Paginated<Account>>(`/accounts/${buildQuery(params)}`),

  create: (payload: NewAccount) => api.post<Account>("/accounts/", payload),

  advance: (id: number) => api.post<Account>(`/accounts/${id}/advance/`, {}),

  setStatus: (id: number, status: string) =>
    api.patch<Account>(`/accounts/${id}/`, { status }),

  remove: (id: number) => api.delete(`/accounts/${id}/`),

  stats: () => api.get<Stats>("/accounts/stats/"),

  meta: () => api.get<Meta>("/accounts/meta/"),

  /** URL for the CSV export honouring the given filters (used in an anchor). */
  exportUrl: (params: AccountQuery = {}) =>
    apiUrl(`/accounts/export/${buildQuery(params)}`),
};
