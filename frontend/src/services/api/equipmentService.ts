import type { EquipmentOverview, Paginated, ReadingSeries } from '@/types/api';

import { httpClient } from './httpClient';

export const equipmentService = {
  async list(storeId: number): Promise<EquipmentOverview[]> {
    const { data } = await httpClient.get<Paginated<EquipmentOverview>>('/equipment/', {
      params: { store_id: storeId, page_size: 200 },
    });
    return data.results;
  },

  async getReadings(equipmentId: number, hours = 6): Promise<ReadingSeries> {
    const { data } = await httpClient.get<ReadingSeries>(`/equipment/${equipmentId}/readings/`, {
      params: { hours },
    });
    return data;
  },
};
