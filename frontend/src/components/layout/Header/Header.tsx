import { Menu } from 'lucide-react';

import { useI18n } from '@/contexts/LocaleContext';
import { useStoreContext } from '@/contexts/StoreContext';
import type { EquipmentStatus } from '@/types/api';

import { LanguageToggle } from '../LanguageToggle';
import { LiveIndicator } from '../LiveIndicator';
import { OverallStatus } from '../OverallStatus';
import { StoreSelector } from '../StoreSelector';
import { UserMenu } from '../UserMenu';
import styles from './Header.module.css';

export interface HeaderProps {
  overallStatus?: EquipmentStatus;
  lastUpdatedAt?: string | null;
  onOpenMenu: () => void;
}

export function Header({ overallStatus, lastUpdatedAt, onOpenMenu }: HeaderProps) {
  const { messages } = useI18n();
  const { stores, selectedStoreId, selectStore, isLoading } = useStoreContext();

  return (
    <header className={styles.header}>
      <div className={styles.left}>
        <button className={styles.menu} onClick={onOpenMenu} aria-label={messages.nav.openMenu}>
          <Menu aria-hidden="true" />
        </button>
        <StoreSelector
          stores={stores}
          selectedId={selectedStoreId}
          onChange={selectStore}
          isLoading={isLoading}
        />
        {overallStatus && <OverallStatus status={overallStatus} />}
      </div>
      <div className={styles.right}>
        <LiveIndicator lastUpdatedAt={lastUpdatedAt} />
        <LanguageToggle />
        <UserMenu />
      </div>
    </header>
  );
}
