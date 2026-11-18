import { useQuery } from '@tanstack/react-query';

import { incidentService } from '@/services/api';
import { POLLING_INTERVAL_MS } from '@/utils/constants';

import { queryKeys } from './queryKeys';

export function useIncidentDetail(incidentId: number | null) {
  return useQuery({
    queryKey: queryKeys.incidentDetail(incidentId ?? 0),
    queryFn: () => incidentService.getDetail(incidentId as number),
    enabled: incidentId !== null,
    refetchInterval: POLLING_INTERVAL_MS,
  });
}
