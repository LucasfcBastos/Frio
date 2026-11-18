import { useMemo, useState } from 'react';

import {
  CriticalBanner,
  EquipmentGrid,
  IncidentDrawer,
  IncidentFeed,
  KpiGrid,
  TemperatureChart,
} from '@/components/dashboard';
import { AppLayout } from '@/components/layout';
import { Card, ErrorState } from '@/components/ui';
import { useI18n } from '@/contexts/LocaleContext';
import { useStoreContext } from '@/contexts/StoreContext';
import { useDashboardSummary } from '@/hooks/useDashboardSummary';
import { useEquipmentList } from '@/hooks/useEquipmentList';
import { useEquipmentReadings } from '@/hooks/useEquipmentReadings';
import { useIncidentDetail } from '@/hooks/useIncidentDetail';
import { useIncidents } from '@/hooks/useIncidents';
import { useSelectedEquipment } from '@/hooks/useSelectedEquipment';
import { CHART_HOURS } from '@/utils/constants';

import styles from './DashboardPage.module.css';

/** Composition only: hooks fetch, components render. */
export function DashboardPage() {
  const { messages, format } = useI18n();
  const store = useStoreContext();
  const storeId = store.selectedStoreId;

  const summary = useDashboardSummary(storeId);
  const equipment = useEquipmentList(storeId);
  const incidents = useIncidents(storeId, 'active');
  const { selectedId, select } = useSelectedEquipment(equipment.data);
  const readings = useEquipmentReadings(selectedId, CHART_HOURS);

  const [openIncidentId, setOpenIncidentId] = useState<number | null>(null);
  const incidentDetail = useIncidentDetail(openIncidentId);

  const criticalIncident = useMemo(
    () => incidents.data?.find((incident) => incident.severity === 'critical'),
    [incidents.data],
  );
  const selectedName = equipment.data?.find((item) => item.id === selectedId)?.name;

  return (
    <AppLayout
      header={{
        overallStatus: summary.data?.overall_status,
        lastUpdatedAt: summary.data?.last_updated_at,
      }}
    >
      {store.isError ? (
        <Card>
          <ErrorState
            message={messages.states.error}
            retryLabel={messages.states.retry}
            onRetry={store.refetch}
          />
        </Card>
      ) : (
        <div className={styles.page}>
          <div className={styles.heading}>
            <h1 className={styles.title}>{messages.dashboard.title}</h1>
            {store.selectedStore && (
              <p className={styles.subtitle}>
                {store.selectedStore.organization_name} ·{' '}
                {format(messages.dashboard.subtitle, {
                  store: store.selectedStore.name,
                  city: store.selectedStore.city,
                  state: store.selectedStore.state,
                })}
              </p>
            )}
          </div>

          {criticalIncident && (
            <CriticalBanner incident={criticalIncident} onDetails={setOpenIncidentId} />
          )}

          <KpiGrid
            summary={summary.data}
            isLoading={summary.isLoading}
            isError={summary.isError}
            onRetry={() => void summary.refetch()}
          />

          <div className={styles.split}>
            <Card
              className={styles.chartCard}
              title={
                <>
                  {format(messages.dashboard.chartSection, { hours: CHART_HOURS })}
                  {selectedName && <span className={styles.chartName}> · {selectedName}</span>}
                </>
              }
            >
              <TemperatureChart
                series={readings.data}
                isLoading={readings.isLoading}
                isError={readings.isError}
                onRetry={() => void readings.refetch()}
                hasSelection={selectedId !== null || equipment.isLoading}
              />
            </Card>

            <Card className={styles.feedCard} title={messages.dashboard.incidentSection}>
              <IncidentFeed
                incidents={incidents.data}
                isLoading={incidents.isLoading}
                isError={incidents.isError}
                onRetry={() => void incidents.refetch()}
                onSelect={setOpenIncidentId}
              />
            </Card>
          </div>

          <Card
            title={messages.dashboard.equipmentSection}
            actions={<span className={styles.hint}>{messages.dashboard.equipmentHint}</span>}
          >
            <EquipmentGrid
              equipment={equipment.data}
              isLoading={equipment.isLoading}
              isError={equipment.isError}
              onRetry={() => void equipment.refetch()}
              selectedId={selectedId}
              onSelect={select}
            />
          </Card>
        </div>
      )}

      <IncidentDrawer
        open={openIncidentId !== null}
        onClose={() => setOpenIncidentId(null)}
        detail={incidentDetail.data}
        isLoading={incidentDetail.isLoading}
        isError={incidentDetail.isError}
        onRetry={() => void incidentDetail.refetch()}
      />
    </AppLayout>
  );
}
