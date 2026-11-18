import { ArrowRight, Siren } from 'lucide-react';

import { Button } from '@/components/ui';
import { useI18n } from '@/contexts/LocaleContext';
import { useNow } from '@/hooks/useNow';
import type { Incident } from '@/types/api';
import { formatRelativeTime } from '@/utils/formatters';
import { localizeIncident } from '@/utils/incidents';

import styles from './CriticalBanner.module.css';

export interface CriticalBannerProps {
  incident: Incident;
  onDetails: (incidentId: number) => void;
}

export function CriticalBanner({ incident, onDetails }: CriticalBannerProps) {
  const { messages, format, locale } = useI18n();
  const now = useNow();
  const { title } = localizeIncident(incident, messages);

  return (
    <section className={styles.banner} role="alert" aria-live="assertive">
      <span className={styles.icon} aria-hidden="true">
        <Siren />
      </span>
      <div className={styles.text}>
        <p className={styles.label}>{messages.banner.label}</p>
        <p className={styles.title}>{title}</p>
        <p className={[styles.meta, 'tabular'].join(' ')}>
          {format(messages.banner.meta, {
            equipment: incident.equipment_name,
            time: formatRelativeTime(incident.started_at, now, locale),
          })}
        </p>
      </div>
      <Button variant="onCritical" icon={<ArrowRight />} onClick={() => onDetails(incident.id)}>
        {messages.banner.details}
      </Button>
    </section>
  );
}
