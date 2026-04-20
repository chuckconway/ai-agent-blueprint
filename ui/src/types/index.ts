export interface User {
  id: string;
  email: string;
  displayName: string;
}

export interface ToolCall {
  name: string;
  status: string;
}

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  toolCalls?: ToolCall[];
}

export interface ApiResponse<T> {
  status: string;
  data: T;
}
