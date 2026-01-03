import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useAdmin } from '../contexts/AdminContext';
import { apiClient } from '../services/api';
import { Loading } from '../components/Loading';
import { showTelegramAlert } from '../utils/telegram';
import type { User, Subscription } from '../types';

export const UserDetailPage: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const { isAdmin } = useAdmin();
  const [user, setUser] = useState<User | null>(null);
  const [subscriptions, setSubscriptions] = useState<Subscription[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isLoadingSubscriptions, setIsLoadingSubscriptions] = useState(false);

  useEffect(() => {
    if (!isAdmin) {
      navigate('/');
      return;
    }
    if (id) {
      loadUser();
      loadUserSubscriptions();
    }
  }, [isAdmin, id]);

  const loadUser = async () => {
    if (!id) return;
    try {
      setIsLoading(true);
      const data = await apiClient.getUser(id);
      setUser(data);
    } catch (error: any) {
      console.error('Failed to load user:', error);
      const errorMessage =
        error.response?.data?.error?.message || 'Ошибка при загрузке пользователя';
      showTelegramAlert(errorMessage);
      if (error.response?.status === 404) {
        navigate('/admin/users');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const loadUserSubscriptions = async () => {
    if (!id) return;
    try {
      setIsLoadingSubscriptions(true);
      const data = await apiClient.getUserSubscriptions(id);
      setSubscriptions(data);
    } catch (error: any) {
      console.error('Failed to load user subscriptions:', error);
      // Не показываем ошибку, если просто нет доступа - это нормально для не-админов
    } finally {
      setIsLoadingSubscriptions(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (isLoading) {
    return <Loading />;
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50 p-4">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <p className="text-center text-gray-600">Пользователь не найден</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50 p-4">
      <div className="max-w-4xl mx-auto">
        <button
          onClick={() => navigate('/admin/users')}
          className="mb-4 text-blue-600 hover:text-blue-800 font-semibold flex items-center gap-2"
        >
          <span>←</span> Назад к списку пользователей
        </button>

        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                👤 Детали пользователя
              </h1>
              <p className="text-gray-600 font-mono text-sm">{user.id}</p>
            </div>
          </div>

          <div className="space-y-6">
            {/* Основная информация */}
            <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
              <h2 className="text-xl font-bold text-gray-900 mb-4">👤 Личная информация</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Username</p>
                  <p className="text-lg font-semibold text-gray-900">{user.username || '-'}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-1">Полное имя</p>
                  <p className="text-lg font-semibold text-gray-900">{user.fullname || '-'}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-1">Telegram ID</p>
                  <p className="text-lg font-semibold text-gray-900">{user.telegram_id || '-'}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-1">Телефон</p>
                  <p className="text-lg font-semibold text-gray-900">{user.phone || '-'}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-1">Дата создания</p>
                  <p className="text-lg font-semibold text-gray-900">{formatDate(user.created_at)}</p>
                </div>
              </div>
            </div>

            {/* Статус и права */}
            <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
              <h2 className="text-xl font-bold text-gray-900 mb-4">⚙️ Статус и права</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-white rounded-lg p-4 border-2 border-blue-400">
                  <p className="text-sm text-gray-600 mb-2 font-semibold">Роль</p>
                  <span
                    className={`px-3 py-1 rounded-full text-sm font-semibold ${
                      user.role === 'admin' || user.role === 'super_admin'
                        ? 'bg-red-100 text-red-800'
                        : 'bg-green-100 text-green-800'
                    }`}
                  >
                    {user.role === 'super_admin'
                      ? '🔴 Super Admin'
                      : user.role === 'admin'
                      ? '⚙️ Admin'
                      : '👤 User'}
                  </span>
                </div>
                <div className="bg-white rounded-lg p-4 border-2 border-purple-400">
                  <p className="text-sm text-gray-600 mb-2 font-semibold">Premium</p>
                  <span
                    className={`px-3 py-1 rounded-full text-sm font-semibold ${
                      user.is_premium ? 'bg-purple-100 text-purple-800' : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    {user.is_premium ? '✅ Да' : '❌ Нет'}
                  </span>
                </div>
                <div className="bg-white rounded-lg p-4 border-2 border-green-400">
                  <p className="text-sm text-gray-600 mb-2 font-semibold">Рефералов</p>
                  <p className="text-2xl font-bold text-green-700">{user.referrals_count || 0}</p>
                </div>
              </div>
            </div>

            {/* Реферальная информация */}
            {user.referred_by && (
              <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                <h2 className="text-xl font-bold text-gray-900 mb-2">🔗 Реферальная информация</h2>
                <div>
                  <p className="text-sm text-gray-600 mb-1">Приглашен пользователем</p>
                  <p className="text-lg font-semibold text-gray-900 font-mono">{user.referred_by}</p>
                </div>
              </div>
            )}

            {/* Подписки */}
            <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold text-gray-900">🔐 Подписки пользователя</h2>
                <span className="text-sm text-gray-600 font-semibold">
                  Всего: {subscriptions.length}
                </span>
              </div>
              {isLoadingSubscriptions ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                </div>
              ) : subscriptions.length === 0 ? (
                <p className="text-gray-600 text-center py-4">У пользователя нет подписок</p>
              ) : (
                <div className="space-y-3">
                  {subscriptions.map((sub) => (
                    <div
                      key={sub.id}
                      onClick={() => navigate(`/subscriptions/${sub.id}`)}
                      className="bg-white rounded-lg p-4 border border-gray-300 hover:border-blue-400 cursor-pointer transition-colors"
                    >
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <span className="text-lg">{sub.flag}</span>
                            <span className="font-bold text-gray-900">{sub.name}</span>
                            <span className="text-sm text-gray-600">({sub.code})</span>
                          </div>
                          <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-sm">
                            <div>
                              <span className="text-gray-600">Длительность: </span>
                              <span className="font-semibold">{sub.duration} дн.</span>
                            </div>
                            <div>
                              <span className="text-gray-600">Устройств: </span>
                              <span className="font-semibold">{sub.device_count}</span>
                            </div>
                            <div>
                              <span className="text-gray-600">Начало: </span>
                              <span className="font-semibold">
                                {new Date(sub.start_date).toLocaleDateString('ru-RU')}
                              </span>
                            </div>
                            <div>
                              <span
                                className={`px-2 py-1 rounded text-xs font-semibold ${
                                  sub.status === 'active'
                                    ? 'bg-green-100 text-green-800'
                                    : sub.status === 'expired'
                                    ? 'bg-red-100 text-red-800'
                                    : 'bg-yellow-100 text-yellow-800'
                                }`}
                              >
                                {sub.status === 'active'
                                  ? '✅ Активна'
                                  : sub.status === 'expired'
                                  ? '⏰ Истекла'
                                  : '⏳ Ожидание'}
                              </span>
                            </div>
                          </div>
                          <div className="mt-2 flex flex-wrap gap-1">
                            {sub.protocol_types.map((protocol) => (
                              <span
                                key={protocol}
                                className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded font-medium"
                              >
                                {protocol}
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

