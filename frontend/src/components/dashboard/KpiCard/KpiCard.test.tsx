import { render, screen } from '@testing-library/react';
import { Timer } from 'lucide-react';

import { KpiCard } from './KpiCard';

describe('KpiCard', () => {
  it('shows label, value and hint', () => {
    render(
      <KpiCard
        label="Tempo médio de detecção"
        value="18s"
        hint="vs. 3h30 no ataque da Suécia"
        icon={<Timer />}
      />,
    );

    expect(screen.getByText('Tempo médio de detecção')).toBeInTheDocument();
    expect(screen.getByText('18s')).toBeInTheDocument();
    expect(screen.getByText('vs. 3h30 no ataque da Suécia')).toBeInTheDocument();
  });

  it('exposes the tone used to highlight alerts', () => {
    render(<KpiCard label="Alertas ativos" value={4} icon={<Timer />} tone="critical" />);
    expect(screen.getByRole('article')).toHaveAttribute('data-tone', 'critical');
  });

  it('renders a skeleton instead of the value while loading', () => {
    render(<KpiCard label="Alertas ativos" value={4} hint="x" icon={<Timer />} isLoading />);

    expect(screen.getByText('Alertas ativos')).toBeInTheDocument();
    expect(screen.queryByText('4')).not.toBeInTheDocument();
    expect(screen.queryByText('x')).not.toBeInTheDocument();
  });
});
