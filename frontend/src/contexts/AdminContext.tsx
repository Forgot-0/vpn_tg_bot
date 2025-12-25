import React, { createContext, useContext, ReactNode } from 'react';
import { useAuth } from './AuthContext';

interface AdminContextType {
  isAdmin: boolean;
  canManageServers: boolean;
  canManageUsers: boolean;
  canManagePayments: boolean;
}

const AdminContext = createContext<AdminContextType | undefined>(undefined);

export const AdminProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const { user } = useAuth();

  // Проверяем роль пользователя (admin или super_admin)
  const isAdmin = user?.role === 'admin' || user?.role === 'super_admin';
  const canManageServers = isAdmin;
  const canManageUsers = isAdmin;
  const canManagePayments = isAdmin;

  return (
    <AdminContext.Provider
      value={{
        isAdmin,
        canManageServers,
        canManageUsers,
        canManagePayments,
      }}
    >
      {children}
    </AdminContext.Provider>
  );
};

export const useAdmin = () => {
  const context = useContext(AdminContext);
  if (context === undefined) {
    throw new Error('useAdmin must be used within an AdminProvider');
  }
  return context;
};
