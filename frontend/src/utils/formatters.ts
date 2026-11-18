import type { Locale } from '@/locales';

const intlLocale = (locale: Locale) => (locale === 'en' ? 'en-US' : 'pt-BR');

export function formatTemperature(value: number | null | undefined, locale: Locale): string {
  if (value === null || value === undefined || Number.isNaN(value)) return '—';
  const formatted = new Intl.NumberFormat(intlLocale(locale), {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
    signDisplay: 'exceptZero',
  }).format(value);
  return `${formatted}°C`;
}

/** Compact duration: 18s · 4min · 3h30 */
export function formatDuration(totalSeconds: number | null | undefined): string {
  if (totalSeconds === null || totalSeconds === undefined) return '—';
  const seconds = Math.max(0, Math.round(totalSeconds));
  if (seconds < 60) return `${seconds}s`;
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}min`;
  const hours = Math.floor(minutes / 60);
  const rest = minutes % 60;
  return rest ? `${hours}h${String(rest).padStart(2, '0')}` : `${hours}h`;
}

const RELATIVE_UNITS: [Intl.RelativeTimeFormatUnit, number][] = [
  ['day', 86_400],
  ['hour', 3_600],
  ['minute', 60],
  ['second', 1],
];

export function formatRelativeTime(
  date: string | Date | null | undefined,
  now: Date,
  locale: Locale,
): string {
  if (!date) return '—';
  const target = typeof date === 'string' ? new Date(date) : date;
  const diffSeconds = Math.round((target.getTime() - now.getTime()) / 1000);
  const formatter = new Intl.RelativeTimeFormat(intlLocale(locale), { numeric: 'auto' });
  if (Math.abs(diffSeconds) < 1) return formatter.format(0, 'second');
  for (const [unit, size] of RELATIVE_UNITS) {
    if (Math.abs(diffSeconds) >= size || unit === 'second') {
      return formatter.format(Math.round(diffSeconds / size), unit);
    }
  }
  return formatter.format(diffSeconds, 'second');
}

export function formatClock(date: string | Date | number, locale: Locale, withSeconds = false) {
  return new Intl.DateTimeFormat(intlLocale(locale), {
    hour: '2-digit',
    minute: '2-digit',
    ...(withSeconds ? { second: '2-digit' } : {}),
  }).format(typeof date === 'string' ? new Date(date) : date);
}

export function formatNumber(value: number | null | undefined, locale: Locale): string {
  if (value === null || value === undefined) return '—';
  return new Intl.NumberFormat(intlLocale(locale)).format(value);
}
