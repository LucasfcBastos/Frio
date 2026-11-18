import { useId, type ReactNode } from 'react';

import styles from './Tooltip.module.css';

export interface TooltipProps {
  label: string;
  children: ReactNode;
  placement?: 'top' | 'bottom' | 'right';
}

/** CSS-only tooltip, shown on hover and keyboard focus. */
export function Tooltip({ label, children, placement = 'top' }: TooltipProps) {
  const id = useId();
  return (
    <span className={styles.wrapper} aria-describedby={id}>
      {children}
      <span role="tooltip" id={id} className={[styles.tooltip, styles[placement]].join(' ')}>
        {label}
      </span>
    </span>
  );
}
