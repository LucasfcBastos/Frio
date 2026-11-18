import type { ReactNode } from 'react';

import { Card, Skeleton } from '@/components/ui';
import type { Tone } from '@/utils/status';

import styles from './KpiCard.module.css';

export interface KpiCardProps {
  label: string;
  value: ReactNode;
  hint?: string;
  icon: ReactNode;
  tone?: Tone;
  isLoading?: boolean;
}

export function KpiCard({ label, value, hint, icon, tone = 'neutral', isLoading }: KpiCardProps) {
  return (
    <Card as="article" className={[styles.kpi, styles[tone]].join(' ')} data-tone={tone}>
      <div className={styles.top}>
        <p className={styles.label}>{label}</p>
        <span className={styles.icon} aria-hidden="true">
          {icon}
        </span>
      </div>
      {isLoading ? (
        <>
          <Skeleton width="40%" height="var(--text-3xl)" />
          <Skeleton width="70%" height="var(--text-xs)" />
        </>
      ) : (
        <>
          <p className={[styles.value, 'tabular'].join(' ')}>{value}</p>
          {hint && <p className={styles.hint}>{hint}</p>}
        </>
      )}
    </Card>
  );
}
