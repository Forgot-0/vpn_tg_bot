import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAdmin } from '../contexts/AdminContext';
import { apiClient } from '../services/api';
import { Loading } from '../components/Loading';
import { showTelegramAlert } from '../utils/telegram';
import type { User } from '../types';

export const AdminUsers: React.FC = () => {
  const navigate = useNavigate();
  const { isAdmin } = useAdmin();
  const [users, setUsers] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    if (!isAdmin) {
      navigate('/');
      return;
    }
    loadUsers();
  }, [isAdmin]);

  const loadUsers = async () => {
    try {
      setIsLoading(true);
      // TODO: Добавить endpoint в backend для получения списка пользователей
      // const data = await apiClient.getAllUsers();
      // setUsers(data);
      showTelegramAlert('Функция в разработке. Нужен endpoint GET /admin/users');
    } catch (error) {
      console.error('Failed to load users:', error);
      showTelegramAlert('Ошибка при загрузке пользователей');
    } finally {
      setIsLoading(false);
    }
  };

  const filteredUsers = users.filter(user =>
    user.email?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    user.telegram_id?.toString().includes(searchQuery)
  );

  if (isLoading) {
    return <Loading />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-4">
      <div className="max-w-4xl mx-auto">
        <button
          onClick={() => navigate('/')}
          className="mb-4 text-blue-600 hover:text-blue-800 font-semibold"
        >
          ← Назад
        </button>

        <div className="bg-white rounded-lg shadow-lg p-6">
          <h1 className="text-3xl font-bold text-gray-800 mb-6">👥 Управление пользователями</h1>

          {/* Поиск */}
          <div className="mb-6">
            <input
              type="text"
              placeholder="Поиск по email или Telegram ID..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Таблица пользователей */}
          {filteredUsers.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <p className="text-lg">Пользователей не найдено</p>
              <p className="text-sm">Эндпоинт для получения списка ещё не реализован</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-100">
                  <tr>
                    <th className="px-4 py-2 text-left text-gray-700 font-semibold">ID</th>
                    <th className="px-4 py-2 text-left text-gray-700 font-semibold">Email</th>
                    <th className="px-4 py-2 text-left text-gray-700 font-semibold">Telegram ID</th>
                    <th className="px-4 py-2 text-left text-gray-700 font-semibold">Роль</th>
                    <th className="px-4 py-2 text-left text-gray-700 font-semibold">Действия</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredUsers.map((user) => (
                    <tr key={user.id} className="border-t hover:bg-gray-50">
                      <td className="px-4 py-2 text-gray-800">{user.id}</td>
                      <td className="px-4 py-2 text-gray-800">{user.email}</td>
                      <td className="px-4 py-2 text-gray-800">{user.telegram_id}</td>
                      <td className="px-4 py-2">
                        <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                          user.role === 'admin'
                            ? 'bg-red-100 text-red-800'
                            : 'bg-green-100 text-green-800'
                        }`}>
                          {user.role === 'admin' ? '⚙️ Admin' : '👤 User'}
                        </span>
                      </td>
                      <td className="px-4 py-2">
                        <button
                          onClick={() => showTelegramAlert('Функция в разработке')}
                          className="text-blue-600 hover:text-blue-800 font-semibold text-sm"
                        >
                          Подробнее
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Статистика */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <h2 className="text-xl font-bold text-gray-800 mb-4">📊 Статистика</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-gray-600 text-sm">Всего пользователей</p>
                <p className="text-2xl font-bold text-blue-600">{filteredUsers.length}</p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <p className="text-gray-600 text-sm">Обычных юзеров</p>
                <p className="text-2xl font-bold text-green-600">{filteredUsers.filter(u => u.role !== 'admin').length}</p>
              </div>
              <div className="bg-red-50 p-4 rounded-lg">
                <p className="text-gray-600 text-sm">Администраторов</p>
                <p className="text-2xl font-bold text-red-600">{filteredUsers.filter(u => u.role === 'admin').length}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
