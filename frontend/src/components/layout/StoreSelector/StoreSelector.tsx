import { ChevronDown, Store as StoreIcon } from 'lucide-react';
import { useId } from 'react';

import { Skeleton } from '@/components/ui';
import { useI18n } from '@/contexts/LocaleContext';
import type { Store } from '@/types/api';

import styles from './StoreSelector.module.css';

export interface StoreSelectorProps {
  stores: Store[];
  selectedId: number | null;
  onChange: (storeId: number) => void;
  isLoading?: boolean;
}

export function StoreSelector({ stores, selectedId, onChange, isLoading }: StoreSelectorProps) {
  const { messages } = useI18n();
  const id = useId();
  if (isLoading) return <Skeleton width="12rem" height="2.25rem" radius="md" />;

  return (
    <div className={styles.wrapper}>
      <label htmlFor={id} className="visually-hidden">
        {messages.header.store}
      </label>
      <StoreIcon className={styles.leading} aria-hidden="true" />
      <select
        id={id}
        className={styles.select}
        value={selectedId ?? ''}
        onChange={(event) => onChange(Number(event.target.value))}
      >
        {stores.map((store) => (
          <option key={store.id} value={store.id}>
            {store.name} · {store.city}/{store.state}
          </option>
        ))}
      </select>
      <ChevronDown className={styles.trailing} aria-hidden="true" />
    </div>
  );
}
