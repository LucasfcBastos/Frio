import styles from './Skeleton.module.css';

export interface SkeletonProps {
  /** Any CSS length, preferably a token: `var(--space-8)`. */
  width?: string;
  height?: string;
  radius?: 'sm' | 'md' | 'lg' | 'full';
  className?: string;
}

export function Skeleton({
  width = '100%',
  height = '1em',
  radius = 'sm',
  className,
}: SkeletonProps) {
  return (
    <span
      aria-hidden="true"
      className={[styles.skeleton, styles[radius], className].filter(Boolean).join(' ')}
      style={{ width, height }}
    />
  );
}
