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
        // Используем getUserSubscriptions для получения подписок текущего пользователя
        const userSubscriptions = await apiClient.getUserSubscriptions(user.id);
        setSubscriptions(userSubscriptions);
      } catch (error) {
        console.error('Failed to fetch subscriptions:', error);
        // Fallback на общий список подписок
        try {
          const data = await apiClient.getSubscriptions(1, 10);
          setSubscriptions(data.items);
        } catch (fallbackError) {
          console.error('Failed to fetch subscriptions (fallback):', fallbackError);
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchSubscriptions();
  }, [isAuthenticated, navigate, user]);

  if (isLoading) {
    return <Loading />;
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const getStatusColor = (status: string) => {
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

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto p-4">
        {/* Админ меню для админов */}
        <AdminMenu />

        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h1 className="text-2xl font-bold text-gray-800 mb-2">
            Добро пожаловать, {user?.first_name || user?.username || 'Пользователь'}!
          </h1>
          <p className="text-gray-600">Управляйте своими VPN подписками</p>
        </div>

        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold text-gray-800">Мои подписки</h2>
          <button
            onClick={() => navigate('/subscriptions/create')}
            className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
          >
            + Создать подписку
          </button>
        </div>

        {subscriptions.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-8 text-center">
            <p className="text-gray-600 mb-4">У вас пока нет подписок</p>
            <button
              onClick={() => navigate('/subscriptions/create')}
              className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
            >
              Создать первую подписку
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            {subscriptions.map((subscription) => (
              <div
                key={subscription.id}
                className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer"
                onClick={() => navigate(`/subscriptions/${subscription.id}`)}
              >
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-800 mb-2">
                      Подписка #{subscription.id.slice(0, 8)}
                    </h3>
                    <div className="flex flex-wrap gap-2 text-sm text-gray-600">
                      <span>Устройств: {subscription.device_count}</span>
                      <span>•</span>
                      <span>Дней: {subscription.duration_days}</span>
                      <span>•</span>
                      <span>Протоколы: {subscription.protocol_types.join(', ')}</span>
                    </div>
                  </div>
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(
                      subscription.status
                    )}`}
                  >
                    {subscription.status}
                  </span>
                </div>
                <div className="text-sm text-gray-500">
                  Истекает: {formatDate(subscription.expires_at)}
                </div>
              </div>
            ))}
          </div>
        )}

        <div className="mt-6 flex gap-4">
          <button
            onClick={() => navigate('/profile')}
            className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-2 px-4 rounded-lg transition-colors"
          >
            Профиль
          </button>
          {user?.role === 'admin' && (
            <button
              onClick={() => navigate('/servers/create')}
              className="flex-1 bg-purple-500 hover:bg-purple-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
            >
              Добавить сервер
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

