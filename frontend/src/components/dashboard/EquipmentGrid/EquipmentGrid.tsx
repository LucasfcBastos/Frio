import { PackageOpen } from 'lucide-react';

import { EmptyState, ErrorState, Skeleton } from '@/components/ui';
import { useI18n } from '@/contexts/LocaleContext';
import type { EquipmentOverview } from '@/types/api';

import { EquipmentCard } from '../EquipmentCard';
import styles from './EquipmentGrid.module.css';

export interface EquipmentGridProps {
  equipment: EquipmentOverview[] | undefined;
  isLoading: boolean;
  isError: boolean;
  onRetry: () => void;
  selectedId: number | null;
  onSelect: (equipmentId: number) => void;
}

const SKELETON_CARDS = 4;

export function EquipmentGrid({
  equipment,
  isLoading,
  isError,
  onRetry,
  selectedId,
  onSelect,
}: EquipmentGridProps) {
  const { messages } = useI18n();

  if (isLoading && !equipment) {
    return (
      <div className={styles.grid} aria-busy="true" aria-label={messages.states.loading}>
        {Array.from({ length: SKELETON_CARDS }, (_, index) => (
          <Skeleton key={index} height="17rem" radius="lg" />
        ))}
      </div>
    );
  }
  if (isError && !equipment) {
    return (
      <ErrorState
        message={messages.states.error}
        retryLabel={messages.states.retry}
        onRetry={onRetry}
      />
    );
  }
  if (!equipment?.length) {
    return <EmptyState icon={<PackageOpen />} title={messages.equipment.empty} />;
  }

  return (
    <ul className={styles.grid}>
      {equipment.map((item) => (
        <li key={item.id}>
          <EquipmentCard equipment={item} selected={item.id === selectedId} onSelect={onSelect} />
        </li>
      ))}
    </ul>
  );
}
