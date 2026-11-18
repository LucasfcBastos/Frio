import { Compass } from 'lucide-react';
import { Link } from 'react-router-dom';

import { AppLayout } from '@/components/layout';
import { Card, EmptyState } from '@/components/ui';
import { useI18n } from '@/contexts/LocaleContext';

import styles from './NotFoundPage.module.css';

export function NotFoundPage() {
  const { messages } = useI18n();
  return (
    <AppLayout>
      <Card>
        <EmptyState
          icon={<Compass />}
          title={messages.notFound.title}
          description={messages.notFound.description}
          action={
            <Link to="/" className={styles.link}>
              {messages.notFound.back}
            </Link>
          }
        />
      </Card>
    </AppLayout>
  );
}
