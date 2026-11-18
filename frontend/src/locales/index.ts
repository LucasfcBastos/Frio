import { en } from './en';
import { ptBR, type Messages } from './pt-BR';

export type Locale = 'pt-BR' | 'en';
export type { Messages };

export const DEFAULT_LOCALE: Locale = 'pt-BR';
export const LOCALES: Record<Locale, Messages> = { 'pt-BR': ptBR, en };
export const LOCALE_LABELS: Record<Locale, string> = { 'pt-BR': 'PT', en: 'EN' };

/** Replace `{name}` placeholders. Unknown placeholders are left untouched. */
export function interpolate(
  template: string,
  values: Record<string, string | number | null | undefined>,
): string {
  return template.replace(/\{(\w+)\}/g, (match, key: string) => {
    const value = values[key];
    return value === undefined || value === null ? match : String(value);
  });
}
