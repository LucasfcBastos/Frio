import { Route, Routes } from 'react-router-dom';

import { DashboardPage } from '@/pages/DashboardPage';
import { NotFoundPage } from '@/pages/NotFoundPage';

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<DashboardPage />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}
