import type { Paginated, Store } from '@/types/api';

import { httpClient } from './httpClient';

export const storeService = {
  async list(): Promise<Store[]> {
    const { data } = await httpClient.get<Paginated<Store>>('/stores/');
    return data.results;
  },
};
