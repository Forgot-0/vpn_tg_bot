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

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'Не указано';
    return new Date(dateString).toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getStatusColor = (status?: string) => {
    if (!status) return 'bg-gray-100 text-gray-800';
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

  // Вычисляем дату истечения на основе start_date и duration
  const calculateExpiresAt = () => {
    if (subscription.start_date && subscription.duration) {
      const startDate = new Date(subscription.start_date);
      const expiresDate = new Date(startDate);
      expiresDate.setDate(expiresDate.getDate() + subscription.duration);
      return expiresDate.toISOString();
    }
    return subscription.expires_at;
  };

  const expiresAt = calculateExpiresAt();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      <div className="max-w-3xl mx-auto p-4">
        {/* Header */}
        <div className="mb-6">
          <button
            onClick={() => navigate('/')}
            className="mb-4 text-blue-600 hover:text-blue-800 font-semibold flex items-center gap-2"
          >
            <span>←</span> Назад к подпискам
          </button>
        </div>

        {/* Main Card */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-4 border-2 border-gray-300">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Детали подписки</h1>
              <p className="text-gray-700 font-medium">Управление VPN подпиской</p>
            </div>
            {subscription.status && (
              <span
                className={`px-4 py-2 rounded-full text-sm font-semibold ${getStatusColor(
                  subscription.status
                )}`}
              >
                {subscription.status === 'active' ? '✅ Активна' : 
                 subscription.status === 'expired' ? '⏰ Истекла' : 
                 subscription.status === 'pending' ? '⏳ Ожидание' : subscription.status}
              </span>
            )}
          </div>

          {/* Info Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white border-2 border-blue-200 rounded-lg p-4 shadow-sm">
              <label className="block text-xs font-semibold text-blue-800 mb-2 uppercase tracking-wide">
                ID подписки
              </label>
              <div className="text-gray-900 font-mono text-sm break-all font-bold">{subscription.id}</div>
            </div>

            <div className="bg-white border-2 border-green-200 rounded-lg p-4 shadow-sm">
              <label className="block text-xs font-semibold text-green-800 mb-2 uppercase tracking-wide">
                Регион
              </label>
              <div className="text-gray-900 font-bold text-base">
                {subscription.flag} {subscription.name} ({subscription.code})
              </div>
            </div>

            <div className="bg-white border-2 border-purple-200 rounded-lg p-4 shadow-sm">
              <label className="block text-xs font-semibold text-purple-800 mb-2 uppercase tracking-wide">
                Длительность
              </label>
              <div className="text-gray-900 font-bold text-xl">{subscription.duration} дней</div>
            </div>

            <div className="bg-white border-2 border-orange-200 rounded-lg p-4 shadow-sm">
              <label className="block text-xs font-semibold text-orange-800 mb-2 uppercase tracking-wide">
                Устройств
              </label>
              <div className="text-gray-900 font-bold text-xl">{subscription.device_count}</div>
            </div>

            <div className="bg-white border-2 border-indigo-200 rounded-lg p-4 md:col-span-2 shadow-sm">
              <label className="block text-xs font-semibold text-indigo-800 mb-2 uppercase tracking-wide">
                Протоколы
              </label>
              <div className="flex flex-wrap gap-2">
                {subscription.protocol_types.map((protocol) => (
                  <span
                    key={protocol}
                    className="px-3 py-1.5 bg-indigo-600 text-white text-sm font-bold rounded-lg shadow-sm"
                  >
                    {protocol}
                  </span>
                ))}
              </div>
            </div>

            {subscription.start_date && (
              <div className="bg-white border-2 border-gray-200 rounded-lg p-4 shadow-sm">
                <label className="block text-xs font-semibold text-gray-700 mb-2 uppercase tracking-wide">
                  Начало подписки
                </label>
                <div className="text-gray-900 font-semibold">{formatDate(subscription.start_date)}</div>
              </div>
            )}

            {expiresAt && (
              <div className="bg-white border-2 border-red-200 rounded-lg p-4 shadow-sm">
                <label className="block text-xs font-semibold text-red-800 mb-2 uppercase tracking-wide">
                  Истекает
                </label>
                <div className="text-gray-900 font-bold text-base">{formatDate(expiresAt)}</div>
              </div>
            )}

            {subscription.created_at && (
              <div className="bg-white border-2 border-gray-200 rounded-lg p-4 md:col-span-2 shadow-sm">
                <label className="block text-xs font-semibold text-gray-700 mb-2 uppercase tracking-wide">
                  Создана
                </label>
                <div className="text-gray-900 font-semibold">{formatDate(subscription.created_at)}</div>
              </div>
            )}
          </div>
        </div>

        {/* VPN Config Card */}
        {showConfig && config && (
          <div className="bg-white rounded-xl shadow-lg p-6 mb-4 border-2 border-gray-300">
            <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <span>🔐</span> Конфигурация VPN
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-bold text-gray-900 mb-2">
                  Протокол: <span className="font-bold text-blue-700">{config.protocol}</span>
                </label>
                <div className="bg-gray-900 rounded-lg p-4 border-2 border-gray-700">
                  <pre className="text-xs text-green-400 whitespace-pre-wrap break-all font-mono">
                    {config.config}
                  </pre>
                </div>
                <button
                  onClick={() => copyToClipboard(config.config)}
                  className="mt-3 w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-semibold py-3 px-4 rounded-lg transition-all shadow-md hover:shadow-lg"
                >
                  📋 Копировать конфигурацию
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="space-y-3">
          {!showConfig && (
            <button
              onClick={fetchConfig}
              disabled={isLoadingConfig}
              className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white font-semibold py-4 px-4 rounded-xl transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center text-lg"
            >
              {isLoadingConfig ? (
                <>
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-3"></div>
                  Загрузка конфигурации...
                </>
              ) : (
                <>
                  <span className="mr-2">🔓</span>
                  Показать конфигурацию VPN
                </>
              )}
            </button>
          )}

          {subscription.status?.toLowerCase() === 'active' && (
            <button
              onClick={handleRenew}
              disabled={isRenewing}
              className="w-full bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-semibold py-4 px-4 rounded-xl transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center text-lg"
            >
              {isRenewing ? (
                <>
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-3"></div>
                  Продление...
                </>
              ) : (
                <>
                  <span className="mr-2">⏰</span>
                  Продлить на 30 дней
                </>
              )}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
