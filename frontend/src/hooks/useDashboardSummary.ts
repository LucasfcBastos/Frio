import { useQuery } from '@tanstack/react-query';

import { dashboardService } from '@/services/api';
import { POLLING_INTERVAL_MS } from '@/utils/constants';

import { queryKeys } from './queryKeys';

export function useDashboardSummary(storeId: number | null) {
  return useQuery({
    queryKey: queryKeys.summary(storeId ?? 0),
    queryFn: () => dashboardService.getSummary(storeId as number),
    enabled: storeId !== null,
    refetchInterval: POLLING_INTERVAL_MS,
  });
}
