import { screen } from '@testing-library/react';

import { renderWithProviders } from '@/test/renderWithProviders';

import { StatusBadge } from './StatusBadge';

describe('StatusBadge', () => {
  it.each([
    ['normal', 'Normal', 'success'],
    ['warning', 'Atenção', 'warning'],
    ['critical', 'Crítico', 'critical'],
  ] as const)('renders %s with text and tone (not color alone)', (status, label, tone) => {
    renderWithProviders(<StatusBadge status={status} />);

    const badge = screen.getByText(label);
    expect(badge).toHaveAttribute('data-tone', tone);
    expect(badge.querySelector('svg')).toBeInTheDocument();
  });

  it('follows the selected language', () => {
    renderWithProviders(<StatusBadge status="warning" />, { locale: 'en' });
    expect(screen.getByText('Warning')).toBeInTheDocument();
  });
});
