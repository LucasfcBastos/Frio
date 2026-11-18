import { useQuery } from '@tanstack/react-query';

import { storeService } from '@/services/api';

import { queryKeys } from './queryKeys';

export function useStores() {
  return useQuery({ queryKey: queryKeys.stores, queryFn: storeService.list, staleTime: 60_000 });
}
