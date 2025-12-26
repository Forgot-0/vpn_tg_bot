import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAdmin } from '../contexts/AdminContext';
import { apiClient } from '../services/api';
import { Loading } from '../components/Loading';
import { FilterBar } from '../components/FilterBar';
import { showTelegramAlert } from '../utils/telegram';
import type { User, PaginatedResult } from '../types';

export const AdminUsers: React.FC = () => {
  const navigate = useNavigate();
  const { isAdmin } = useAdmin();
  const [users, setUsers] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [total, setTotal] = useState(0);
  const [roleFilter, setRoleFilter] = useState('all');
  const [sortBy, setSortBy] = useState('created_at');

  useEffect(() => {
    if (!isAdmin) {
      navigate('/');
      return;
    }
    loadUsers();
  }, [isAdmin, page, roleFilter, sortBy]);

  const loadUsers = async () => {
    try {
      setIsLoading(true);
      const filters: { [key: string]: string } = {};
      if (roleFilter !== 'all') {
        filters.role = roleFilter;
      }
      const data: PaginatedResult<User> = await apiClient.getUsers(page, 20, filters, sortBy);
      setUsers(data.items);
      setTotalPages(data.pages);
      setTotal(data.total);
    } catch (error: any) {
      console.error('Failed to load users:', error);
      const errorMessage =
        error.response?.data?.error?.message ||
        'Ошибка при загрузке пользователей. Убедитесь, что у вас есть права администратора.';
      showTelegramAlert(errorMessage);
      if (error.response?.status === 403 || error.response?.status === 401) {
        navigate('/');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const filteredUsers = users.filter(
    (user) =>
      user.username?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      user.fullname?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      user.telegram_id?.toString().includes(searchQuery) ||
      user.id.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const resetFilters = () => {
    setRoleFilter('all');
    setSortBy('created_at');
    setSearchQuery('');
    setPage(1);
  };

  if (isLoading) {
    return <Loading />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50 p-4">
      <div className="max-w-7xl mx-auto">
        <button
          onClick={() => navigate('/')}
          className="mb-4 text-blue-600 hover:text-blue-800 font-semibold flex items-center gap-2"
        >
          <span>←</span> Назад
        </button>

        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold text-gray-800">👥 Управление пользователями</h1>
            <div className="text-sm text-gray-600">
              Всего: <span className="font-semibold text-blue-600">{total}</span>
            </div>
          </div>

          {/* Filters */}
          <FilterBar
            filters={{
              role: {
                label: 'Роль',
                options: [
                  { value: 'all', label: 'Все роли' },
                  { value: 'user', label: '👤 Пользователь' },
                  { value: 'admin', label: '⚙️ Администратор' },
                  { value: 'super_admin', label: '🔴 Super Admin' },
                ],
                value: roleFilter,
                onChange: (value) => {
                  setRoleFilter(value);
                  setPage(1);
                },
              },
              sort: {
                label: 'Сортировка',
                options: [
                  { value: 'created_at', label: 'По дате создания' },
                  { value: 'username', label: 'По username' },
                  { value: 'referrals_count', label: 'По рефералам' },
                ],
                value: sortBy,
                onChange: (value) => {
                  setSortBy(value);
                  setPage(1);
                },
              },
            }}
            onReset={resetFilters}
          />

          {/* Search */}
          <div className="mb-6">
            <input
              type="text"
              placeholder="🔍 Поиск по username, имени, Telegram ID или ID..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-4 py-3 border-2 border-gray-400 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-600 shadow-md bg-white text-gray-900 font-medium"
            />
          </div>

          {/* Table */}
          {filteredUsers.length === 0 && users.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <p className="text-lg">Пользователей не найдено</p>
            </div>
          ) : (
            <div className="overflow-x-auto rounded-lg border border-gray-200">
              <table className="w-full">
                <thead className="bg-gray-800">
                  <tr>
                    <th className="px-4 py-3 text-left text-white font-bold">ID</th>
                    <th className="px-4 py-3 text-left text-white font-bold">Username</th>
                    <th className="px-4 py-3 text-left text-white font-bold">Имя</th>
                    <th className="px-4 py-3 text-left text-white font-bold">Telegram ID</th>
                    <th className="px-4 py-3 text-left text-white font-bold">Роль</th>
                    <th className="px-4 py-3 text-left text-white font-bold">Создан</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredUsers.map((user) => (
                    <tr
                      key={user.id}
                      className="border-t border-gray-200 bg-white hover:bg-blue-50 transition-colors cursor-pointer"
                    >
                      <td className="px-4 py-3 text-gray-900 font-mono text-xs font-semibold">{user.id.slice(0, 8)}...</td>
                      <td className="px-4 py-3 text-gray-900 font-semibold">{user.username || '-'}</td>
                      <td className="px-4 py-3 text-gray-900 font-medium">{user.fullname || '-'}</td>
                      <td className="px-4 py-3 text-gray-900 font-medium">{user.telegram_id || '-'}</td>
                      <td className="px-4 py-3">
                        <span
                          className={`px-3 py-1 rounded-full text-xs font-semibold ${
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
                      </td>
                      <td className="px-4 py-3 text-gray-700 text-sm font-medium">{formatDate(user.created_at)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="mt-6 flex justify-center items-center gap-3">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page === 1}
                className="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                ← Назад
              </button>
              <span className="text-gray-600 font-medium">
                Страница {page} из {totalPages} (всего: {total})
              </span>
              <button
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                className="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Вперед →
              </button>
            </div>
          )}

          {/* Statistics */}
          <div className="mt-8 pt-6 border-t-2 border-gray-300">
            <h2 className="text-xl font-bold text-gray-900 mb-4">📊 Статистика</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-white border-2 border-blue-400 p-5 rounded-lg shadow-md">
                <p className="text-gray-700 text-sm mb-2 font-semibold">Всего пользователей</p>
                <p className="text-4xl font-bold text-blue-700">{total}</p>
              </div>
              <div className="bg-white border-2 border-green-400 p-5 rounded-lg shadow-md">
                <p className="text-gray-700 text-sm mb-2 font-semibold">Обычных юзеров</p>
                <p className="text-4xl font-bold text-green-700">
                  {users.filter((u) => u.role === 'user').length}
                </p>
              </div>
              <div className="bg-white border-2 border-red-400 p-5 rounded-lg shadow-md">
                <p className="text-gray-700 text-sm mb-2 font-semibold">Администраторов</p>
                <p className="text-4xl font-bold text-red-700">
                  {users.filter((u) => u.role === 'admin' || u.role === 'super_admin').length}
                </p>
              </div>
              <div className="bg-white border-2 border-purple-400 p-5 rounded-lg shadow-md">
                <p className="text-gray-700 text-sm mb-2 font-semibold">Premium</p>
                <p className="text-4xl font-bold text-purple-700">
                  {users.filter((u) => u.is_premium).length}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
