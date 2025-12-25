import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAdmin } from '../contexts/AdminContext';
import { Loading } from '../components/Loading';
import { showTelegramAlert } from '../utils/telegram';

interface Subscription {
  id: string;
  user_id: string;
  region: string;
  protocol: string;
  status: 'active' | 'expired' | 'cancelled';
  expires_at: string;
  created_at: string;
}

export const AdminSubscriptions: React.FC = () => {
  const navigate = useNavigate();
  const { isAdmin } = useAdmin();
  const [subscriptions, setSubscriptions] = useState<Subscription[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState<string>('all');

  useEffect(() => {
    if (!isAdmin) {
      navigate('/');
      return;
    }
    loadSubscriptions();
  }, [isAdmin]);

  const loadSubscriptions = async () => {
    try {
      setIsLoading(true);
      // TODO: Добавить endpoint в backend для получения списка подписок
      showTelegramAlert('Функция в разработке. Нужен endpoint GET /admin/subscriptions');
    } catch (error) {
      console.error('Failed to load subscriptions:', error);
      showTelegramAlert('Ошибка при загрузке подписок');
    } finally {
      setIsLoading(false);
    }
  };

  const filteredSubscriptions = subscriptions.filter(sub =>
    filterStatus === 'all' || sub.status === filterStatus
  );

  if (isLoading) {
    return <Loading />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-4">
      <div className="max-w-6xl mx-auto">
        <button
          onClick={() => navigate('/')}
          className="mb-4 text-blue-600 hover:text-blue-800 font-semibold"
        >
          ← Назад
        </button>

        <div className="bg-white rounded-lg shadow-lg p-6">
          <h1 className="text-3xl font-bold text-gray-800 mb-6">🔐 Управление подписками</h1>

          {/* Фильтры */}
          <div className="mb-6 flex gap-2 flex-wrap">
            {['all', 'active', 'expired', 'cancelled'].map((status) => (
              <button
                key={status}
                onClick={() => setFilterStatus(status)}
                className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
                  filterStatus === status
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {status === 'all' ? 'Все' : status === 'active' ? '✅ Активные' : status === 'expired' ? '⏰ Истекшие' : '❌ Отменённые'}
              </button>
            ))}
          </div>

          {/* Таблица подписок */}
          {filteredSubscriptions.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <p className="text-lg">📭 Подписок не найдено</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-100">
                  <tr>
                    <th className="px-4 py-2 text-left text-gray-700 font-semibold">ID подписки</th>
                    <th className="px-4 py-2 text-left text-gray-700 font-semibold">ID пользователя</th>
                    <th className="px-4 py-2 text-left text-gray-700 font-semibold">Регион</th>
                    <th className="px-4 py-2 text-left text-gray-700 font-semibold">Протокол</th>
                    <th className="px-4 py-2 text-left text-gray-700 font-semibold">Статус</th>
                    <th className="px-4 py-2 text-left text-gray-700 font-semibold">Истекает</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredSubscriptions.map((sub) => (
                    <tr key={sub.id} className="border-t hover:bg-gray-50">
                      <td className="px-4 py-2 text-gray-800 font-mono text-sm">{sub.id}</td>
                      <td className="px-4 py-2 text-gray-800">{sub.user_id}</td>
                      <td className="px-4 py-2 text-gray-800">{sub.region}</td>
                      <td className="px-4 py-2 text-gray-800">{sub.protocol}</td>
                      <td className="px-4 py-2">
                        <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                          sub.status === 'active'
                            ? 'bg-green-100 text-green-800'
                            : sub.status === 'expired'
                            ? 'bg-red-100 text-red-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}>
                          {sub.status === 'active' ? '✅ Активна' : sub.status === 'expired' ? '⏰ Истекла' : '❌ Отменена'}
                        </span>
                      </td>
                      <td className="px-4 py-2 text-gray-600 text-sm">
                        {new Date(sub.expires_at).toLocaleDateString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Статистика */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <h2 className="text-xl font-bold text-gray-800 mb-4">📊 Статистика подписок</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-gray-600 text-sm">Всего подписок</p>
                <p className="text-2xl font-bold text-blue-600">{filteredSubscriptions.length}</p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <p className="text-gray-600 text-sm">Активных</p>
                <p className="text-2xl font-bold text-green-600">
                  {filteredSubscriptions.filter(s => s.status === 'active').length}
                </p>
              </div>
              <div className="bg-red-50 p-4 rounded-lg">
                <p className="text-gray-600 text-sm">Истекших</p>
                <p className="text-2xl font-bold text-red-600">
                  {filteredSubscriptions.filter(s => s.status === 'expired').length}
                </p>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-gray-600 text-sm">Отменённых</p>
                <p className="text-2xl font-bold text-gray-600">
                  {filteredSubscriptions.filter(s => s.status === 'cancelled').length}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
