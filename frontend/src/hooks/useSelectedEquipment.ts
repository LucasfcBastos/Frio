import { useMemo, useState } from 'react';

import type { EquipmentOverview } from '@/types/api';

const STATUS_PRIORITY = { critical: 0, warning: 1, normal: 2 } as const;

/**
 * Equipment shown in the main chart: the user's choice if still present,
 * otherwise the most critical one.
 */
export function useSelectedEquipment(equipment: EquipmentOverview[] | undefined) {
  const [chosenId, setChosenId] = useState<number | null>(null);

  const selectedId = useMemo(() => {
    if (!equipment?.length) return null;
    if (chosenId !== null && equipment.some((item) => item.id === chosenId)) return chosenId;
    const [mostCritical] = [...equipment].sort(
      (a, b) => STATUS_PRIORITY[a.status] - STATUS_PRIORITY[b.status],
    );
    return mostCritical?.id ?? null;
  }, [equipment, chosenId]);

  return { selectedId, select: setChosenId };
}
