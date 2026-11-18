import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';
import { BrowserRouter } from 'react-router-dom';

import { LocaleProvider } from '@/contexts/LocaleContext';
import { StoreProvider } from '@/contexts/StoreContext';
import { AppRoutes } from '@/routes/AppRoutes';

export function App() {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: { retry: 1, refetchOnWindowFocus: true, staleTime: 2_000 },
        },
      }),
  );

  return (
    <QueryClientProvider client={queryClient}>
      <LocaleProvider>
        <BrowserRouter>
          <StoreProvider>
            <AppRoutes />
          </StoreProvider>
        </BrowserRouter>
      </LocaleProvider>
    </QueryClientProvider>
  );
}
