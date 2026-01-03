import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAdmin } from '../contexts/AdminContext';
import { apiClient } from '../services/api';
import { Loading } from '../components/Loading';
import { FilterBar } from '../components/FilterBar';
import { showTelegramAlert, showTelegramConfirm } from '../utils/telegram';
import type { Server, PaginatedResult } from '../types';

export const AdminServers: React.FC = () => {
  const navigate = useNavigate();
  const { isAdmin } = useAdmin();
  const [servers, setServers] = useState<Server[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [total, setTotal] = useState(0);
  const [regionFilter, setRegionFilter] = useState('all');
  const [apiTypeFilter, setApiTypeFilter] = useState('all');
  const [freeSlotsRange, setFreeSlotsRange] = useState<{ min?: number; max?: number }>({});
  const [hasDomainFilter, setHasDomainFilter] = useState<boolean | undefined>(undefined);
  const [protocolTypesFilter, setProtocolTypesFilter] = useState<string[]>([]);
  const [sortBy, setSortBy] = useState('free:desc');

  useEffect(() => {
    if (!isAdmin) {
      navigate('/');
      return;
    }
    loadServers();
  }, [isAdmin, page, regionFilter, apiTypeFilter, freeSlotsRange, hasDomainFilter, protocolTypesFilter, sortBy]);

  const loadServers = async () => {
    try {
      setIsLoading(true);
      const filters: {
        region_code?: string;
        api_type?: string;
        min_free_slots?: number;
        max_free_slots?: number;
        protocol_types?: string[];
        has_domain?: boolean;
      } = {};
      if (regionFilter !== 'all') {
        filters.region_code = regionFilter;
      }
      if (apiTypeFilter !== 'all') {
        filters.api_type = apiTypeFilter;
      }
      if (freeSlotsRange.min !== undefined) {
        filters.min_free_slots = freeSlotsRange.min;
      }
      if (freeSlotsRange.max !== undefined) {
        filters.max_free_slots = freeSlotsRange.max;
      }
      if (protocolTypesFilter.length > 0) {
        filters.protocol_types = protocolTypesFilter;
      }
      if (hasDomainFilter !== undefined) {
        filters.has_domain = hasDomainFilter;
      }
      const data: PaginatedResult<Server> = await apiClient.getServers(page, 20, filters, sortBy);
      setServers(data.items);
      setTotalPages(data.total_pages);
      setTotal(data.total);
    } catch (error: any) {
      console.error('Failed to load servers:', error);
      const errorMessage =
        error.response?.data?.error?.message ||
        'Ошибка при загрузке серверов. Убедитесь, что у вас есть права администратора.';
      showTelegramAlert(errorMessage);
      if (error.response?.status === 403 || error.response?.status === 401) {
        navigate('/');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (serverId: string) => {
    const confirmed = await showTelegramConfirm(
      'Вы уверены, что хотите удалить этот сервер? Это действие нельзя отменить.'
    );

    if (!confirmed) return;

    try {
      await apiClient.deleteServer(serverId);
      showTelegramAlert('Сервер успешно удален');
      loadServers();
    } catch (error: any) {
      console.error('Failed to delete server:', error);
      const errorMessage =
        error.response?.data?.error?.message || 'Ошибка при удалении сервера';
      showTelegramAlert(errorMessage);
    }
  };

  const resetFilters = () => {
    setRegionFilter('all');
    setApiTypeFilter('all');
    setFreeSlotsRange({});
    setHasDomainFilter(undefined);
    setProtocolTypesFilter([]);
    setSortBy('free:desc');
    setPage(1);
  };

  // Получаем уникальные регионы, типы API и протоколы
  const uniqueRegions = Array.from(new Set(servers.map((s) => s.region_code))).sort();
  const uniqueApiTypes = Array.from(new Set(servers.map((s) => s.api_type))).sort();
  const allProtocols = Array.from(
    new Set(servers.flatMap((s) => s.protocol_configs))
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
            <h1 className="text-3xl font-bold text-gray-900 leading-tight">🖥️ Управление серверами</h1>
            <div className="flex items-center gap-4">
              <div className="text-base text-gray-800 font-semibold">
                Всего: <span className="font-bold text-blue-700 text-lg">{total}</span>
              </div>
              <button
                onClick={() => navigate('/servers/create')}
                className="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-all shadow-md hover:shadow-lg"
              >
                + Добавить сервер
              </button>
            </div>
          </div>

          {/* Filters */}
          <FilterBar
            filters={{
              region_code: {
                type: 'select',
                label: 'Регион',
                options: [
                  { value: 'all', label: 'Все регионы' },
                  ...uniqueRegions.map((r) => {
                    const server = servers.find((s) => s.region_code === r);
                    return {
                      value: r,
                      label: `${server?.region_flag || ''} ${server?.region_name || r}`,
                    };
                  }),
                ],
                value: regionFilter,
                onChange: (value) => {
                  setRegionFilter(value);
                  setPage(1);
                },
              },
              api_type: {
                type: 'select',
                label: 'Тип API',
                options: [
                  { value: 'all', label: 'Все типы' },
                  ...uniqueApiTypes.map((type) => ({ value: type, label: type })),
                ],
                value: apiTypeFilter,
                onChange: (value) => {
                  setApiTypeFilter(value);
                  setPage(1);
                },
              },
              free_slots: {
                type: 'range',
                label: 'Свободные слоты',
                value: freeSlotsRange,
                onChange: (value) => {
                  setFreeSlotsRange(value);
                  setPage(1);
                },
                min: 0,
                minLabel: 'Мин',
                maxLabel: 'Макс',
              },
              has_domain: {
                type: 'checkbox',
                label: 'С доменом',
                value: hasDomainFilter,
                onChange: (value) => {
                  setHasDomainFilter(value);
                  setPage(1);
                },
              },
              sort: {
                type: 'select',
                label: 'Сортировка',
                options: [
                  { value: 'free:desc', label: 'По свободным слотам (больше)' },
                  { value: 'free:asc', label: 'По свободным слотам (меньше)' },
                  { value: 'limit:desc', label: 'По лимиту (больше)' },
                  { value: 'limit:asc', label: 'По лимиту (меньше)' },
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
          {servers.length === 0 ? (
            <div className="text-center py-12 text-gray-600">
              <p className="text-xl font-semibold mb-2">📭 Серверов не добавлено</p>
              <p className="text-base mt-2 font-medium">Нажмите кнопку выше, чтобы добавить первый сервер</p>
            </div>
          ) : (
            <div className="overflow-x-auto rounded-lg border border-gray-200">
              <table className="w-full">
                <thead className="bg-gray-800">
                  <tr>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">ID</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">Регион</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">IP</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">Тип API</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">Лимит/Свободно</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">Протоколы</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">Действия</th>
                  </tr>
                </thead>
                <tbody>
                  {servers.map((server) => (
                    <tr
                      key={server.id}
                      className="border-t border-gray-200 bg-white hover:bg-blue-50 transition-colors cursor-pointer"
                      onClick={() => navigate(`/admin/servers/${server.id}`)}
                    >
                      <td className="px-4 py-4 text-gray-900 font-mono text-sm font-semibold">
                        {server.id.slice(0, 8)}...
                      </td>
                      <td className="px-4 py-4 text-gray-900 font-semibold text-base">
                        {server.region_flag} {server.region_name} ({server.region_code})
                      </td>
                      <td className="px-4 py-4 text-gray-900 font-mono font-semibold text-base">{server.ip}</td>
                      <td className="px-4 py-4 text-gray-900 font-semibold text-base">{server.api_type}</td>
                      <td className="px-4 py-3">
                        <span
                          className={`font-semibold ${
                            server.free === 0
                              ? 'text-red-600'
                              : server.free < server.limit / 2
                              ? 'text-yellow-600'
                              : 'text-green-600'
                          }`}
                        >
                          {server.free}/{server.limit}
                        </span>
                      </td>
                      <td className="px-4 py-3">
                        <div className="flex flex-wrap gap-1">
                          {server.protocol_configs.map((protocol) => (
                            <span
                              key={protocol}
                              className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded font-medium"
                            >
                              {protocol}
                            </span>
                          ))}
                        </div>
                      </td>
                      <td className="px-4 py-3">
                        <div className="flex gap-2">
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              navigate(`/admin/servers/${server.id}`);
                            }}
                            className="text-blue-600 hover:text-blue-800 font-semibold text-sm hover:underline"
                          >
                            Просмотр
                          </button>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleDelete(server.id);
                            }}
                            className="text-red-600 hover:text-red-800 font-semibold text-sm hover:underline"
                          >
                            Удалить
                          </button>
                        </div>
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
            <h2 className="text-2xl font-bold text-gray-900 mb-4 leading-tight">📊 Статистика</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-white border-2 border-blue-400 p-5 rounded-lg shadow-md">
                <p className="text-gray-700 text-sm mb-2 font-semibold">Всего серверов</p>
                <p className="text-4xl font-bold text-blue-700">{total}</p>
              </div>
              <div className="bg-white border-2 border-green-400 p-5 rounded-lg shadow-md">
                <p className="text-gray-700 text-sm mb-2 font-semibold">Свободных слотов</p>
                <p className="text-4xl font-bold text-green-700">
                  {servers.reduce((sum, s) => sum + s.free, 0)}
                </p>
              </div>
              <div className="bg-white border-2 border-red-400 p-5 rounded-lg shadow-md">
                <p className="text-gray-700 text-sm mb-2 font-semibold">Занятых слотов</p>
                <p className="text-4xl font-bold text-red-700">
                  {servers.reduce((sum, s) => sum + (s.limit - s.free), 0)}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
