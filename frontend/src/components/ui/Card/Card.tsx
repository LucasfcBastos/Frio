import type { HTMLAttributes, ReactNode } from 'react';

import styles from './Card.module.css';

export interface CardProps extends Omit<HTMLAttributes<HTMLElement>, 'title'> {
  as?: 'section' | 'article' | 'div';
  title?: ReactNode;
  actions?: ReactNode;
  padded?: boolean;
}

export function Card({
  as: Tag = 'section',
  title,
  actions,
  padded = true,
  className,
  children,
  ...rest
}: CardProps) {
  return (
    <Tag
      className={[styles.card, padded && styles.padded, className].filter(Boolean).join(' ')}
      {...rest}
    >
      {(title || actions) && (
        <header className={styles.header}>
          {title && <h2 className={styles.title}>{title}</h2>}
          {actions && <div className={styles.actions}>{actions}</div>}
        </header>
      )}
      {children}
    </Tag>
  );
}
