import { keepPreviousData, useQuery } from '@tanstack/react-query';

import { equipmentService } from '@/services/api';
import { POLLING_INTERVAL_MS } from '@/utils/constants';

import { queryKeys } from './queryKeys';

export function useEquipmentList(storeId: number | null) {
  return useQuery({
    queryKey: queryKeys.equipment(storeId ?? 0),
    queryFn: () => equipmentService.list(storeId as number),
    enabled: storeId !== null,
    refetchInterval: POLLING_INTERVAL_MS,
    placeholderData: keepPreviousData,
  });
}
