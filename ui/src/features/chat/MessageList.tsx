import { useEffect, useRef } from 'react';
import type { Message } from '@/types';

interface MessageListProps {
  messages: Message[];
}

export function MessageList({ messages }: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className="flex flex-1 items-center justify-center">
        <p className="text-sm text-slate-500">
          Send a message to start a conversation.
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-1 flex-col gap-4 overflow-y-auto px-4 py-6">
      {messages.map((msg, i) => (
        <div
          key={i}
          className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
        >
          <div className="flex max-w-[70%] flex-col gap-1">
            {msg.toolCalls && msg.toolCalls.length > 0 && (
              <div className="flex flex-wrap gap-1">
                {msg.toolCalls.map((tc, j) => (
                  <span
                    key={j}
                    className="rounded bg-slate-700 px-2 py-0.5 text-xs text-slate-400"
                  >
                    {tc.name}: {tc.status}
                  </span>
                ))}
              </div>
            )}
            <div
              className={`rounded-lg px-4 py-3 text-sm whitespace-pre-wrap ${
                msg.role === 'user'
                  ? 'bg-indigo-900/30 text-slate-200'
                  : 'bg-slate-800 text-slate-300'
              }`}
            >
              {msg.content || (
                <span className="text-slate-500">Thinking...</span>
              )}
            </div>
          </div>
        </div>
      ))}
      <div ref={bottomRef} />
    </div>
  );
}
