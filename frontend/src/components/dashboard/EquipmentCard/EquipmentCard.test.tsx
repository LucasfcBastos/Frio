import { screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

import { renderWithProviders } from '@/test/renderWithProviders';
import type { EquipmentOverview } from '@/types/api';

import { EquipmentCard } from './EquipmentCard';

const base: EquipmentOverview = {
  id: 2,
  store_id: 1,
  name: 'Câmara de Congelados 02',
  type: 'cold_room',
  status: 'normal',
  manufacturer: 'Polarix',
  model: 'PX-400',
  firmware_version: '3.2.0',
  firmware_outdated: false,
  setpoint_c: -18,
  safe_min_c: -25,
  safe_max_c: -15,
  mode: 'cooling',
  controller_temperature_c: -18.1,
  sensor_temperature_c: -18.3,
  divergence_c: 0.2,
  is_diverging: false,
  last_reading_at: '2026-11-18T05:30:00Z',
  sparkline: [-18.2, -18.4, -18.1].map((temperature_c, i) => ({
    recorded_at: `2026-11-18T05:2${i}:00Z`,
    temperature_c,
  })),
};

const attacked: EquipmentOverview = {
  ...base,
  status: 'critical',
  mode: 'defrost',
  firmware_version: '2.9.1',
  firmware_outdated: true,
  controller_temperature_c: -18,
  sensor_temperature_c: 5.2,
  divergence_c: 23.2,
  is_diverging: true,
};

describe('EquipmentCard', () => {
  it('shows controller and independent sensor side by side', () => {
    renderWithProviders(<EquipmentCard equipment={base} />);

    expect(screen.getByText('Câmara de Congelados 02')).toBeInTheDocument();
    expect(screen.getByText('Câmara fria')).toBeInTheDocument();
    expect(
      within(screen.getByTestId('controller-reading')).getByText('-18,1°C'),
    ).toBeInTheDocument();
    expect(within(screen.getByTestId('sensor-reading')).getByText('-18,3°C')).toBeInTheDocument();
    expect(screen.getByText('Resfriando')).toBeInTheDocument();
    expect(screen.queryByRole('note')).not.toBeInTheDocument();
  });

  it('highlights divergence, defrost and outdated firmware during the attack', () => {
    renderWithProviders(<EquipmentCard equipment={attacked} />);

    expect(screen.getByText('Crítico')).toBeInTheDocument();
    expect(screen.getByRole('note')).toHaveTextContent('Divergência de +23,2°C');
    expect(screen.getByText('Degelo')).toBeInTheDocument();
    expect(screen.getByText('Firmware 2.9.1 desatualizado')).toBeInTheDocument();
    expect(screen.getByText('+5,2°C')).toBeInTheDocument();
  });

  it('reports selection and exposes it to assistive tech', async () => {
    const onSelect = vi.fn();
    renderWithProviders(<EquipmentCard equipment={base} selected onSelect={onSelect} />);

    const card = screen.getByRole('button', { pressed: true });
    await userEvent.click(card);

    expect(onSelect).toHaveBeenCalledWith(2);
  });

  it('renders a sparkline from the sensor history', () => {
    renderWithProviders(<EquipmentCard equipment={base} />);
    expect(
      screen.getByRole('img', { name: 'Tendência do sensor independente' }),
    ).toBeInTheDocument();
  });
});
