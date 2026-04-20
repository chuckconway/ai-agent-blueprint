import { api } from '@shared/services/api';
import { useChatStore } from './useChatStore';

export function useChat() {
  const { messages, addMessage, appendToLastMessage, addToolCall, setStreaming, isStreaming } =
    useChatStore();

  const sendMessage = async (content: string) => {
    addMessage({ role: 'user', content });
    addMessage({ role: 'assistant', content: '', toolCalls: [] });
    setStreaming(true);

    try {
      for await (const event of api.stream('/chat/stream', {
        message: content,
      })) {
        if (event.event === 'text_delta') {
          appendToLastMessage(event.content as string);
        } else if (event.event === 'tool_call_started') {
          addToolCall({
            name: event.name as string,
            status: 'running',
          });
        } else if (event.event === 'tool_call_completed') {
          addToolCall({
            name: event.name as string,
            status: 'done',
          });
        } else if (event.event === 'done') {
          break;
        }
      }
    } catch {
      appendToLastMessage('\n\n[Error: Failed to get response]');
    } finally {
      setStreaming(false);
    }
  };

  return { messages, sendMessage, isStreaming };
}
