import { useI18n } from '@/contexts/LocaleContext';
import { LOCALE_LABELS, type Locale } from '@/locales';

import styles from './LanguageToggle.module.css';

export function LanguageToggle() {
  const { locale, setLocale, messages } = useI18n();
  return (
    <div className={styles.toggle} role="group" aria-label={messages.header.language}>
      {(Object.keys(LOCALE_LABELS) as Locale[]).map((option) => (
        <button
          key={option}
          className={[styles.option, option === locale && styles.active].filter(Boolean).join(' ')}
          aria-pressed={option === locale}
          onClick={() => setLocale(option)}
          lang={option}
        >
          {LOCALE_LABELS[option]}
        </button>
      ))}
    </div>
  );
}
