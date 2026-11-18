import { LineChart as LineChartIcon } from 'lucide-react';
import { useMemo } from 'react';
import {
  CartesianGrid,
  Line,
  LineChart,
  ReferenceArea,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  type TooltipProps,
} from 'recharts';

import { EmptyState, ErrorState, Skeleton } from '@/components/ui';
import { useI18n } from '@/contexts/LocaleContext';
import { useChartTheme } from '@/hooks/useChartTheme';
import type { ReadingSeries } from '@/types/api';
import { formatClock, formatTemperature } from '@/utils/formatters';

import styles from './TemperatureChart.module.css';

export interface TemperatureChartProps {
  series: ReadingSeries | undefined;
  isLoading: boolean;
  isError: boolean;
  onRetry: () => void;
  hasSelection: boolean;
}

interface ChartRow {
  t: number;
  controller: number | null;
  sensor: number | null;
  setpoint: number | null;
}

const Y_PADDING_C = 2;

export function TemperatureChart({
  series,
  isLoading,
  isError,
  onRetry,
  hasSelection,
}: TemperatureChartProps) {
  const { messages, format, locale } = useI18n();
  const theme = useChartTheme();
  const t = messages.chart;

  const rows = useMemo<ChartRow[]>(
    () =>
      series?.points.map((point) => ({
        t: new Date(point.recorded_at).getTime(),
        controller: point.controller_c,
        sensor: point.sensor_c,
        setpoint: point.setpoint_c,
      })) ?? [],
    [series],
  );

  const incidentStart = useMemo(() => {
    const starts = series?.incidents.map((m) => new Date(m.started_at).getTime()) ?? [];
    return starts.length ? Math.min(...starts) : null;
  }, [series]);

  const yDomain = useMemo<[number, number]>(() => {
    if (!series) return [0, 1];
    const values = rows
      .flatMap((r) => [r.controller, r.sensor])
      .filter((v): v is number => v !== null);
    const min = Math.min(series.equipment.safe_min_c, ...values);
    const max = Math.max(series.equipment.safe_max_c, ...values);
    return [Math.floor(min - Y_PADDING_C), Math.ceil(max + Y_PADDING_C)];
  }, [rows, series]);

  if (!hasSelection) return <EmptyState icon={<LineChartIcon />} title={t.noSelection} />;
  if (isLoading && !series) return <Skeleton height="var(--chart-height)" radius="md" />;
  if (isError && !series) {
    return (
      <ErrorState
        message={messages.states.error}
        retryLabel={messages.states.retry}
        onRetry={onRetry}
      />
    );
  }
  if (!series || rows.length === 0) return <EmptyState icon={<LineChartIcon />} title={t.empty} />;

  const { equipment } = series;
  const xDomain: [number, number] = [rows[0]!.t, rows[rows.length - 1]!.t];

  return (
    <figure className={styles.figure}>
      <ul className={styles.legend}>
        <li className={styles.controller}>{t.controller}</li>
        <li className={styles.sensor}>{t.sensor}</li>
        <li className={styles.setpoint}>{t.setpoint}</li>
        <li className={styles.safe}>
          {t.safeRange} ({formatTemperature(equipment.safe_min_c, locale)} /{' '}
          {formatTemperature(equipment.safe_max_c, locale)})
        </li>
        {incidentStart !== null && <li className={styles.incident}>{t.incidentStart}</li>}
      </ul>
      <div
        className={styles.chart}
        role="img"
        aria-label={format(t.ariaLabel, { name: equipment.name })}
      >
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={rows} margin={{ top: 16, right: 16, bottom: 0, left: -8 }}>
            <CartesianGrid stroke={theme.grid} strokeDasharray="3 3" vertical={false} />
            <ReferenceArea
              y1={equipment.safe_min_c}
              y2={equipment.safe_max_c}
              fill={theme.safeBand}
              fillOpacity={0.08}
              stroke={theme.safeBand}
              strokeOpacity={0.25}
              ifOverflow="extendDomain"
            />
            <XAxis
              dataKey="t"
              type="number"
              scale="time"
              domain={xDomain}
              tickFormatter={(value: number) => formatClock(value, locale)}
              stroke={theme.axis}
              tick={{ fill: theme.axis, fontSize: 12 }}
              tickLine={false}
              minTickGap={32}
            />
            <YAxis
              domain={yDomain}
              stroke={theme.axis}
              tick={{ fill: theme.axis, fontSize: 12 }}
              tickLine={false}
              axisLine={false}
              tickFormatter={(value: number) => `${value}°`}
              width={48}
            />
            <Tooltip
              content={<ChartTooltip labels={t} locale={locale} />}
              cursor={{ stroke: theme.border }}
            />
            {incidentStart !== null && (
              <ReferenceLine
                x={incidentStart}
                stroke={theme.incident}
                strokeWidth={2}
                strokeDasharray="4 3"
                label={{
                  value: `⚠ ${formatClock(incidentStart, locale)}`,
                  position: 'insideTopRight',
                  fill: theme.incident,
                  fontSize: 12,
                  fontWeight: 600,
                }}
              />
            )}
            <Line
              type="stepAfter"
              dataKey="setpoint"
              stroke={theme.setpoint}
              strokeDasharray="6 4"
              strokeWidth={1.25}
              dot={false}
              isAnimationActive={false}
              connectNulls
            />
            <Line
              type="monotone"
              dataKey="controller"
              stroke={theme.controller}
              strokeWidth={2}
              dot={false}
              isAnimationActive={false}
              connectNulls
            />
            <Line
              type="monotone"
              dataKey="sensor"
              stroke={theme.sensor}
              strokeWidth={2.25}
              dot={false}
              isAnimationActive={false}
              connectNulls
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </figure>
  );
}

interface ChartTooltipProps extends TooltipProps<number, string> {
  labels: { controller: string; sensor: string; setpoint: string };
  locale: 'pt-BR' | 'en';
}

function ChartTooltip({ active, payload, label, labels, locale }: ChartTooltipProps) {
  if (!active || !payload?.length) return null;
  const row = payload[0]?.payload as ChartRow | undefined;
  if (!row) return null;
  return (
    <div className={styles.tooltip}>
      <p className={styles.tooltipTime}>{formatClock(Number(label), locale, true)}</p>
      <p className={styles.controller}>
        {labels.controller}:{' '}
        <strong className="tabular">{formatTemperature(row.controller, locale)}</strong>
      </p>
      <p className={styles.sensor}>
        {labels.sensor}:{' '}
        <strong className="tabular">{formatTemperature(row.sensor, locale)}</strong>
      </p>
      <p className={styles.setpoint}>
        {labels.setpoint}:{' '}
        <strong className="tabular">{formatTemperature(row.setpoint, locale)}</strong>
      </p>
    </div>
  );
}
