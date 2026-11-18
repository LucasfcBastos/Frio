/** Pure geometry for the sparkline (kept apart from the component for testing). */
export const SPARKLINE_SIZE = { width: 120, height: 36, padding: 3 } as const;
const { width: WIDTH, height: HEIGHT, padding: PADDING } = SPARKLINE_SIZE;

export function buildSparklinePath(values: number[]): string {
  if (values.length < 2) return '';
  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min || 1;
  const step = (WIDTH - PADDING * 2) / (values.length - 1);
  return values
    .map((value, index) => {
      const x = PADDING + index * step;
      const y = HEIGHT - PADDING - ((value - min) / range) * (HEIGHT - PADDING * 2);
      return `${index === 0 ? 'M' : 'L'}${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(' ');
}
