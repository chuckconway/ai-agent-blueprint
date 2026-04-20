import { Layout } from '@shared/components/ui';
import { useAuth } from '@features/auth/useAuth';
import { MessageList } from './MessageList';
import { ChatInput } from './ChatInput';
import { useChat } from './useChat';

export function ChatPage() {
  const { logout } = useAuth();
  const { messages, sendMessage, isStreaming } = useChat();

  return (
    <Layout onLogout={logout}>
      <div className="flex flex-1 flex-col overflow-hidden">
        <MessageList messages={messages} />
        <ChatInput onSend={sendMessage} disabled={isStreaming} />
      </div>
    </Layout>
  );
}
