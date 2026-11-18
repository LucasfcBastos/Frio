import type { IncidentStatus } from '@/types/api';

/** Centralized TanStack Query keys. */
export const queryKeys = {
  stores: ['stores'] as const,
  summary: (storeId: number) => ['dashboard', 'summary', storeId] as const,
  equipment: (storeId: number) => ['equipment', 'list', storeId] as const,
  readings: (equipmentId: number, hours: number) =>
    ['equipment', 'readings', equipmentId, hours] as const,
  incidents: (storeId: number, status?: IncidentStatus) =>
    ['incidents', 'list', storeId, status ?? 'all'] as const,
  incidentDetail: (incidentId: number) => ['incidents', 'detail', incidentId] as const,
};
