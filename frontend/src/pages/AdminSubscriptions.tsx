import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAdmin } from '../contexts/AdminContext';
import { apiClient } from '../services/api';
import { Loading } from '../components/Loading';
import { FilterBar } from '../components/FilterBar';
import { showTelegramAlert } from '../utils/telegram';
import type { Subscription, PaginatedResult } from '../types';

export const AdminSubscriptions: React.FC = () => {
  const navigate = useNavigate();
  const { isAdmin } = useAdmin();
  const [subscriptions, setSubscriptions] = useState<Subscription[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [total, setTotal] = useState(0);
  const [statusFilter, setStatusFilter] = useState('all');
  const [regionFilter, setRegionFilter] = useState('all');
  const [sortBy, setSortBy] = useState('start_date');

  useEffect(() => {
    if (!isAdmin) {
      navigate('/');
      return;
    }
    loadSubscriptions();
  }, [isAdmin, page, statusFilter, regionFilter, sortBy]);

  const loadSubscriptions = async () => {
    try {
      setIsLoading(true);
      const filters: { [key: string]: string } = {};
      if (statusFilter !== 'all') {
        filters.status = statusFilter;
      }
      if (regionFilter !== 'all') {
        filters.region = regionFilter;
      }
      const data: PaginatedResult<Subscription> = await apiClient.getSubscriptions(
        page,
        20,
        filters,
        sortBy
      );
      setSubscriptions(data.items);
      setTotalPages(data.pages);
      setTotal(data.total);
    } catch (error: any) {
      console.error('Failed to load subscriptions:', error);
      const errorMessage =
        error.response?.data?.error?.message ||
        'Ошибка при загрузке подписок. Убедитесь, что у вас есть права администратора.';
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
    setStatusFilter('all');
    setRegionFilter('all');
    setSortBy('start_date');
    setPage(1);
  };

  // Получаем уникальные регионы
  const uniqueRegions = Array.from(new Set(subscriptions.map((s) => s.code))).sort();

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
            <h1 className="text-3xl font-bold text-gray-800">🔐 Управление подписками</h1>
            <div className="text-sm text-gray-600">
              Всего: <span className="font-semibold text-blue-600">{total}</span>
            </div>
          </div>

          {/* Filters */}
          <FilterBar
            filters={{
              status: {
                label: 'Статус',
                options: [
                  { value: 'all', label: 'Все статусы' },
                  { value: 'active', label: '✅ Активные' },
                  { value: 'expired', label: '⏰ Истекшие' },
                  { value: 'pending', label: '⏳ Ожидание' },
                ],
                value: statusFilter,
                onChange: (value) => {
                  setStatusFilter(value);
                  setPage(1);
                },
              },
              region: {
                label: 'Регион',
                options: [
                  { value: 'all', label: 'Все регионы' },
                  ...uniqueRegions.map((code) => {
                    const sub = subscriptions.find((s) => s.code === code);
                    return {
                      value: code,
                      label: `${sub?.flag || ''} ${sub?.name || code}`,
                    };
                  }),
                ],
                value: regionFilter,
                onChange: (value) => {
                  setRegionFilter(value);
                  setPage(1);
                },
              },
              sort: {
                label: 'Сортировка',
                options: [
                  { value: 'start_date', label: 'По дате начала' },
                  { value: 'duration', label: 'По длительности' },
                  { value: 'device_count', label: 'По количеству устройств' },
                  { value: 'id', label: 'По ID' },
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
          {subscriptions.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <p className="text-lg">📭 Подписок не найдено</p>
            </div>
          ) : (
            <div className="overflow-x-auto rounded-lg border border-gray-200">
              <table className="w-full">
                <thead className="bg-gradient-to-r from-gray-100 to-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-gray-700 font-semibold">ID</th>
                    <th className="px-4 py-3 text-left text-gray-700 font-semibold">Регион</th>
                    <th className="px-4 py-3 text-left text-gray-700 font-semibold">Длительность</th>
                    <th className="px-4 py-3 text-left text-gray-700 font-semibold">Устройств</th>
                    <th className="px-4 py-3 text-left text-gray-700 font-semibold">Протоколы</th>
                    <th className="px-4 py-3 text-left text-gray-700 font-semibold">Начало</th>
                    <th className="px-4 py-3 text-left text-gray-700 font-semibold">Статус</th>
                  </tr>
                </thead>
                <tbody>
                  {subscriptions.map((sub) => (
                    <tr
                      key={sub.id}
                      className="border-t hover:bg-blue-50 transition-colors cursor-pointer"
                      onClick={() => navigate(`/subscriptions/${sub.id}`)}
                    >
                      <td className="px-4 py-3 text-gray-800 font-mono text-xs">
                        {sub.id.slice(0, 8)}...
                      </td>
                      <td className="px-4 py-3 text-gray-800 font-medium">
                        {sub.flag} {sub.name} ({sub.code})
                      </td>
                      <td className="px-4 py-3 text-gray-800">{sub.duration} дней</td>
                      <td className="px-4 py-3 text-gray-800">{sub.device_count}</td>
                      <td className="px-4 py-3">
                        <div className="flex flex-wrap gap-1">
                          {sub.protocol_types.map((protocol) => (
                            <span
                              key={protocol}
                              className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded font-medium"
                            >
                              {protocol}
                            </span>
                          ))}
                        </div>
                      </td>
                      <td className="px-4 py-3 text-gray-600 text-sm">
                        {formatDate(sub.start_date)}
                      </td>
                      <td className="px-4 py-3">
                        {sub.status && (
                          <span
                            className={`px-3 py-1 rounded-full text-xs font-semibold ${
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
                        )}
                      </td>
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
          <div className="mt-8 pt-6 border-t border-gray-200">
            <h2 className="text-xl font-bold text-gray-800 mb-4">📊 Статистика подписок</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg border border-blue-200">
                <p className="text-gray-600 text-sm mb-1">Всего подписок</p>
                <p className="text-3xl font-bold text-blue-600">{total}</p>
              </div>
              <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg border border-green-200">
                <p className="text-gray-600 text-sm mb-1">Активных</p>
                <p className="text-3xl font-bold text-green-600">
                  {subscriptions.filter((s) => s.status === 'active').length}
                </p>
              </div>
              <div className="bg-gradient-to-br from-red-50 to-red-100 p-4 rounded-lg border border-red-200">
                <p className="text-gray-600 text-sm mb-1">Истекших</p>
                <p className="text-3xl font-bold text-red-600">
                  {subscriptions.filter((s) => s.status === 'expired').length}
                </p>
              </div>
              <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 p-4 rounded-lg border border-yellow-200">
                <p className="text-gray-600 text-sm mb-1">Ожидание</p>
                <p className="text-3xl font-bold text-yellow-600">
                  {subscriptions.filter((s) => s.status === 'pending').length}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
