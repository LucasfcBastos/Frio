import {
  Bug,
  LayoutDashboard,
  Server,
  Settings,
  ShieldAlert,
  X,
  type LucideIcon,
} from 'lucide-react';
import { NavLink } from 'react-router-dom';

import logo from '@/assets/logo.svg';
import { Badge } from '@/components/ui';
import { useI18n } from '@/contexts/LocaleContext';
import type { Messages } from '@/locales';

import styles from './Sidebar.module.css';

interface NavItem {
  key: keyof Pick<
    Messages['nav'],
    'dashboard' | 'equipment' | 'incidents' | 'vulnerabilities' | 'settings'
  >;
  icon: LucideIcon;
  to?: string;
}

const NAV_ITEMS: NavItem[] = [
  { key: 'dashboard', icon: LayoutDashboard, to: '/' },
  { key: 'equipment', icon: Server },
  { key: 'incidents', icon: ShieldAlert },
  { key: 'vulnerabilities', icon: Bug },
  { key: 'settings', icon: Settings },
];

export interface SidebarProps {
  open: boolean;
  onClose: () => void;
}

export function Sidebar({ open, onClose }: SidebarProps) {
  const { messages } = useI18n();
  return (
    <aside className={[styles.sidebar, open && styles.open].filter(Boolean).join(' ')}>
      <div className={styles.brand}>
        <img src={logo} alt="" className={styles.logo} />
        <div>
          <p className={styles.name}>{messages.app.name}</p>
          <p className={styles.tagline}>{messages.app.tagline}</p>
        </div>
        <button className={styles.close} onClick={onClose} aria-label={messages.nav.closeMenu}>
          <X aria-hidden="true" />
        </button>
      </div>

      <nav aria-label={messages.nav.label}>
        <ul className={styles.list}>
          {NAV_ITEMS.map(({ key, icon: Icon, to }) => (
            <li key={key}>
              {to ? (
                <NavLink
                  to={to}
                  end
                  onClick={onClose}
                  className={({ isActive }) =>
                    [styles.item, isActive && styles.active].filter(Boolean).join(' ')
                  }
                >
                  <Icon className={styles.icon} aria-hidden="true" />
                  {messages.nav[key]}
                </NavLink>
              ) : (
                <span className={[styles.item, styles.disabled].join(' ')} aria-disabled="true">
                  <Icon className={styles.icon} aria-hidden="true" />
                  {messages.nav[key]}
                  <Badge size="sm" className={styles.soon}>
                    {messages.nav.comingSoon}
                  </Badge>
                </span>
              )}
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
}
