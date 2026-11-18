import type { DashboardSummary } from '@/types/api';

import { httpClient } from './httpClient';

export const dashboardService = {
  async getSummary(storeId: number): Promise<DashboardSummary> {
    const { data } = await httpClient.get<DashboardSummary>('/dashboard/summary/', {
      params: { store_id: storeId },
    });
    return data;
  },
};
