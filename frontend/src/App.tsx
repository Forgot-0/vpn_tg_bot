import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ErrorBoundary } from './components/ErrorBoundary';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { AdminProvider } from './contexts/AdminContext';
import { Login } from './pages/Login';
import { Home } from './pages/Home';
import { Profile } from './pages/Profile';
import { CreateSubscription } from './pages/CreateSubscription';
import { SubscriptionDetail } from './pages/SubscriptionDetail';
import { CreateServer } from './pages/CreateServer';
import { AdminUsers } from './pages/AdminUsers';
import { AdminServers } from './pages/AdminServers';
import { AdminPayments } from './pages/AdminPayments';
import { AdminSubscriptions } from './pages/AdminSubscriptions';
import { AdminRoute } from './components/AdminRoute';
import { Loading } from './components/Loading';
import './App.css';

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <Loading />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

const AppRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Home />
          </ProtectedRoute>
        }
      />
      <Route
        path="/profile"
        element={
          <ProtectedRoute>
            <Profile />
          </ProtectedRoute>
        }
      />
      <Route
        path="/subscriptions/create"
        element={
          <ProtectedRoute>
            <CreateSubscription />
          </ProtectedRoute>
        }
      />
      <Route
        path="/subscriptions/:id"
        element={
          <ProtectedRoute>
            <SubscriptionDetail />
          </ProtectedRoute>
        }
      />
      <Route
        path="/servers/create"
        element={
          <ProtectedRoute>
            <CreateServer />
          </ProtectedRoute>
        }
      />
      
      {/* Admin routes */}
      <Route
        path="/admin/users"
        element={
          <ProtectedRoute>
            <AdminRoute>
              <AdminUsers />
            </AdminRoute>
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/servers"
        element={
          <ProtectedRoute>
            <AdminRoute>
              <AdminServers />
            </AdminRoute>
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/payments"
        element={
          <ProtectedRoute>
            <AdminRoute>
              <AdminPayments />
            </AdminRoute>
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/subscriptions"
        element={
          <ProtectedRoute>
            <AdminRoute>
              <AdminSubscriptions />
            </AdminRoute>
          </ProtectedRoute>
        }
      />
      
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <AuthProvider>
          <AdminProvider>
            <AppRoutes />
          </AdminProvider>
        </AuthProvider>
      </BrowserRouter>
    </ErrorBoundary>
  );
};

export default App;

