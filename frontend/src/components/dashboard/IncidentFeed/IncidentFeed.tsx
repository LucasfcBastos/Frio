import { ShieldCheck } from 'lucide-react';

import { EmptyState, ErrorState, Skeleton } from '@/components/ui';
import { useI18n } from '@/contexts/LocaleContext';
import { useNow } from '@/hooks/useNow';
import type { Incident } from '@/types/api';

import { IncidentItem } from '../IncidentItem';
import styles from './IncidentFeed.module.css';

export interface IncidentFeedProps {
  incidents: Incident[] | undefined;
  isLoading: boolean;
  isError: boolean;
  onRetry: () => void;
  onSelect: (incidentId: number) => void;
}

export function IncidentFeed({
  incidents,
  isLoading,
  isError,
  onRetry,
  onSelect,
}: IncidentFeedProps) {
  const { messages } = useI18n();
  const now = useNow(5_000);

  if (isLoading && !incidents) {
    return (
      <div className={styles.list} aria-busy="true" aria-label={messages.states.loading}>
        {[0, 1, 2].map((key) => (
          <Skeleton key={key} height="5rem" radius="md" />
        ))}
      </div>
    );
  }
  if (isError && !incidents) {
    return (
      <ErrorState
        message={messages.states.error}
        retryLabel={messages.states.retry}
        onRetry={onRetry}
      />
    );
  }
  if (!incidents?.length)
    return <EmptyState icon={<ShieldCheck />} title={messages.incidents.empty} />;

  return (
    <ol className={styles.list}>
      {incidents.map((incident) => (
        <li key={incident.id}>
          <IncidentItem incident={incident} now={now} onSelect={onSelect} />
        </li>
      ))}
    </ol>
  );
}
