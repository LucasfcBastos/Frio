import { AlertTriangle, CheckCircle2, ShieldAlert } from 'lucide-react';

import { Badge } from '@/components/ui';
import { useI18n } from '@/contexts/LocaleContext';
import type { EquipmentStatus } from '@/types/api';
import { STATUS_TONE } from '@/utils/status';

const ICONS = { normal: CheckCircle2, warning: AlertTriangle, critical: ShieldAlert } as const;

export interface StatusBadgeProps {
  status: EquipmentStatus;
  size?: 'sm' | 'md';
}

/** Status shown with icon + text, never by color alone (WCAG 1.4.1). */
export function StatusBadge({ status, size = 'md' }: StatusBadgeProps) {
  const { messages } = useI18n();
  const Icon = ICONS[status];
  return (
    <Badge tone={STATUS_TONE[status]} icon={<Icon />} size={size}>
      {messages.status[status]}
    </Badge>
  );
}
