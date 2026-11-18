import type { Incident, IncidentDetail, IncidentStatus, Paginated } from '@/types/api';

import { httpClient } from './httpClient';

export const incidentService = {
  async list(storeId: number, status?: IncidentStatus): Promise<Incident[]> {
    const { data } = await httpClient.get<Paginated<Incident>>('/incidents/', {
      params: { store_id: storeId, status, page_size: 50 },
    });
    return data.results;
  },

  async getDetail(incidentId: number): Promise<IncidentDetail> {
    const { data } = await httpClient.get<IncidentDetail>(`/incidents/${incidentId}/`);
    return data;
  },
};
