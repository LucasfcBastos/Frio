import { useI18n } from '@/contexts/LocaleContext';

import styles from './UserMenu.module.css';

function initials(name: string): string {
  return name
    .split(' ')
    .map((part) => part[0])
    .slice(0, 2)
    .join('')
    .toUpperCase();
}

/** Mock user: authentication is out of scope for this MVP stage. */
export function UserMenu() {
  const { messages } = useI18n();
  const { name, role } = messages.header.user;
  return (
    <div className={styles.user}>
      <span className={styles.avatar} aria-hidden="true">
        {initials(name)}
      </span>
      <span className={styles.text}>
        <span className={styles.name}>{name}</span>
        <span className={styles.role}>{role}</span>
      </span>
    </div>
  );
}
