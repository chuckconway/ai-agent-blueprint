import { create } from 'zustand';
import type { Message, ToolCall } from '@/types';

interface ChatState {
  messages: Message[];
  isStreaming: boolean;
  addMessage: (msg: Message) => void;
  appendToLastMessage: (content: string) => void;
  addToolCall: (toolCall: ToolCall) => void;
  setStreaming: (streaming: boolean) => void;
  clearMessages: () => void;
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  isStreaming: false,

  addMessage: (msg) =>
    set((state) => ({ messages: [...state.messages, msg] })),

  appendToLastMessage: (content) =>
    set((state) => {
      const messages = [...state.messages];
      const last = messages[messages.length - 1];
      if (last) {
        messages[messages.length - 1] = {
          ...last,
          content: last.content + content,
        };
      }
      return { messages };
    }),

  addToolCall: (toolCall) =>
    set((state) => {
      const messages = [...state.messages];
      const last = messages[messages.length - 1];
      if (last) {
        const toolCalls = [...(last.toolCalls || [])];
        const existing = toolCalls.findIndex((tc) => tc.name === toolCall.name);
        if (existing >= 0) {
          toolCalls[existing] = toolCall;
        } else {
          toolCalls.push(toolCall);
        }
        messages[messages.length - 1] = { ...last, toolCalls };
      }
      return { messages };
    }),

  setStreaming: (streaming) => set({ isStreaming: streaming }),

  clearMessages: () => set({ messages: [] }),
}));
