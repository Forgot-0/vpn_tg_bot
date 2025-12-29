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
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [total, setTotal] = useState(0);

  // Filters
  const [roleFilter, setRoleFilter] = useState('all');
  const [isPremiumFilter, setIsPremiumFilter] = useState<boolean | undefined>(undefined);
  const [hasSubscriptionsFilter, setHasSubscriptionsFilter] = useState<boolean | undefined>(undefined);
  const [minReferralsFilter, setMinReferralsFilter] = useState<number | undefined>(undefined);
  const [usernameFilter, setUsernameFilter] = useState('');
  const [fullnameFilter, setFullnameFilter] = useState('');
  const [phoneFilter, setPhoneFilter] = useState('');
  const [createdAfterFilter, setCreatedAfterFilter] = useState<string | undefined>(undefined);
  const [createdBeforeFilter, setCreatedBeforeFilter] = useState<string | undefined>(undefined);
  const [sortBy, setSortBy] = useState('created_at:desc');

  useEffect(() => {
    if (!isAdmin) {
      navigate('/');
      return;
    }
    loadUsers();
  }, [
    isAdmin,
    page,
    roleFilter,
    isPremiumFilter,
    hasSubscriptionsFilter,
    minReferralsFilter,
    usernameFilter,
    fullnameFilter,
    phoneFilter,
    createdAfterFilter,
    createdBeforeFilter,
    sortBy,
  ]);

  const loadUsers = async () => {
    try {
      setIsLoading(true);
      const filters: {
        role?: string;
        is_premium?: boolean;
        has_subscriptions?: boolean;
        min_referrals_count?: number;
        username?: string;
        fullname?: string;
        phone?: string;
        created_after?: string;
        created_before?: string;
      } = {};

      if (roleFilter !== 'all') {
        filters.role = roleFilter;
      }
      if (isPremiumFilter !== undefined) {
        filters.is_premium = isPremiumFilter;
      }
      if (hasSubscriptionsFilter !== undefined) {
        filters.has_subscriptions = hasSubscriptionsFilter;
      }
      if (minReferralsFilter !== undefined && minReferralsFilter > 0) {
        filters.min_referrals_count = minReferralsFilter;
      }
      if (usernameFilter.trim()) {
        filters.username = usernameFilter.trim();
      }
      if (fullnameFilter.trim()) {
        filters.fullname = fullnameFilter.trim();
      }
      if (phoneFilter.trim()) {
        filters.phone = phoneFilter.trim();
      }
      if (createdAfterFilter) {
        filters.created_after = createdAfterFilter;
      }
      if (createdBeforeFilter) {
        filters.created_before = createdBeforeFilter;
      }

      const data: PaginatedResult<User> = await apiClient.getUsers(page, 20, filters, sortBy);
      setUsers(data.items);
      setTotalPages(data.total_pages);
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

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const resetFilters = () => {
    setRoleFilter('all');
    setIsPremiumFilter(undefined);
    setHasSubscriptionsFilter(undefined);
    setMinReferralsFilter(undefined);
    setUsernameFilter('');
    setFullnameFilter('');
    setPhoneFilter('');
    setCreatedAfterFilter(undefined);
    setCreatedBeforeFilter(undefined);
    setSortBy('created_at:desc');
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
          className="mb-4 text-blue-600 hover:text-blue-800 font-semibold text-lg flex items-center gap-2 transition-colors"
        >
          <span>←</span> Назад
        </button>

        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold text-gray-900 leading-tight">👥 Управление пользователями</h1>
            <div className="text-base text-gray-700 font-semibold">
              Всего: <span className="font-bold text-blue-700 text-lg">{total}</span>
            </div>
          </div>

          {/* Filters */}
          <FilterBar
            filters={{
              role: {
                type: 'select',
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
              is_premium: {
                type: 'checkbox',
                label: 'Premium пользователи',
                value: isPremiumFilter,
                onChange: (value) => {
                  setIsPremiumFilter(value);
                  setPage(1);
                },
              },
              has_subscriptions: {
                type: 'checkbox',
                label: 'С подписками',
                value: hasSubscriptionsFilter,
                onChange: (value) => {
                  setHasSubscriptionsFilter(value);
                  setPage(1);
                },
              },
              min_referrals: {
                type: 'number',
                label: 'Мин. рефералов',
                value: minReferralsFilter,
                onChange: (value) => {
                  setMinReferralsFilter(value);
                  setPage(1);
                },
                min: 0,
                placeholder: '0',
              },
              username: {
                type: 'text',
                label: 'Username',
                value: usernameFilter,
                onChange: (value) => {
                  setUsernameFilter(value);
                  setPage(1);
                },
                placeholder: 'Поиск по username',
              },
              fullname: {
                type: 'text',
                label: 'Полное имя',
                value: fullnameFilter,
                onChange: (value) => {
                  setFullnameFilter(value);
                  setPage(1);
                },
                placeholder: 'Поиск по имени',
              },
              phone: {
                type: 'text',
                label: 'Телефон',
                value: phoneFilter,
                onChange: (value) => {
                  setPhoneFilter(value);
                  setPage(1);
                },
                placeholder: 'Поиск по телефону',
              },
              created_after: {
                type: 'date',
                label: 'Создан после',
                value: createdAfterFilter,
                onChange: (value) => {
                  setCreatedAfterFilter(value);
                  setPage(1);
                },
              },
              created_before: {
                type: 'date',
                label: 'Создан до',
                value: createdBeforeFilter,
                onChange: (value) => {
                  setCreatedBeforeFilter(value);
                  setPage(1);
                },
              },
              sort: {
                type: 'select',
                label: 'Сортировка',
                options: [
                  { value: 'created_at:desc', label: 'По дате создания (новые)' },
                  { value: 'created_at:asc', label: 'По дате создания (старые)' },
                  { value: 'username:asc', label: 'По username (А-Я)' },
                  { value: 'username:desc', label: 'По username (Я-А)' },
                  { value: 'referrals_count:desc', label: 'По рефералам (больше)' },
                  { value: 'referrals_count:asc', label: 'По рефералам (меньше)' },
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

          {/* Table */}
          {users.length === 0 ? (
            <div className="text-center py-12 text-gray-600">
              <p className="text-xl font-semibold">Пользователей не найдено</p>
            </div>
          ) : (
            <div className="overflow-x-auto rounded-lg border border-gray-200">
              <table className="w-full">
                <thead className="bg-gray-800">
                  <tr>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">ID</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">Username</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">Имя</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">Telegram ID</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">Роль</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">Premium</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">Рефералов</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">Создан</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((user) => (
                    <tr
                      key={user.id}
                      className="border-t border-gray-200 bg-white hover:bg-blue-50 transition-colors cursor-pointer"
                    >
                      <td className="px-4 py-4 text-gray-900 font-mono text-sm font-semibold">{user.id.slice(0, 8)}...</td>
                      <td className="px-4 py-4 text-gray-900 font-semibold text-base">{user.username || '-'}</td>
                      <td className="px-4 py-4 text-gray-900 font-medium text-base">{user.fullname || '-'}</td>
                      <td className="px-4 py-4 text-gray-900 font-medium text-base">{user.telegram_id || '-'}</td>
                      <td className="px-4 py-4">
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
                      <td className="px-4 py-4">
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${user.is_premium ? 'bg-purple-100 text-purple-800' : 'bg-gray-100 text-gray-800'}`}>
                          {user.is_premium ? '✅ Да' : '❌ Нет'}
                        </span>
                      </td>
                      <td className="px-4 py-4 text-gray-900 font-semibold text-base">{user.referrals_count || 0}</td>
                      <td className="px-4 py-4 text-gray-700 text-base font-medium">{formatDate(user.created_at)}</td>
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
                className="px-5 py-2.5 bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-base"
              >
                ← Назад
              </button>
              <span className="text-gray-700 font-semibold text-base">
                Страница {page} из {totalPages} (всего: {total})
              </span>
              <button
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                className="px-5 py-2.5 bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-base"
              >
                Вперед →
              </button>
            </div>
          )}

          {/* Statistics */}
          <div className="mt-8 pt-6 border-t-2 border-gray-300">
            <h2 className="text-2xl font-bold text-gray-900 mb-4 leading-tight">📊 Статистика</h2>
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
