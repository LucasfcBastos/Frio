import { useCallback, useState, type ReactElement, type ReactNode } from 'react';

import { Header, type HeaderProps } from '../Header';
import { Sidebar } from '../Sidebar';
import styles from './AppLayout.module.css';

export interface AppLayoutProps {
  header?: Omit<HeaderProps, 'onOpenMenu'>;
  children: ReactNode;
}

export function AppLayout({ header, children }: AppLayoutProps): ReactElement {
  const [menuOpen, setMenuOpen] = useState(false);
  const closeMenu = useCallback(() => setMenuOpen(false), []);

  return (
    <div className={styles.layout}>
      <Sidebar open={menuOpen} onClose={closeMenu} />
      {menuOpen && <div className={styles.scrim} onClick={closeMenu} aria-hidden="true" />}
      <div className={styles.main}>
        <Header {...header} onOpenMenu={() => setMenuOpen(true)} />
        <main className={styles.content} id="main-content">
          {children}
        </main>
      </div>
    </div>
  );
}
