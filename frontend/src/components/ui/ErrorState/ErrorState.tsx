import { AlertOctagon, RotateCw } from 'lucide-react';

import { Button } from '../Button';
import styles from './ErrorState.module.css';

export interface ErrorStateProps {
  message: string;
  retryLabel?: string;
  onRetry?: () => void;
}

export function ErrorState({ message, retryLabel, onRetry }: ErrorStateProps) {
  return (
    <div className={styles.error} role="alert">
      <AlertOctagon className={styles.icon} aria-hidden="true" />
      <p>{message}</p>
      {onRetry && retryLabel && (
        <Button size="sm" icon={<RotateCw />} onClick={onRetry}>
          {retryLabel}
        </Button>
      )}
    </div>
  );
}
