import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { apiClient } from '../services/api';
import { showTelegramAlert, showTelegramConfirm } from '../utils/telegram';
import { Loading } from '../components/Loading';
import type { Subscription, VPNConfig } from '../types';

export const SubscriptionDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [subscription, setSubscription] = useState<Subscription | null>(null);
  const [config, setConfig] = useState<VPNConfig | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isLoadingConfig, setIsLoadingConfig] = useState(false);
  const [isRenewing, setIsRenewing] = useState(false);
  const [showConfig, setShowConfig] = useState(false);

  useEffect(() => {
    const fetchSubscription = async () => {
      if (!id) return;

      try {
        const data = await apiClient.getSubscription(id);
        setSubscription(data);
      } catch (error) {
        console.error('Failed to fetch subscription:', error);
        showTelegramAlert('Не удалось загрузить подписку');
        navigate('/');
      } finally {
        setIsLoading(false);
      }
    };

    fetchSubscription();
  }, [id, navigate]);

  const fetchConfig = async () => {
    if (!id) return;

    try {
      setIsLoadingConfig(true);
      const configData = await apiClient.getSubscriptionConfig(id);
      setConfig(configData);
      setShowConfig(true);
    } catch (error) {
      console.error('Failed to fetch config:', error);
      showTelegramAlert('Не удалось загрузить конфигурацию');
    } finally {
      setIsLoadingConfig(false);
    }
  };

  const handleRenew = async () => {
    if (!id) return;

    const confirmed = await showTelegramConfirm(
      'Вы уверены, что хотите продлить подписку на 30 дней?'
    );

    if (!confirmed) return;

    try {
      setIsRenewing(true);
      const paymentUrl = await apiClient.renewSubscription(id, { duration_days: 30 });
      window.location.href = paymentUrl;
    } catch (error) {
      console.error('Failed to renew subscription:', error);
      showTelegramAlert('Ошибка при продлении подписки');
    } finally {
      setIsRenewing(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text).then(() => {
      showTelegramAlert('Скопировано в буфер обмена');
    });
  };

  if (isLoading) {
    return <Loading />;
  }

  if (!subscription) {
    return null;
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active':
        return 'bg-green-100 text-green-800';
      case 'expired':
        return 'bg-red-100 text-red-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-2xl mx-auto p-4">
        <div className="bg-white rounded-lg shadow-md p-6 mb-4">
          <div className="flex justify-between items-start mb-4">
            <h1 className="text-2xl font-bold text-gray-800">Подписка</h1>
            <span
              className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(
                subscription.status
              )}`}
            >
              {subscription.status}
            </span>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                ID подписки
              </label>
              <div className="text-gray-900 font-mono text-sm">{subscription.id}</div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Длительность
              </label>
              <div className="text-gray-900">{subscription.duration_days} дней</div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Количество устройств
              </label>
              <div className="text-gray-900">{subscription.device_count}</div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Протоколы
              </label>
              <div className="text-gray-900">{subscription.protocol_types.join(', ')}</div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Истекает
              </label>
              <div className="text-gray-900">{formatDate(subscription.expires_at)}</div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Создана
              </label>
              <div className="text-gray-900">{formatDate(subscription.created_at)}</div>
            </div>
          </div>
        </div>

        {showConfig && config && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-4">
            <h2 className="text-xl font-bold text-gray-800 mb-4">Конфигурация VPN</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Протокол: {config.protocol}
                </label>
                <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                  <pre className="text-xs text-gray-800 whitespace-pre-wrap break-all">
                    {config.config}
                  </pre>
                </div>
                <button
                  onClick={() => copyToClipboard(config.config)}
                  className="mt-2 w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
                >
                  Копировать конфигурацию
                </button>
              </div>
            </div>
          </div>
        )}

        <div className="space-y-3">
          {!showConfig && (
            <button
              onClick={fetchConfig}
              disabled={isLoadingConfig}
              className="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3 px-4 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {isLoadingConfig ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Загрузка...
                </>
              ) : (
                'Показать конфигурацию'
              )}
            </button>
          )}

          {subscription.status.toLowerCase() === 'active' && (
            <button
              onClick={handleRenew}
              disabled={isRenewing}
              className="w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-3 px-4 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {isRenewing ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Продление...
                </>
              ) : (
                'Продлить на 30 дней'
              )}
            </button>
          )}

          <button
            onClick={() => navigate('/')}
            className="w-full bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-3 px-4 rounded-lg transition-colors"
          >
            Назад
          </button>
        </div>
      </div>
    </div>
  );
};

