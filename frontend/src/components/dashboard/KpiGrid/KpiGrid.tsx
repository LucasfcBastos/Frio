import { Activity, BellRing, CheckCircle2, Cpu, Timer } from 'lucide-react';

import { Card, ErrorState } from '@/components/ui';
import { useI18n } from '@/contexts/LocaleContext';
import type { DashboardSummary } from '@/types/api';
import { formatDuration, formatNumber } from '@/utils/formatters';

import { KpiCard } from '../KpiCard';
import styles from './KpiGrid.module.css';

export interface KpiGridProps {
  summary: DashboardSummary | undefined;
  isLoading: boolean;
  isError: boolean;
  onRetry: () => void;
}

export function KpiGrid({ summary, isLoading, isError, onRetry }: KpiGridProps) {
  const { messages, format, locale } = useI18n();
  const t = messages.kpi;

  if (isError && !summary) {
    return (
      <Card>
        <ErrorState
          message={messages.states.error}
          retryLabel={messages.states.retry}
          onRetry={onRetry}
        />
      </Card>
    );
  }

  const loading = isLoading || !summary;
  const s = summary;
  return (
    <div className={styles.grid}>
      <KpiCard
        label={t.monitored}
        icon={<Activity />}
        tone="info"
        value={formatNumber(s?.total_equipment, locale)}
        hint={t.monitoredHint}
        isLoading={loading}
      />
      <KpiCard
        label={t.normal}
        icon={<CheckCircle2 />}
        tone="success"
        value={formatNumber(s?.normal_equipment, locale)}
        hint={format(t.normalHint, {
          warning: s?.warning_equipment ?? 0,
          critical: s?.critical_equipment ?? 0,
        })}
        isLoading={loading}
      />
      <KpiCard
        label={t.activeAlerts}
        icon={<BellRing />}
        tone={s && s.active_incidents > 0 ? 'critical' : 'success'}
        value={formatNumber(s?.active_incidents, locale)}
        hint={s && s.active_incidents > 0 ? t.activeAlertsHint : t.noAlertsHint}
        isLoading={loading}
      />
      <KpiCard
        label={t.detectionTime}
        icon={<Timer />}
        tone="info"
        value={
          s?.mean_detection_seconds != null ? formatDuration(s.mean_detection_seconds) : t.noData
        }
        hint={t.detectionTimeHint}
        isLoading={loading}
      />
      <KpiCard
        label={t.firmware}
        icon={<Cpu />}
        tone={s && s.outdated_firmware > 0 ? 'warning' : 'success'}
        value={formatNumber(s?.outdated_firmware, locale)}
        hint={format(t.firmwareHint, { total: s?.total_equipment ?? 0 })}
        isLoading={loading}
      />
    </div>
  );
}
