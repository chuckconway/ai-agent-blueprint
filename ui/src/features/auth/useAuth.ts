import { api } from '@shared/services/api';
import { useAppStore } from '@shared/stores/useAppStore';

interface LoginResponse {
  access_token: string;
  token_type: string;
  user: { id: string; email: string; display_name: string };
}

interface MeResponse {
  user_id: string;
  email: string;
  display_name: string;
}

export function useAuth() {
  const { user, setUser } = useAppStore();

  const login = async (email: string, password: string) => {
    const res = await api.post<LoginResponse>('/auth/login', {
      email,
      password,
    });
    api.setToken(res.access_token);
    localStorage.setItem('token', res.access_token);
    setUser({
      id: res.user.id,
      email: res.user.email,
      displayName: res.user.display_name,
    });
  };

  const logout = () => {
    api.setToken(null);
    localStorage.removeItem('token');
    setUser(null);
  };

  const restore = async (): Promise<boolean> => {
    const token = localStorage.getItem('token');
    if (!token) return false;
    api.setToken(token);
    try {
      const res = await api.get<MeResponse>('/auth/me');
      setUser({
        id: res.user_id,
        email: res.email,
        displayName: res.display_name,
      });
      return true;
    } catch {
      logout();
      return false;
    }
  };

  return { user, login, logout, restore, isAuthenticated: !!user };
}
