import { useQuery } from '@tanstack/react-query';

import { incidentService } from '@/services/api';
import type { IncidentStatus } from '@/types/api';
import { POLLING_INTERVAL_MS } from '@/utils/constants';

import { queryKeys } from './queryKeys';

export function useIncidents(storeId: number | null, status?: IncidentStatus) {
  return useQuery({
    queryKey: queryKeys.incidents(storeId ?? 0, status),
    queryFn: () => incidentService.list(storeId as number, status),
    enabled: storeId !== null,
    refetchInterval: POLLING_INTERVAL_MS,
  });
}
