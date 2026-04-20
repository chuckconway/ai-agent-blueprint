import { Routes, Route, Navigate } from 'react-router-dom';
import { LoginPage } from '@features/auth/LoginPage';
import { AuthGuard } from '@features/auth/AuthGuard';
import { ChatPage } from '@features/chat/ChatPage';

export function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/"
        element={
          <AuthGuard>
            <ChatPage />
          </AuthGuard>
        }
      />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
