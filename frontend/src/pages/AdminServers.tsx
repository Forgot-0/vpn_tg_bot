import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAdmin } from '../contexts/AdminContext';
import { apiClient } from '../services/api';
import { Loading } from '../components/Loading';
import { showTelegramAlert } from '../utils/telegram';
import type { Server } from '../types';

interface Server {
  id: string;
  ip: string;
  region: string;
  api_type: string;
  panel_port: number;
  status: 'active' | 'inactive';
  created_at: string;
}

export const AdminServers: React.FC = () => {
  const navigate = useNavigate();
  const { isAdmin } = useAdmin();
  const [servers, setServers] = useState<Server[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);

  useEffect(() => {
    if (!isAdmin) {
      navigate('/');
      return;
    }
    loadServers();
  }, [isAdmin]);

  const loadServers = async () => {
    try {
      setIsLoading(true);
      // TODO: Добавить endpoint в backend для получения списка серверов
      // const data = await apiClient.getServers();
      // setServers(data);
      showTelegramAlert('Функция в разработке. Нужен endpoint GET /admin/servers');
    } catch (error) {
      console.error('Failed to load servers:', error);
      showTelegramAlert('Ошибка при загрузке серверов');
    } finally {
      setIsLoading(false);
    }
  };

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
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold text-gray-800">🖥️ Управление серверами</h1>
            <button
              onClick={() => setShowCreateForm(true)}
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
            >
              + Добавить сервер
            </button>
          </div>

          {/* Таблица серверов */}
          {servers.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <p className="text-lg">📭 Серверов не добавлено</p>
              <p className="text-sm">Нажмите кнопку выше, чтобы добавить первый сервер</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-100">
                  <tr>
                    <th className="px-4 py-2 text-left text-gray-700 font-semibold">IP</th>
                    <th className="px-4 py-2 text-left text-gray-700 font-semibold">Регион</th>
                    <th className="px-4 py-2 text-left text-gray-700 font-semibold">Тип API</th>
                    <th className="px-4 py-2 text-left text-gray-700 font-semibold">Порт</th>
                    <th className="px-4 py-2 text-left text-gray-700 font-semibold">Статус</th>
                    <th className="px-4 py-2 text-left text-gray-700 font-semibold">Действия</th>
                  </tr>
                </thead>
                <tbody>
                  {servers.map((server) => (
                    <tr key={server.id} className="border-t hover:bg-gray-50">
                      <td className="px-4 py-2 text-gray-800 font-mono">{server.ip}</td>
                      <td className="px-4 py-2 text-gray-800">{server.region}</td>
                      <td className="px-4 py-2 text-gray-800">{server.api_type}</td>
                      <td className="px-4 py-2 text-gray-800">{server.panel_port}</td>
                      <td className="px-4 py-2">
                        <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                          server.status === 'active'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {server.status === 'active' ? '✅ Активен' : '❌ Неактивен'}
                        </span>
                      </td>
                      <td className="px-4 py-2">
                        <button
                          onClick={() => showTelegramAlert('Функция в разработке')}
                          className="text-blue-600 hover:text-blue-800 font-semibold text-sm mr-3"
                        >
                          Редактировать
                        </button>
                        <button
                          onClick={() => showTelegramAlert('Функция в разработке')}
                          className="text-red-600 hover:text-red-800 font-semibold text-sm"
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

          {/* Статистика */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <h2 className="text-xl font-bold text-gray-800 mb-4">📊 Статистика</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-gray-600 text-sm">Всего серверов</p>
                <p className="text-2xl font-bold text-blue-600">{servers.length}</p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <p className="text-gray-600 text-sm">Активных</p>
                <p className="text-2xl font-bold text-green-600">
                  {servers.filter(s => s.status === 'active').length}
                </p>
              </div>
              <div className="bg-red-50 p-4 rounded-lg">
                <p className="text-gray-600 text-sm">Неактивных</p>
                <p className="text-2xl font-bold text-red-600">
                  {servers.filter(s => s.status === 'inactive').length}
                </p>
              </div>
            </div>
          </div>

          {/* Заглушка для формы создания */}
          {showCreateForm && (
            <div className="mt-8 pt-6 border-t border-gray-200">
              <h2 className="text-xl font-bold text-gray-800 mb-4">➕ Добавить новый сервер</h2>
              <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg">
                <p className="text-yellow-800">
                  ⚠️ Форма создания сервера в разработке.
                </p>
                <p className="text-yellow-700 text-sm mt-2">
                  Требуется реализовать эндпоинт POST /admin/servers на бэкенде
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
