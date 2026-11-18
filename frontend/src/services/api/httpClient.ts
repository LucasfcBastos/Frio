import axios, { AxiosError } from 'axios';

import type { ApiErrorBody } from '@/types/api';

/** Normalized error thrown by every API service. */
export class ApiError extends Error {
  constructor(
    message: string,
    readonly code: string,
    readonly status: number | null,
    readonly details: unknown = null,
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

export const httpClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api/v1',
  timeout: 10_000,
  headers: { Accept: 'application/json' },
});

httpClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ApiErrorBody>) => {
    const body = error.response?.data?.error;
    if (body) {
      return Promise.reject(
        new ApiError(body.message, body.code, error.response?.status ?? null, body.details),
      );
    }
    const code = error.code === 'ECONNABORTED' ? 'timeout' : 'network_error';
    return Promise.reject(new ApiError(error.message, code, error.response?.status ?? null));
  },
);
