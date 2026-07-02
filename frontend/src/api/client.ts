// Thin fetch wrapper around the REST API.
//
// The base URL is empty by default so requests hit the relative `/api/...`
// path (proxied to Django by Vite in development). In production set
// `VITE_API_BASE` to the backend origin, e.g. https://api.example.com

const BASE = (import.meta.env.VITE_API_BASE ?? "").replace(/\/$/, "");

export class ApiError extends Error {
  status: number;
  data: unknown;

  constructor(status: number, message: string, data: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
}

export function apiUrl(path: string): string {
  return `${BASE}/api${path}`;
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(apiUrl(path), {
    headers: { "Content-Type": "application/json", ...options.headers },
    ...options,
  });

  if (!response.ok) {
    const data = await response.json().catch(() => null);
    throw new ApiError(response.status, extractError(data, response.statusText), data);
  }

  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

/** Turn a DRF validation error object into a readable single-line message. */
function extractError(data: unknown, fallback: string): string {
  if (data && typeof data === "object") {
    const parts: string[] = [];
    for (const [key, value] of Object.entries(data as Record<string, unknown>)) {
      const text = Array.isArray(value) ? value.join(", ") : String(value);
      parts.push(key === "detail" || key === "non_field_errors" ? text : `${key}: ${text}`);
    }
    if (parts.length) return parts.join("; ");
  }
  return fallback;
}

export const api = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, body: unknown) =>
    request<T>(path, { method: "POST", body: JSON.stringify(body) }),
  patch: <T>(path: string, body: unknown) =>
    request<T>(path, { method: "PATCH", body: JSON.stringify(body) }),
  delete: (path: string) => request<void>(path, { method: "DELETE" }),
};
