import type { EquipmentStatus, Severity } from '@/types/api';

/** Visual tone shared by badges, dots and cards. */
export type Tone = 'success' | 'warning' | 'critical' | 'neutral' | 'info';

export const STATUS_TONE: Record<EquipmentStatus, Tone> = {
  normal: 'success',
  warning: 'warning',
  critical: 'critical',
};

export const SEVERITY_TONE: Record<Severity, Tone> = {
  low: 'info',
  medium: 'warning',
  high: 'critical',
  critical: 'critical',
};
