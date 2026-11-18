import { AlertTriangle, Cpu, Snowflake, ThermometerSnowflake, Wind } from 'lucide-react';

import { useI18n } from '@/contexts/LocaleContext';
import type { EquipmentOverview } from '@/types/api';
import { formatTemperature } from '@/utils/formatters';
import { STATUS_TONE } from '@/utils/status';

import { Sparkline } from '../Sparkline';
import { StatusBadge } from '../StatusBadge';
import styles from './EquipmentCard.module.css';

const TYPE_ICONS = { freezer: Snowflake, cold_room: ThermometerSnowflake, chiller: Wind } as const;

export interface EquipmentCardProps {
  equipment: EquipmentOverview;
  selected?: boolean;
  onSelect?: (equipmentId: number) => void;
}

export function EquipmentCard({ equipment, selected = false, onSelect }: EquipmentCardProps) {
  const { messages, format, locale } = useI18n();
  const t = messages.equipment;
  const TypeIcon = TYPE_ICONS[equipment.type];
  const diverging = equipment.is_diverging;

  return (
    <button
      type="button"
      className={[styles.card, styles[equipment.status], selected && styles.selected]
        .filter(Boolean)
        .join(' ')}
      aria-pressed={selected}
      onClick={() => onSelect?.(equipment.id)}
    >
      <div className={styles.head}>
        <span className={styles.typeIcon} aria-hidden="true">
          <TypeIcon />
        </span>
        <span className={styles.identity}>
          <span className={styles.name}>{equipment.name}</span>
          <span className={styles.type}>{t.type[equipment.type]}</span>
        </span>
        <StatusBadge status={equipment.status} size="sm" />
      </div>

      <div className={[styles.readings, diverging && styles.diverging].filter(Boolean).join(' ')}>
        <div className={styles.reading} data-testid="controller-reading">
          <span className={styles.readingLabel}>{t.controller}</span>
          <span className={[styles.temperature, 'tabular'].join(' ')}>
            {formatTemperature(equipment.controller_temperature_c, locale)}
          </span>
        </div>
        <div className={styles.reading} data-testid="sensor-reading">
          <span className={styles.readingLabel}>{t.sensor}</span>
          <span className={[styles.temperature, styles.sensorValue, 'tabular'].join(' ')}>
            {formatTemperature(equipment.sensor_temperature_c, locale)}
          </span>
        </div>
      </div>

      {diverging && (
        <p className={styles.alert} role="note">
          <AlertTriangle aria-hidden="true" />
          {format(t.diverging, { value: formatTemperature(equipment.divergence_c, locale) })}
        </p>
      )}

      <dl className={styles.meta}>
        <div>
          <dt>{t.setpoint}</dt>
          <dd className="tabular">{formatTemperature(equipment.setpoint_c, locale)}</dd>
        </div>
        <div>
          <dt>{t.modeLabel}</dt>
          <dd className={equipment.mode === 'defrost' ? styles.defrost : undefined}>
            {equipment.mode ? t.mode[equipment.mode] : '—'}
          </dd>
        </div>
      </dl>

      <Sparkline
        values={equipment.sparkline.map((point) => point.temperature_c)}
        label={t.sparklineLabel}
        tone={STATUS_TONE[equipment.status] === 'success' ? 'info' : STATUS_TONE[equipment.status]}
      />

      {equipment.firmware_outdated && (
        <p className={styles.firmware}>
          <Cpu aria-hidden="true" />
          {format(t.firmwareOutdated, { version: equipment.firmware_version })}
        </p>
      )}
    </button>
  );
}
