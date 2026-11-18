import { AlertTriangle, CheckCircle2, ShieldAlert } from 'lucide-react';

import { useI18n } from '@/contexts/LocaleContext';
import type { EquipmentStatus } from '@/types/api';

import styles from './OverallStatus.module.css';

const ICONS = { normal: CheckCircle2, warning: AlertTriangle, critical: ShieldAlert } as const;

export interface OverallStatusProps {
  status: EquipmentStatus;
}

export function OverallStatus({ status }: OverallStatusProps) {
  const { messages } = useI18n();
  const Icon = ICONS[status];
  return (
    <p className={[styles.status, styles[status]].join(' ')} role="status">
      <span className={styles.dot} aria-hidden="true" />
      <Icon className={styles.icon} aria-hidden="true" />
      <span className={styles.label}>{messages.header.overall[status]}</span>
    </p>
  );
}
