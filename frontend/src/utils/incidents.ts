import { interpolate, type Messages } from '@/locales';
import type { Incident, RuleCode } from '@/types/api';

/**
 * The API stores English text for auditability; the UI renders the localized
 * version from `rule_code` + `metadata`, falling back to the API text.
 */
export function localizeRuleTitle(ruleCode: string, fallback: string, messages: Messages): string {
  return messages.rules[ruleCode as RuleCode]?.title ?? fallback;
}

export function localizeIncident(incident: Incident, messages: Messages) {
  const rule = messages.rules[incident.rule_code];
  if (!rule) return { title: incident.title, description: incident.description };
  return {
    title: rule.title,
    description: interpolate(rule.description, {
      equipment: incident.equipment_name,
      ...incident.metadata,
    }),
  };
}
