import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from 'react';

import { useStores } from '@/hooks/useStores';
import type { Store } from '@/types/api';
import { STORE_STORAGE_KEY } from '@/utils/constants';

interface StoreContextValue {
  stores: Store[];
  selectedStore: Store | null;
  selectedStoreId: number | null;
  selectStore: (storeId: number) => void;
  isLoading: boolean;
  isError: boolean;
  refetch: () => void;
}

const StoreContext = createContext<StoreContextValue | null>(null);

function readStoredStoreId(): number | null {
  try {
    const value = Number(window.localStorage.getItem(STORE_STORAGE_KEY));
    return Number.isInteger(value) && value > 0 ? value : null;
  } catch {
    return null;
  }
}

export function StoreProvider({ children }: { children: ReactNode }) {
  const { data: stores = [], isLoading, isError, refetch } = useStores();
  const [chosenId, setChosenId] = useState<number | null>(readStoredStoreId);

  const selectedStore = useMemo(
    () => stores.find((store) => store.id === chosenId) ?? stores[0] ?? null,
    [stores, chosenId],
  );

  const selectStore = useCallback((storeId: number) => {
    setChosenId(storeId);
    try {
      window.localStorage.setItem(STORE_STORAGE_KEY, String(storeId));
    } catch {
      /* ignore */
    }
  }, []);

  const value = useMemo(
    () => ({
      stores,
      selectedStore,
      selectedStoreId: selectedStore?.id ?? null,
      selectStore,
      isLoading,
      isError,
      refetch: () => void refetch(),
    }),
    [stores, selectedStore, selectStore, isLoading, isError, refetch],
  );
  return <StoreContext.Provider value={value}>{children}</StoreContext.Provider>;
}

export function useStoreContext(): StoreContextValue {
  const context = useContext(StoreContext);
  if (!context) throw new Error('useStoreContext must be used inside <StoreProvider>.');
  return context;
}
