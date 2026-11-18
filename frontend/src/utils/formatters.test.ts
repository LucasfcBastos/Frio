import { formatDuration, formatRelativeTime, formatTemperature } from './formatters';

describe('formatters', () => {
  it('formats temperatures per locale with explicit sign', () => {
    expect(formatTemperature(-18.04, 'pt-BR')).toBe('-18,0°C');
    expect(formatTemperature(5.2, 'en')).toBe('+5.2°C');
    expect(formatTemperature(null, 'en')).toBe('—');
  });

  it('formats compact durations', () => {
    expect(formatDuration(18.4)).toBe('18s');
    expect(formatDuration(240)).toBe('4min');
    expect(formatDuration(3.5 * 3600)).toBe('3h30');
  });

  it('formats relative time', () => {
    const now = new Date('2026-11-18T05:00:30Z');
    expect(formatRelativeTime('2026-11-18T05:00:00Z', now, 'en')).toBe('30 seconds ago');
  });
});
