import { keepPreviousData, useQuery } from '@tanstack/react-query';

import { equipmentService } from '@/services/api';
import { CHART_HOURS, POLLING_INTERVAL_MS } from '@/utils/constants';

import { queryKeys } from './queryKeys';

export function useEquipmentReadings(equipmentId: number | null, hours = CHART_HOURS) {
  return useQuery({
    queryKey: queryKeys.readings(equipmentId ?? 0, hours),
    queryFn: () => equipmentService.getReadings(equipmentId as number, hours),
    enabled: equipmentId !== null,
    refetchInterval: POLLING_INTERVAL_MS,
    placeholderData: keepPreviousData,
  });
}
