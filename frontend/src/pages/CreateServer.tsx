import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiClient } from '../services/api';
import { showTelegramAlert } from '../utils/telegram';
import type { ApiType, CreateServerRequest } from '../types';

const API_TYPES: ApiType[] = ['3X-UI'];

export const CreateServer: React.FC = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [apiType, setApiType] = useState<ApiType>('3X-UI');

  const [formData, setFormData] = useState<CreateServerRequest>({
    limit: 100,
    region_code: 'NL',
    ip: '',
    panel_port: 2053,
    panel_path: '',
    domain: null,
    username: '',
    password: '',
    twoFactorCode: null,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Валидация обязательных полей
    if (!formData.ip || !formData.panel_path || !formData.username || !formData.password) {
      showTelegramAlert('Заполните все обязательные поля');
      return;
    }

    if (formData.panel_port < 1 || formData.panel_port > 65535) {
      showTelegramAlert('Порт должен быть в диапазоне 1-65535');
      return;
    }

    if (formData.limit < 1) {
      showTelegramAlert('Лимит должен быть больше 0');
      return;
    }

    try {
      setIsLoading(true);
      await apiClient.createServer(apiType, formData);
      showTelegramAlert('Сервер успешно создан!');
      navigate('/');
    } catch (error: any) {
      console.error('Failed to create server:', error);
      const errorMessage =
        error.response?.data?.error?.message ||
        error.response?.data?.detail ||
        'Ошибка при создании сервера. Проверьте правильность данных.';
      showTelegramAlert(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => {
      if (name === 'twoFactorCode') {
        return {
          ...prev,
          [name]: value === '' ? null : value,
        };
      }
      if (name === 'domain') {
        return {
          ...prev,
          [name]: value === '' ? null : value,
        };
      }
      return {
        ...prev,
        [name]: name === 'panel_port' || name === 'limit' ? Number(value) : value,
      };
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50">
      <div className="max-w-3xl mx-auto p-4">
        <button
          onClick={() => navigate('/')}
          className="mb-4 text-blue-600 hover:text-blue-800 font-semibold flex items-center gap-2"
        >
          <span>←</span> Назад
        </button>

        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
          <h1 className="text-3xl font-bold text-gray-800 mb-6">🖥️ Добавить сервер</h1>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Тип API *
              </label>
              <select
                name="api_type"
                value={apiType}
                onChange={(e) => setApiType(e.target.value as ApiType)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                required
              >
                {API_TYPES.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Лимит подключений *
              </label>
              <input
                type="number"
                name="limit"
                value={formData.limit}
                onChange={handleChange}
                min="1"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Код региона *
              </label>
              <input
                type="text"
                name="region_code"
                value={formData.region_code}
                onChange={handleChange}
                placeholder="NL"
                maxLength={10}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                required
              />
              <p className="text-xs text-gray-500 mt-1">
                Например: NL, US, RU и т.д.
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                IP адрес *
              </label>
              <input
                type="text"
                name="ip"
                value={formData.ip}
                onChange={handleChange}
                placeholder="192.168.1.1"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Порт панели *
              </label>
              <input
                type="number"
                name="panel_port"
                value={formData.panel_port}
                onChange={handleChange}
                min="1"
                max="65535"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Путь панели *
              </label>
              <input
                type="text"
                name="panel_path"
                value={formData.panel_path}
                onChange={handleChange}
                placeholder="panel"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                required
              />
              <p className="text-xs text-gray-500 mt-1">
                Путь к панели управления (например: panel, xui, admin)
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Домен (опционально)
              </label>
              <input
                type="text"
                name="domain"
                value={formData.domain || ''}
                onChange={handleChange}
                placeholder="example.com"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
              <p className="text-xs text-gray-500 mt-1">
                Если указан, будет использоваться HTTPS
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Имя пользователя *
              </label>
              <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleChange}
                placeholder="admin"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Пароль *
              </label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="••••••••"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Двухфакторная аутентификация (опционально)
              </label>
              <input
                type="text"
                name="twoFactorCode"
                value={formData.twoFactorCode || ''}
                onChange={handleChange}
                placeholder="000000"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
              <p className="text-xs text-gray-500 mt-1">
                Код из приложения аутентификатора (если требуется)
              </p>
            </div>

            <div className="flex gap-4 pt-4">
              <button
                type="button"
                onClick={() => navigate('/')}
                className="flex-1 bg-white hover:bg-gray-50 text-gray-800 font-semibold py-3 px-4 rounded-lg transition-all shadow-md hover:shadow-lg border border-gray-200"
              >
                Отмена
              </button>
              <button
                type="submit"
                disabled={isLoading}
                className="flex-1 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-semibold py-3 px-4 rounded-lg transition-all shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
              >
                {isLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Создание...
                  </>
                ) : (
                  <>
                    <span className="mr-2">✨</span>
                    Создать сервер
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

