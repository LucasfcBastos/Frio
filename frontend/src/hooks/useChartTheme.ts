import { useMemo } from 'react';

const TOKENS = {
  controller: '--chart-controller',
  sensor: '--chart-sensor',
  setpoint: '--chart-setpoint',
  safeBand: '--chart-safe-band',
  incident: '--chart-incident',
  grid: '--chart-grid',
  axis: '--chart-axis',
  surface: '--color-surface-raised',
  border: '--color-border',
} as const;

export type ChartTheme = Record<keyof typeof TOKENS, string>;

/**
 * Recharts needs concrete color strings in SVG attributes, so we resolve the
 * CSS custom properties from tokens.css once instead of duplicating hex values.
 */
export function useChartTheme(): ChartTheme {
  return useMemo(() => {
    const styles = getComputedStyle(document.documentElement);
    return Object.fromEntries(
      Object.entries(TOKENS).map(([key, variable]) => [
        key,
        styles.getPropertyValue(variable).trim() || 'currentColor',
      ]),
    ) as ChartTheme;
  }, []);
}
