import type { ReactNode } from 'react';

import type { Tone } from '@/utils/status';

import styles from './Badge.module.css';

export interface BadgeProps {
  tone?: Tone;
  icon?: ReactNode;
  size?: 'sm' | 'md';
  children: ReactNode;
  className?: string;
}

export function Badge({ tone = 'neutral', icon, size = 'md', children, className }: BadgeProps) {
  return (
    <span
      className={[styles.badge, styles[tone], styles[size], className].filter(Boolean).join(' ')}
      data-tone={tone}
    >
      {icon && (
        <span className={styles.icon} aria-hidden="true">
          {icon}
        </span>
      )}
      {children}
    </span>
  );
}
