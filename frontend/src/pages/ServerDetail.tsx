import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useAdmin } from '../contexts/AdminContext';
import { apiClient } from '../services/api';
import { Loading } from '../components/Loading';
import { showTelegramAlert, showTelegramConfirm } from '../utils/telegram';
import type { ServerDetail } from '../types';

export const ServerDetailPage: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const { isAdmin } = useAdmin();
  const [server, setServer] = useState<ServerDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!isAdmin) {
      navigate('/');
      return;
    }
    if (id) {
      loadServer();
    }
  }, [isAdmin, id]);

  const loadServer = async () => {
    if (!id) return;
    try {
      setIsLoading(true);
      const data = await apiClient.getServer(id);
      setServer(data);
    } catch (error: any) {
      console.error('Failed to load server:', error);
      const errorMessage =
        error.response?.data?.error?.message || 'Ошибка при загрузке сервера';
      showTelegramAlert(errorMessage);
      if (error.response?.status === 404) {
        navigate('/admin/servers');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!id) return;
    const confirmed = await showTelegramConfirm(
      'Вы уверены, что хотите удалить этот сервер? Это действие нельзя отменить.'
    );

    if (!confirmed) return;

    try {
      await apiClient.deleteServer(id);
      showTelegramAlert('Сервер успешно удален');
      navigate('/admin/servers');
    } catch (error: any) {
      console.error('Failed to delete server:', error);
      const errorMessage =
        error.response?.data?.error?.message || 'Ошибка при удалении сервера';
      showTelegramAlert(errorMessage);
    }
  };

  const handleReloadConfig = async () => {
    if (!id) return;
    try {
      await apiClient.reloadServerConfig(id);
      showTelegramAlert('Конфигурация сервера успешно перезагружена');
      loadServer();
    } catch (error: any) {
      console.error('Failed to reload server config:', error);
      const errorMessage =
        error.response?.data?.error?.message || 'Ошибка при перезагрузке конфигурации';
      showTelegramAlert(errorMessage);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    showTelegramAlert('Скопировано в буфер обмена');
  };

  if (isLoading) {
    return <Loading />;
  }

  if (!server) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50 p-4">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <p className="text-center text-gray-600">Сервер не найден</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50 p-4">
      <div className="max-w-4xl mx-auto">
        <button
          onClick={() => navigate('/admin/servers')}
          className="mb-4 text-blue-600 hover:text-blue-800 font-semibold flex items-center gap-2"
        >
          <span>←</span> Назад к списку серверов
        </button>

        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                🖥️ Детали сервера
              </h1>
              <p className="text-gray-600 font-mono text-sm">{server.id}</p>
            </div>
            <div className="flex gap-2">
              <button
                onClick={handleReloadConfig}
                className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
              >
                🔄 Перезагрузить конфигурацию
              </button>
              <button
                onClick={handleDelete}
                className="bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
              >
                🗑️ Удалить
              </button>
            </div>
          </div>

          <div className="space-y-6">
            {/* Основная информация */}
            <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
              <h2 className="text-xl font-bold text-gray-900 mb-4">📍 Регион</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Флаг и название</p>
                  <p className="text-lg font-semibold text-gray-900">
                    {server.region_flag} {server.region_name}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-1">Код региона</p>
                  <p className="text-lg font-semibold text-gray-900">{server.region_code}</p>
                </div>
              </div>
            </div>

            {/* Информация о сервере */}
            <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
              <h2 className="text-xl font-bold text-gray-900 mb-4">🔧 Конфигурация</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Тип API</p>
                  <p className="text-lg font-semibold text-gray-900">{server.api_type}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-1">IP адрес</p>
                  <div className="flex items-center gap-2">
                    <p className="text-lg font-semibold text-gray-900 font-mono">{server.ip}</p>
                    <button
                      onClick={() => copyToClipboard(server.ip)}
                      className="text-blue-600 hover:text-blue-800 text-sm"
                    >
                      📋
                    </button>
                  </div>
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-1">Порт панели</p>
                  <p className="text-lg font-semibold text-gray-900">{server.panel_port}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-1">Путь панели</p>
                  <p className="text-lg font-semibold text-gray-900 font-mono">{server.panel_path}</p>
                </div>
                {server.domain && (
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Домен</p>
                    <div className="flex items-center gap-2">
                      <p className="text-lg font-semibold text-gray-900">{server.domain}</p>
                      <button
                        onClick={() => copyToClipboard(server.domain!)}
                        className="text-blue-600 hover:text-blue-800 text-sm"
                      >
                        📋
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Статистика */}
            <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
              <h2 className="text-xl font-bold text-gray-900 mb-4">📊 Статистика</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-white rounded-lg p-4 border-2 border-blue-400">
                  <p className="text-sm text-gray-600 mb-2 font-semibold">Всего слотов</p>
                  <p className="text-3xl font-bold text-blue-700">{server.limit}</p>
                </div>
                <div className="bg-white rounded-lg p-4 border-2 border-green-400">
                  <p className="text-sm text-gray-600 mb-2 font-semibold">Свободных слотов</p>
                  <p className="text-3xl font-bold text-green-700">{server.free}</p>
                </div>
                <div className="bg-white rounded-lg p-4 border-2 border-red-400">
                  <p className="text-sm text-gray-600 mb-2 font-semibold">Занятых слотов</p>
                  <p className="text-3xl font-bold text-red-700">{server.limit - server.free}</p>
                </div>
              </div>
            </div>

            {/* Протоколы */}
            <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
              <h2 className="text-xl font-bold text-gray-900 mb-4">🔐 Протоколы</h2>
              {Object.keys(server.protocol_configs).length === 0 ? (
                <p className="text-gray-600">Протоколы не настроены</p>
              ) : (
                <div className="space-y-4">
                  {Object.entries(server.protocol_configs).map(([protocol, config]) => (
                    <div key={protocol} className="bg-white rounded-lg p-4 border border-gray-300">
                      <h3 className="text-lg font-bold text-gray-900 mb-2">{protocol}</h3>
                      <pre className="bg-gray-100 p-3 rounded text-sm overflow-x-auto">
                        {JSON.stringify(config, null, 2)}
                      </pre>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
