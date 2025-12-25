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
  const [sortBy, setSortBy] = useState('free');

  useEffect(() => {
    if (!isAdmin) {
      navigate('/');
      return;
    }
    loadServers();
  }, [isAdmin, page, regionFilter, apiTypeFilter, sortBy]);

  const loadServers = async () => {
    try {
      setIsLoading(true);
      const filters: { [key: string]: string } = {};
      if (regionFilter !== 'all') {
        filters.region = regionFilter;
      }
      if (apiTypeFilter !== 'all') {
        filters.api_type = apiTypeFilter;
      }
      const data: PaginatedResult<Server> = await apiClient.getServers(page, 20, filters, sortBy);
      setServers(data.items);
      setTotalPages(data.pages);
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
    setSortBy('free');
    setPage(1);
  };

  // Получаем уникальные регионы и типы API
  const uniqueRegions = Array.from(new Set(servers.map((s) => s.region_code))).sort();
  const uniqueApiTypes = Array.from(new Set(servers.map((s) => s.api_type))).sort();

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
            <h1 className="text-3xl font-bold text-gray-800">🖥️ Управление серверами</h1>
            <div className="flex items-center gap-4">
              <div className="text-sm text-gray-600">
                Всего: <span className="font-semibold text-blue-600">{total}</span>
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
              region: {
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
              apiType: {
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
              sort: {
                label: 'Сортировка',
                options: [
                  { value: 'free', label: 'По свободным слотам' },
                  { value: 'limit', label: 'По лимиту' },
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
          {servers.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <p className="text-lg">📭 Серверов не добавлено</p>
              <p className="text-sm mt-2">Нажмите кнопку выше, чтобы добавить первый сервер</p>
            </div>
          ) : (
            <div className="overflow-x-auto rounded-lg border border-gray-200">
              <table className="w-full">
                <thead className="bg-gradient-to-r from-gray-100 to-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-gray-700 font-semibold">ID</th>
                    <th className="px-4 py-3 text-left text-gray-700 font-semibold">Регион</th>
                    <th className="px-4 py-3 text-left text-gray-700 font-semibold">IP</th>
                    <th className="px-4 py-3 text-left text-gray-700 font-semibold">Тип API</th>
                    <th className="px-4 py-3 text-left text-gray-700 font-semibold">Лимит/Свободно</th>
                    <th className="px-4 py-3 text-left text-gray-700 font-semibold">Протоколы</th>
                    <th className="px-4 py-3 text-left text-gray-700 font-semibold">Действия</th>
                  </tr>
                </thead>
                <tbody>
                  {servers.map((server) => (
                    <tr
                      key={server.id}
                      className="border-t hover:bg-blue-50 transition-colors"
                    >
                      <td className="px-4 py-3 text-gray-800 font-mono text-xs">
                        {server.id.slice(0, 8)}...
                      </td>
                      <td className="px-4 py-3 text-gray-800 font-medium">
                        {server.region_flag} {server.region_name} ({server.region_code})
                      </td>
                      <td className="px-4 py-3 text-gray-800 font-mono">{server.ip}</td>
                      <td className="px-4 py-3 text-gray-800">{server.api_type}</td>
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
                        <button
                          onClick={() => handleDelete(server.id)}
                          className="text-red-600 hover:text-red-800 font-semibold text-sm hover:underline"
                        >
                          Удалить
                        </button>
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
            <h2 className="text-xl font-bold text-gray-800 mb-4">📊 Статистика</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg border border-blue-200">
                <p className="text-gray-600 text-sm mb-1">Всего серверов</p>
                <p className="text-3xl font-bold text-blue-600">{total}</p>
              </div>
              <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg border border-green-200">
                <p className="text-gray-600 text-sm mb-1">Свободных слотов</p>
                <p className="text-3xl font-bold text-green-600">
                  {servers.reduce((sum, s) => sum + s.free, 0)}
                </p>
              </div>
              <div className="bg-gradient-to-br from-red-50 to-red-100 p-4 rounded-lg border border-red-200">
                <p className="text-gray-600 text-sm mb-1">Занятых слотов</p>
                <p className="text-3xl font-bold text-red-600">
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
