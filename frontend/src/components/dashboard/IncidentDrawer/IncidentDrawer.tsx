import { Settings2, ShieldAlert, Timer } from 'lucide-react';

import { Badge, Drawer, ErrorState, Skeleton } from '@/components/ui';
import { useI18n } from '@/contexts/LocaleContext';
import type { Messages } from '@/locales';
import type { IncidentDetail, TimelineEvent } from '@/types/api';
import { formatClock, formatDuration } from '@/utils/formatters';
import { localizeIncident, localizeRuleTitle } from '@/utils/incidents';
import { SEVERITY_TONE } from '@/utils/status';

import styles from './IncidentDrawer.module.css';

export interface IncidentDrawerProps {
  open: boolean;
  onClose: () => void;
  detail: IncidentDetail | undefined;
  isLoading: boolean;
  isError: boolean;
  onRetry: () => void;
}

const TIMELINE_ICONS = {
  config_change: Settings2,
  condition_started: ShieldAlert,
  incident_detected: Timer,
} as const;

function describeEvent(
  event: TimelineEvent,
  messages: Messages,
  format: (t: string, v: Record<string, string | number>) => string,
) {
  const d = messages.drawer;
  const data = event.data;
  switch (event.kind) {
    case 'config_change': {
      const field = String(data.field);
      return {
        text: format(d.configChange, {
          field: d.fields[field as keyof typeof d.fields] ?? field,
          old: data.old_value ?? '',
          new: data.new_value ?? '',
        }),
        detail: format(d.fromIp, { ip: data.origin_ip ?? '' }),
      };
    }
    case 'condition_started':
      return { text: localizeRuleTitle(String(data.rule_code), event.label, messages) };
    case 'incident_detected':
      return {
        text: format(d.detectedAfter, {
          title: localizeRuleTitle(String(data.rule_code), event.label, messages),
          time: formatDuration(Number(data.detection_seconds)),
        }),
      };
  }
}

export function IncidentDrawer({
  open,
  onClose,
  detail,
  isLoading,
  isError,
  onRetry,
}: IncidentDrawerProps) {
  const { messages, format, locale } = useI18n();
  const d = messages.drawer;
  const incident = detail?.incident;
  const localized = incident ? localizeIncident(incident, messages) : null;

  return (
    <Drawer
      open={open}
      onClose={onClose}
      closeLabel={d.close}
      title={localized?.title ?? <Skeleton width="16rem" height="var(--text-lg)" />}
    >
      {isError && !detail && (
        <ErrorState
          message={messages.states.error}
          retryLabel={messages.states.retry}
          onRetry={onRetry}
        />
      )}
      {isLoading && !detail && (
        <div className={styles.stack}>
          <Skeleton height="4rem" radius="md" />
          <Skeleton height="12rem" radius="md" />
        </div>
      )}
      {incident && localized && detail && (
        <div className={styles.stack}>
          <div className={styles.badges}>
            <Badge tone={SEVERITY_TONE[incident.severity]} icon={<ShieldAlert />}>
              {messages.severity[incident.severity]}
            </Badge>
            <Badge>{incident.equipment_name}</Badge>
            <code className={styles.rule}>{incident.rule_code}</code>
          </div>

          <section>
            <h3 className={styles.heading}>{d.description}</h3>
            <p className={styles.description}>{localized.description}</p>
          </section>

          <dl className={styles.facts}>
            <div>
              <dt>{d.startedAt}</dt>
              <dd className="tabular">{formatClock(incident.started_at, locale, true)}</dd>
            </div>
            <div>
              <dt>{d.detectedAt}</dt>
              <dd className="tabular">{formatClock(incident.detected_at, locale, true)}</dd>
            </div>
            <div>
              <dt>{d.detectionTime}</dt>
              <dd className={[styles.highlight, 'tabular'].join(' ')}>
                {formatDuration(incident.detection_seconds)}
              </dd>
            </div>
            {incident.metadata.origin_ip && (
              <div>
                <dt>{d.origin}</dt>
                <dd className={styles.mono}>{incident.metadata.origin_ip}</dd>
              </div>
            )}
          </dl>

          <section>
            <h3 className={styles.heading}>{d.timeline}</h3>
            <ol className={styles.timeline}>
              {detail.timeline.map((event, index) => {
                const Icon = TIMELINE_ICONS[event.kind];
                const { text, detail: extra } = describeEvent(event, messages, format);
                return (
                  <li
                    key={`${event.at}-${index}`}
                    className={[styles.event, styles[event.kind]].join(' ')}
                  >
                    <span className={styles.marker} aria-hidden="true">
                      <Icon />
                    </span>
                    <div>
                      <p className={styles.eventMeta}>
                        <time className="tabular" dateTime={event.at}>
                          {formatClock(event.at, locale, true)}
                        </time>{' '}
                        · {d.timelineKinds[event.kind]}
                      </p>
                      <p className={styles.eventText}>{text}</p>
                      {extra && <p className={styles.eventExtra}>{extra}</p>}
                    </div>
                  </li>
                );
              })}
            </ol>
          </section>
        </div>
      )}
    </Drawer>
  );
}
