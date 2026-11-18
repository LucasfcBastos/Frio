import { useId } from 'react';

import type { Tone } from '@/utils/status';

import styles from './Sparkline.module.css';
import { buildSparklinePath, SPARKLINE_SIZE } from './sparklinePath';

const { width: WIDTH, height: HEIGHT, padding: PADDING } = SPARKLINE_SIZE;

export interface SparklineProps {
  values: number[];
  label: string;
  tone?: Tone;
}

export function Sparkline({ values, label, tone = 'info' }: SparklineProps) {
  const gradientId = useId();
  const path = buildSparklinePath(values);
  if (!path) return <div className={styles.placeholder} aria-hidden="true" />;

  const area = `${path} L${WIDTH - PADDING},${HEIGHT} L${PADDING},${HEIGHT} Z`;
  return (
    <svg
      className={[styles.sparkline, styles[tone]].join(' ')}
      viewBox={`0 0 ${WIDTH} ${HEIGHT}`}
      preserveAspectRatio="none"
      role="img"
      aria-label={label}
    >
      <defs>
        <linearGradient id={gradientId} x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stopColor="currentColor" stopOpacity="0.28" />
          <stop offset="100%" stopColor="currentColor" stopOpacity="0" />
        </linearGradient>
      </defs>
      <path d={area} fill={`url(#${gradientId})`} />
      <path
        d={path}
        fill="none"
        stroke="currentColor"
        strokeWidth="1.6"
        vectorEffect="non-scaling-stroke"
      />
    </svg>
  );
}
