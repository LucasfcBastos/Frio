import { render, type RenderOptions } from '@testing-library/react';
import type { ReactElement } from 'react';

import { LocaleProvider } from '@/contexts/LocaleContext';
import type { Locale } from '@/locales';

export function renderWithProviders(
  ui: ReactElement,
  { locale = 'pt-BR', ...options }: { locale?: Locale } & RenderOptions = {},
) {
  return render(<LocaleProvider initialLocale={locale}>{ui}</LocaleProvider>, options);
}
