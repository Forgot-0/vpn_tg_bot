import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { AdminMenu } from '../components/AdminMenu';
import { apiClient } from '../services/api';
import { Loading } from '../components/Loading';
import type { Subscription } from '../types';

export const Home: React.FC = () => {
  const { user, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [subscriptions, setSubscriptions] = useState<Subscription[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    const fetchSubscriptions = async () => {
      if (!user) return;

      try {
        const userSubscriptions = await apiClient.getUserSubscriptions(user.id);
        setSubscriptions(userSubscriptions);
      } catch (error) {
        console.error('Failed to fetch subscriptions:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchSubscriptions();
  }, [isAuthenticated, navigate, user]);

  if (isLoading) {
    return <Loading />;
  }

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'Не указано';
    return new Date(dateString).toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const getStatusColor = (status?: string) => {
    if (!status) return 'bg-gray-100 text-gray-800';
    switch (status.toLowerCase()) {
      case 'active':
        return 'bg-green-100 text-green-800';
      case 'expired':
        return 'bg-red-100 text-red-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  // Вычисляем дату истечения
  const calculateExpiresAt = (subscription: Subscription) => {
    if (subscription.start_date && subscription.duration) {
      const startDate = new Date(subscription.start_date);
      const expiresDate = new Date(startDate);
      expiresDate.setDate(expiresDate.getDate() + subscription.duration);
      return expiresDate.toISOString();
    }
    return subscription.expires_at;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      <div className="max-w-5xl mx-auto p-4">
        {/* Админ меню для админов */}
        <AdminMenu />

        {/* Welcome Card */}
        <div className="bg-gradient-to-r from-blue-500 to-indigo-600 rounded-xl shadow-lg p-6 mb-6 text-white">
          <h1 className="text-3xl font-bold mb-2">
            Добро пожаловать, {user?.fullname || user?.username || 'Пользователь'}! 👋
          </h1>
          <p className="text-blue-100">Управляйте своими VPN подписками</p>
        </div>

        {/* Actions Bar */}
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-800">Мои подписки</h2>
          <button
            onClick={() => navigate('/subscriptions/create')}
            className="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-all shadow-md hover:shadow-lg flex items-center gap-2"
          >
            <span>+</span> Создать подписку
          </button>
        </div>

        {/* Subscriptions List */}
        {subscriptions.length === 0 ? (
          <div className="bg-white rounded-xl shadow-lg p-12 text-center border border-gray-200">
            <div className="text-6xl mb-4">🔐</div>
            <p className="text-xl text-gray-700 mb-2 font-semibold">У вас пока нет подписок</p>
            <p className="text-gray-500 mb-6">Создайте первую подписку для начала работы</p>
            <button
              onClick={() => navigate('/subscriptions/create')}
              className="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition-all shadow-md hover:shadow-lg"
            >
              Создать первую подписку
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {subscriptions.map((subscription) => {
              const expiresAt = calculateExpiresAt(subscription);
              return (
                <div
                  key={subscription.id}
                  className="bg-white rounded-xl shadow-md p-6 hover:shadow-xl transition-all cursor-pointer border border-gray-200 card-hover"
                  onClick={() => navigate(`/subscriptions/${subscription.id}`)}
                >
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex-1">
                      <h3 className="text-lg font-bold text-gray-800 mb-2">
                        {subscription.flag} {subscription.name}
                      </h3>
                      <p className="text-sm text-gray-500 font-mono mb-3">
                        #{subscription.id.slice(0, 8)}...
                      </p>
                      <div className="flex flex-wrap gap-2 mb-3">
                        <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded font-medium">
                          {subscription.device_count} устройств
                        </span>
                        <span className="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded font-medium">
                          {subscription.duration} дней
                        </span>
                      </div>
                      <div className="flex flex-wrap gap-1 mb-3">
                        {subscription.protocol_types.map((protocol) => (
                          <span
                            key={protocol}
                            className="px-2 py-1 bg-indigo-100 text-indigo-800 text-xs rounded font-medium"
                          >
                            {protocol}
                          </span>
                        ))}
                      </div>
                    </div>
                    {subscription.status && (
                      <span
                        className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(
                          subscription.status
                        )}`}
                      >
                        {subscription.status === 'active'
                          ? '✅ Активна'
                          : subscription.status === 'expired'
                          ? '⏰ Истекла'
                          : '⏳ Ожидание'}
                      </span>
                    )}
                  </div>
                  {expiresAt && (
                    <div className="text-sm text-gray-600 border-t pt-3 mt-3">
                      <span className="font-medium">Истекает:</span> {formatDate(expiresAt)}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {/* Bottom Actions */}
        <div className="mt-6 flex gap-4">
          <button
            onClick={() => navigate('/profile')}
            className="flex-1 bg-white hover:bg-gray-50 text-gray-800 font-semibold py-3 px-4 rounded-lg transition-all shadow-md hover:shadow-lg border border-gray-200"
          >
            👤 Профиль
          </button>
          {user?.role === 'admin' || user?.role === 'super_admin' ? (
            <button
              onClick={() => navigate('/servers/create')}
              className="flex-1 bg-gradient-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700 text-white font-semibold py-3 px-4 rounded-lg transition-all shadow-md hover:shadow-lg"
            >
              🖥️ Добавить сервер
            </button>
          ) : null}
        </div>
      </div>
    </div>
  );
};
