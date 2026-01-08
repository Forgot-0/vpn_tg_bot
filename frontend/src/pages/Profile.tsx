import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export const Profile: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      <div className="max-w-3xl mx-auto p-4">
        <button
          onClick={() => navigate('/')}
          className="mb-4 text-blue-600 hover:text-blue-800 font-semibold flex items-center gap-2"
        >
          <span>←</span> Назад
        </button>

        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
          <div className="flex items-center gap-4 mb-6 pb-6 border-b border-gray-200">
            <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center text-white text-2xl font-bold">
              {user?.fullname?.[0] || user?.username?.[0] || 'U'}
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900 leading-tight">Профиль</h1>
              <p className="text-gray-700 text-lg font-medium">Информация о вашем аккаунте</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white border-2 border-blue-300 rounded-lg p-5 shadow-md">
              <label className="block text-sm font-bold text-blue-900 mb-2 uppercase tracking-wide">
                Telegram ID
              </label>
              <div className="text-gray-900 font-bold text-lg">{user?.telegram_id || 'Не указано'}</div>
            </div>

            <div className="bg-white border-2 border-green-300 rounded-lg p-5 shadow-md">
              <label className="block text-sm font-bold text-green-900 mb-2 uppercase tracking-wide">
                Username
              </label>
              <div className="text-gray-900 font-bold text-lg">
                {user?.username || user?.fullname || 'Не указано'}
              </div>
            </div>

            <div className="bg-white border-2 border-purple-300 rounded-lg p-5 shadow-md">
              <label className="block text-sm font-bold text-purple-900 mb-2 uppercase tracking-wide">
                Полное имя
              </label>
              <div className="text-gray-900 font-bold text-lg">{user?.fullname || 'Не указано'}</div>
            </div>

            <div className="bg-white border-2 border-orange-300 rounded-lg p-5 shadow-md">
              <label className="block text-sm font-bold text-orange-900 mb-2 uppercase tracking-wide">
                Телефон
              </label>
              <div className="text-gray-900 font-bold text-lg">{user?.phone || 'Не указано'}</div>
            </div>

            <div className="bg-white border-2 border-indigo-300 rounded-lg p-5 shadow-md">
              <label className="block text-sm font-bold text-indigo-900 mb-2 uppercase tracking-wide">
                Роль
              </label>
              <div className="text-gray-900 font-bold text-lg">
                {user?.role === 'owner'
                  ? '👑 Owner'
                  : user?.role === 'super_admin'
                  ? '🔴 Super Admin'
                  : user?.role === 'admin'
                  ? '⚙️ Администратор'
                  : '👤 Пользователь'}
              </div>
            </div>

            <div className="bg-white border-2 border-pink-300 rounded-lg p-5 shadow-md">
              <label className="block text-sm font-bold text-pink-900 mb-2 uppercase tracking-wide">
                Premium
              </label>
              <div className="text-gray-900 font-bold text-lg">
                {user?.is_premium ? '✅ Да' : '❌ Нет'}
              </div>
            </div>

            {user?.created_at && (
              <div className="bg-white border-2 border-gray-300 rounded-lg p-5 shadow-md md:col-span-2">
                <label className="block text-sm font-bold text-gray-800 mb-2 uppercase tracking-wide">
                  Дата регистрации
                </label>
                <div className="text-gray-900 font-bold text-lg">{formatDate(user.created_at)}</div>
              </div>
            )}

            {user?.referrals_count !== undefined && user.referrals_count > 0 && (
              <div className="bg-white border-2 border-yellow-300 rounded-lg p-5 shadow-md md:col-span-2">
                <label className="block text-sm font-bold text-yellow-900 mb-2 uppercase tracking-wide">
                  Рефералов
                </label>
                <div className="text-gray-900 font-bold text-4xl">{user.referrals_count}</div>
              </div>
            )}
          </div>
        </div>

        {/* Actions */}
        <div className="mt-6 flex gap-4">
          <button
            onClick={() => navigate('/')}
            className="flex-1 bg-white hover:bg-gray-50 text-gray-800 font-semibold py-3 px-4 rounded-lg transition-all shadow-md hover:shadow-lg border border-gray-200"
          >
            Назад
          </button>
          <button
            onClick={handleLogout}
            className="flex-1 bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white font-semibold py-3 px-4 rounded-lg transition-all shadow-md hover:shadow-lg"
          >
            Выйти
          </button>
        </div>
      </div>
    </div>
  );
};
