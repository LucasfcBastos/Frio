/** Types mirroring the backend serializers (`apps/<app>/serializers.py`). */

export type EquipmentType = 'freezer' | 'cold_room' | 'chiller';
export type EquipmentStatus = 'normal' | 'warning' | 'critical';
export type OperatingMode = 'cooling' | 'defrost' | 'idle';
export type Severity = 'low' | 'medium' | 'high' | 'critical';
export type IncidentStatus = 'active' | 'acknowledged' | 'resolved';
export type RuleCode =
  | 'UNSCHEDULED_DEFROST'
  | 'SENSOR_DIVERGENCE'
  | 'OUT_OF_SAFE_RANGE'
  | 'SETPOINT_TAMPERING';

/** ISO-8601 timestamp as returned by the API. */
export type IsoDateTime = string;

export interface Paginated<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface Store {
  id: number;
  name: string;
  city: string;
  state: string;
  organization_id: number;
  organization_name: string;
}

export interface DashboardSummary {
  total_equipment: number;
  normal_equipment: number;
  warning_equipment: number;
  critical_equipment: number;
  active_incidents: number;
  mean_detection_seconds: number | null;
  outdated_firmware: number;
  overall_status: EquipmentStatus;
  last_updated_at: IsoDateTime | null;
}

export interface SparkPoint {
  recorded_at: IsoDateTime;
  temperature_c: number;
}

export interface EquipmentOverview {
  id: number;
  store_id: number;
  name: string;
  type: EquipmentType;
  status: EquipmentStatus;
  manufacturer: string;
  model: string;
  firmware_version: string;
  firmware_outdated: boolean;
  setpoint_c: number;
  safe_min_c: number;
  safe_max_c: number;
  mode: OperatingMode | null;
  controller_temperature_c: number | null;
  sensor_temperature_c: number | null;
  divergence_c: number | null;
  is_diverging: boolean;
  last_reading_at: IsoDateTime | null;
  sparkline: SparkPoint[];
}

export interface SeriesPoint {
  recorded_at: IsoDateTime;
  controller_c: number | null;
  sensor_c: number | null;
  setpoint_c: number | null;
  mode: OperatingMode | null;
}

export interface IncidentMarker {
  id: number;
  rule_code: RuleCode;
  severity: Severity;
  title: string;
  started_at: IsoDateTime;
}

export interface ReadingSeries {
  equipment: {
    id: number;
    name: string;
    type: EquipmentType;
    setpoint_c: number;
    safe_min_c: number;
    safe_max_c: number;
  };
  hours: number;
  points: SeriesPoint[];
  incidents: IncidentMarker[];
}

export interface Incident {
  id: number;
  equipment_id: number;
  equipment_name: string;
  store_id: number;
  severity: Severity;
  rule_code: RuleCode;
  title: string;
  description: string;
  status: IncidentStatus;
  started_at: IsoDateTime;
  detected_at: IsoDateTime;
  detection_seconds: number;
  metadata: Record<string, string | number>;
}

export type TimelineKind = 'config_change' | 'condition_started' | 'incident_detected';

export interface TimelineEvent {
  at: IsoDateTime;
  kind: TimelineKind;
  label: string;
  data: Record<string, string | number>;
}

export interface IncidentDetail {
  incident: Incident;
  timeline: TimelineEvent[];
}

export interface ApiErrorBody {
  error: { code: string; message: string; details: unknown };
}
