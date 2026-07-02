// Shared domain types mirroring the backend API payloads.

export type AccountType = "agency" | "bm" | "personal";
export type Department = "dep_1" | "dep_2";
export type AccountStatus = "issued" | "in_work" | "ban" | "return";

export interface Account {
  id: number;
  account_id: string;
  type: AccountType;
  type_display: string;
  seller: string;
  department: Department;
  department_display: string;
  status: AccountStatus;
  status_display: string;
  created_at: string;
  updated_at: string;
}

export interface NewAccount {
  account_id: string;
  type: AccountType;
  seller: string;
  department: Department;
}

export interface NewAccountsBulk {
  account_ids: string[];
  type: AccountType;
  seller: string;
  department: Department;
}

export interface Choice<T extends string = string> {
  value: T;
  label: string;
}

export interface Meta {
  types: Choice<AccountType>[];
  departments: Choice<Department>[];
  statuses: Choice<AccountStatus>[];
  sellers: string[];
}

export interface DepartmentStat {
  value: Department;
  label: string;
  total: number;
  alive: number;
  inactive: number;
}

export interface Stats {
  total: number;
  alive: number;
  banned: number;
  returned: number;
  by_status: Array<Choice<AccountStatus> & { count: number }>;
  by_department: DepartmentStat[];
}

export interface Paginated<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface AccountQuery {
  search?: string;
  department?: Department | "";
  status?: AccountStatus | AccountStatus[] | "";
  ordering?: string;
}
