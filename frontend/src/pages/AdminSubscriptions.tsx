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
  const [userIdFilter, setUserIdFilter] = useState('');
  const [serverIdFilter, setServerIdFilter] = useState('');
  const [protocolTypesFilter, setProtocolTypesFilter] = useState<string[]>([]);
  const [durationRange, setDurationRange] = useState<{ min?: number; max?: number }>({});
  const [deviceCountRange, setDeviceCountRange] = useState<{ min?: number; max?: number }>({});
  const [startDateAfterFilter, setStartDateAfterFilter] = useState<string | undefined>(undefined);
  const [startDateBeforeFilter, setStartDateBeforeFilter] = useState<string | undefined>(undefined);
  const [sortBy, setSortBy] = useState('start_date:desc');

  useEffect(() => {
    if (!isAdmin) {
      navigate('/');
      return;
    }
    loadSubscriptions();
  }, [
    isAdmin,
    page,
    statusFilter,
    regionFilter,
    userIdFilter,
    serverIdFilter,
    protocolTypesFilter,
    durationRange,
    deviceCountRange,
    startDateAfterFilter,
    startDateBeforeFilter,
    sortBy,
  ]);

  const loadSubscriptions = async () => {
    try {
      setIsLoading(true);
      const filters: {
        status?: string;
        region_code?: string;
        user_id?: string;
        server_id?: string;
        protocol_types?: string[];
        min_duration?: number;
        max_duration?: number;
        min_device_count?: number;
        max_device_count?: number;
        start_date_after?: string;
        start_date_before?: string;
      } = {};
      if (statusFilter !== 'all') {
        filters.status = statusFilter;
      }
      if (regionFilter !== 'all') {
        filters.region_code = regionFilter;
      }
      if (userIdFilter.trim()) {
        filters.user_id = userIdFilter.trim();
      }
      if (serverIdFilter.trim()) {
        filters.server_id = serverIdFilter.trim();
      }
      if (protocolTypesFilter.length > 0) {
        filters.protocol_types = protocolTypesFilter;
      }
      if (durationRange.min !== undefined) {
        filters.min_duration = durationRange.min;
      }
      if (durationRange.max !== undefined) {
        filters.max_duration = durationRange.max;
      }
      if (deviceCountRange.min !== undefined) {
        filters.min_device_count = deviceCountRange.min;
      }
      if (deviceCountRange.max !== undefined) {
        filters.max_device_count = deviceCountRange.max;
      }
      if (startDateAfterFilter) {
        filters.start_date_after = startDateAfterFilter;
      }
      if (startDateBeforeFilter) {
        filters.start_date_before = startDateBeforeFilter;
      }
      const data: PaginatedResult<Subscription> = await apiClient.getAllSubscriptions(
        page,
        20,
        filters,
        sortBy
      );
      setSubscriptions(data.items);
      setTotalPages(data.total_pages);
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
    setUserIdFilter('');
    setServerIdFilter('');
    setProtocolTypesFilter([]);
    setDurationRange({});
    setDeviceCountRange({});
    setStartDateAfterFilter(undefined);
    setStartDateBeforeFilter(undefined);
    setSortBy('start_date:desc');
    setPage(1);
  };

  // Получаем уникальные регионы и протоколы
  const uniqueRegions = Array.from(new Set(subscriptions.map((s) => s.code))).sort();
  const allProtocols = Array.from(
    new Set(subscriptions.flatMap((s) => s.protocol_types))
  ).sort();

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
            <h1 className="text-3xl font-bold text-gray-900 leading-tight">🔐 Управление подписками</h1>
            <div className="text-base text-gray-800 font-semibold">
              Всего: <span className="font-bold text-blue-700 text-lg">{total}</span>
            </div>
          </div>

          {/* Filters */}
          <FilterBar
            filters={{
              status: {
                type: 'select',
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
              region_code: {
                type: 'select',
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
              user_id: {
                type: 'text',
                label: 'User ID',
                value: userIdFilter,
                onChange: (value) => {
                  setUserIdFilter(value);
                  setPage(1);
                },
                placeholder: 'UUID пользователя',
              },
              server_id: {
                type: 'text',
                label: 'Server ID',
                value: serverIdFilter,
                onChange: (value) => {
                  setServerIdFilter(value);
                  setPage(1);
                },
                placeholder: 'UUID сервера',
              },
              duration: {
                type: 'range',
                label: 'Длительность (дней)',
                value: durationRange,
                onChange: (value) => {
                  setDurationRange(value);
                  setPage(1);
                },
                min: 1,
                minLabel: 'Мин',
                maxLabel: 'Макс',
              },
              device_count: {
                type: 'range',
                label: 'Количество устройств',
                value: deviceCountRange,
                onChange: (value) => {
                  setDeviceCountRange(value);
                  setPage(1);
                },
                min: 1,
                minLabel: 'Мин',
                maxLabel: 'Макс',
              },
              start_date_after: {
                type: 'date',
                label: 'Начало после',
                value: startDateAfterFilter,
                onChange: (value) => {
                  setStartDateAfterFilter(value);
                  setPage(1);
                },
              },
              start_date_before: {
                type: 'date',
                label: 'Начало до',
                value: startDateBeforeFilter,
                onChange: (value) => {
                  setStartDateBeforeFilter(value);
                  setPage(1);
                },
              },
              sort: {
                type: 'select',
                label: 'Сортировка',
                options: [
                  { value: 'start_date:desc', label: 'По дате начала (новые)' },
                  { value: 'start_date:asc', label: 'По дате начала (старые)' },
                  { value: 'duration:desc', label: 'По длительности (больше)' },
                  { value: 'duration:asc', label: 'По длительности (меньше)' },
                  { value: 'device_count:desc', label: 'По устройствам (больше)' },
                  { value: 'device_count:asc', label: 'По устройствам (меньше)' },
                  { value: 'created_at:desc', label: 'По дате создания (новые)' },
                  { value: 'created_at:asc', label: 'По дате создания (старые)' },
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

          {/* Protocol Types Filter */}
          {allProtocols.length > 0 && (
            <div className="mb-6 bg-white rounded-lg shadow-md p-4 border-2 border-gray-300">
              <label className="block text-sm font-bold text-gray-900 mb-3">
                🔐 Протоколы
              </label>
              <div className="flex flex-wrap gap-2">
                {allProtocols.map((protocol) => (
                  <label
                    key={protocol}
                    className={`flex items-center space-x-2 cursor-pointer px-3 py-2 rounded-lg border-2 transition-all ${
                      protocolTypesFilter.includes(protocol)
                        ? 'border-blue-600 bg-blue-100'
                        : 'border-gray-300 bg-white hover:border-blue-400'
                    }`}
                  >
                    <input
                      type="checkbox"
                      checked={protocolTypesFilter.includes(protocol)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setProtocolTypesFilter([...protocolTypesFilter, protocol]);
                        } else {
                          setProtocolTypesFilter(
                            protocolTypesFilter.filter((p) => p !== protocol)
                          );
                        }
                        setPage(1);
                      }}
                      className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                    />
                    <span className={`font-semibold text-sm ${protocolTypesFilter.includes(protocol) ? 'text-blue-900' : 'text-gray-900'}`}>
                      {protocol}
                    </span>
                  </label>
                ))}
              </div>
            </div>
          )}

          {/* Table */}
          {subscriptions.length === 0 ? (
            <div className="text-center py-12 text-gray-600">
              <p className="text-xl font-semibold">📭 Подписок не найдено</p>
            </div>
          ) : (
            <div className="overflow-x-auto rounded-lg border border-gray-200">
              <table className="w-full">
                <thead className="bg-gray-800">
                  <tr>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">ID</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">Регион</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">Длительность</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">Устройств</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">Протоколы</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">Начало</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">Статус</th>
                  </tr>
                </thead>
                <tbody>
                  {subscriptions.map((sub) => (
                    <tr
                      key={sub.id}
                      className="border-t border-gray-200 bg-white hover:bg-blue-50 transition-colors cursor-pointer"
                      onClick={() => navigate(`/subscriptions/${sub.id}`)}
                    >
                      <td className="px-4 py-4 text-gray-900 font-mono text-sm font-semibold">
                        {sub.id.slice(0, 8)}...
                      </td>
                      <td className="px-4 py-4 text-gray-900 font-semibold text-base">
                        {sub.flag} {sub.name} ({sub.code})
                      </td>
                      <td className="px-4 py-4 text-gray-900 font-semibold text-base">{sub.duration} дней</td>
                      <td className="px-4 py-4 text-gray-900 font-semibold text-base">{sub.device_count}</td>
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
                      <td className="px-4 py-4 text-gray-700 text-base font-medium">
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
              <span className="text-gray-700 font-semibold text-base">
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
            <h2 className="text-2xl font-bold text-gray-900 mb-4 leading-tight">📊 Статистика подписок</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-white border-2 border-blue-400 p-5 rounded-lg shadow-md">
                <p className="text-gray-700 text-sm mb-2 font-semibold">Всего подписок</p>
                <p className="text-4xl font-bold text-blue-700">{total}</p>
              </div>
              <div className="bg-white border-2 border-green-400 p-5 rounded-lg shadow-md">
                <p className="text-gray-700 text-sm mb-2 font-semibold">Активных</p>
                <p className="text-4xl font-bold text-green-700">
                  {subscriptions.filter((s) => s.status === 'active').length}
                </p>
              </div>
              <div className="bg-white border-2 border-red-400 p-5 rounded-lg shadow-md">
                <p className="text-gray-700 text-sm mb-2 font-semibold">Истекших</p>
                <p className="text-4xl font-bold text-red-700">
                  {subscriptions.filter((s) => s.status === 'expired').length}
                </p>
              </div>
              <div className="bg-white border-2 border-yellow-400 p-5 rounded-lg shadow-md">
                <p className="text-gray-700 text-sm mb-2 font-semibold">Ожидание</p>
                <p className="text-4xl font-bold text-yellow-700">
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
