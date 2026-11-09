import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { api, getStoredUser } from '../services/api';

export interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'pendamping';
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, pin: string) => Promise<{ success: boolean; error?: string }>;
  logout: () => Promise<void>;
  checkUserStatus: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(getStoredUser());
  const [loading, setLoading] = useState(true);

  const checkUserStatus = useCallback(async () => {
    try {
      const activeUser = await api.checkAuth();
      setUser(activeUser);
    } catch (e) {
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  const login = async (email: string, pin: string) => {
    try {
      const result = await api.login(email, pin);
      if (result.success) {
        // Refresh authenticated user state
        const activeUser = await api.checkAuth();
        setUser(activeUser || result.user || null);
        return { success: true };
      } else {
        return { success: false, error: result.error || 'Email atau PIN salah.' };
      }
    } catch (e) {
      return { success: false, error: 'Koneksi ke server gagal.' };
    }
  };

  const logout = async () => {
    try {
      await api.logout();
    } catch (e) {
      // ignore
    } finally {
      setUser(null);
    }
  };

  useEffect(() => {
    checkUserStatus();
  }, [checkUserStatus]);

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, checkUserStatus }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
