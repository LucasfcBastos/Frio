import { AlertCircle, AlertTriangle, ChevronRight, Info, ShieldAlert } from 'lucide-react';

import { Badge } from '@/components/ui';
import { useI18n } from '@/contexts/LocaleContext';
import type { Incident } from '@/types/api';
import { formatDuration, formatRelativeTime } from '@/utils/formatters';
import { localizeIncident } from '@/utils/incidents';
import { SEVERITY_TONE } from '@/utils/status';

import styles from './IncidentItem.module.css';

const SEVERITY_ICONS = {
  critical: ShieldAlert,
  high: AlertTriangle,
  medium: AlertCircle,
  low: Info,
} as const;

export interface IncidentItemProps {
  incident: Incident;
  now: Date;
  onSelect?: (incidentId: number) => void;
}

export function IncidentItem({ incident, now, onSelect }: IncidentItemProps) {
  const { messages, format, locale } = useI18n();
  const Icon = SEVERITY_ICONS[incident.severity];
  const { title } = localizeIncident(incident, messages);

  return (
    <button
      type="button"
      className={[styles.item, styles[incident.severity]].join(' ')}
      onClick={() => onSelect?.(incident.id)}
    >
      <span className={styles.icon} aria-hidden="true">
        <Icon />
      </span>
      <span className={styles.body}>
        <span className={styles.top}>
          <span className={styles.title}>{title}</span>
          <Badge tone={SEVERITY_TONE[incident.severity]} size="sm">
            {messages.severity[incident.severity]}
          </Badge>
        </span>
        <span className={styles.equipment}>{incident.equipment_name}</span>
        <span className={styles.meta}>
          <code className={styles.rule} title={messages.incidents.rule}>
            {incident.rule_code}
          </code>
          <span className="tabular">
            {formatRelativeTime(incident.detected_at, now, locale)} ·{' '}
            {format(messages.incidents.detectedIn, {
              time: formatDuration(incident.detection_seconds),
            })}
          </span>
        </span>
      </span>
      <ChevronRight className={styles.chevron} aria-hidden="true" />
    </button>
  );
}
