import type { ReactNode } from 'react';
import { useAppStore } from '@shared/stores/useAppStore';
import { Button } from './Button';

interface LayoutProps {
  children: ReactNode;
  onLogout: () => void;
}

export function Layout({ children, onLogout }: LayoutProps) {
  const user = useAppStore((s) => s.user);

  return (
    <div className="flex h-screen flex-col bg-slate-950">
      <nav className="flex items-center justify-between border-b border-slate-800 bg-slate-900 px-6 py-3">
        <span className="text-sm font-semibold text-slate-200">
          AI Agent Blueprint
        </span>
        <div className="flex items-center gap-4">
          {user && (
            <span className="text-sm text-slate-400">{user.email}</span>
          )}
          <Button variant="ghost" onClick={onLogout}>
            Logout
          </Button>
        </div>
      </nav>
      <main className="flex flex-1 flex-col overflow-hidden">{children}</main>
    </div>
  );
}
