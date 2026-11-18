import { useI18n } from '@/contexts/LocaleContext';
import { useNow } from '@/hooks/useNow';
import { formatRelativeTime } from '@/utils/formatters';

import styles from './LiveIndicator.module.css';

export interface LiveIndicatorProps {
  lastUpdatedAt: string | null | undefined;
}

export function LiveIndicator({ lastUpdatedAt }: LiveIndicatorProps) {
  const { messages, format, locale } = useI18n();
  const now = useNow();
  const label = lastUpdatedAt
    ? format(messages.header.updatedAgo, {
        time: formatRelativeTime(lastUpdatedAt, now, locale),
      })
    : messages.header.waitingData;

  return (
    <p className={styles.live} aria-live="polite">
      <span className={[styles.pulse, lastUpdatedAt && styles.active].filter(Boolean).join(' ')} />
      <span className="visually-hidden">{messages.header.live}: </span>
      <span className="tabular">{label}</span>
    </p>
  );
}
