import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useAdmin } from '../contexts/AdminContext';
import { apiClient } from '../services/api';
import { Loading } from '../components/Loading';
import { showTelegramAlert } from '../utils/telegram';
import type { Payment } from '../types';

export const PaymentDetailPage: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const { isAdmin } = useAdmin();
  const [payment, setPayment] = useState<Payment | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!isAdmin) {
      navigate('/');
      return;
    }
    if (id) {
      loadPayment();
    }
  }, [isAdmin, id]);

  const loadPayment = async () => {
    if (!id) return;
    try {
      setIsLoading(true);
      const data = await apiClient.getPayment(id);
      setPayment(data);
    } catch (error: any) {
      console.error('Failed to load payment:', error);
      const errorMessage =
        error.response?.data?.error?.message || 'Ошибка при загрузке платежа';
      showTelegramAlert(errorMessage);
      if (error.response?.status === 404) {
        navigate('/admin/payments');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateString?: string | null) => {
    if (!dateString) return 'Не указано';
    return new Date(dateString).toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('ru-RU', {
      style: 'currency',
      currency: 'RUB',
    }).format(price);
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'succese':
      case 'success':
        return 'bg-green-100 text-green-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'failed':
      case 'canceled':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status.toLowerCase()) {
      case 'succese':
      case 'success':
        return '✅ Успешно';
      case 'pending':
        return '⏳ Ожидание';
      case 'failed':
        return '❌ Ошибка';
      case 'canceled':
        return '🚫 Отменено';
      default:
        return status;
    }
  };

  if (isLoading) {
    return <Loading />;
  }

  if (!payment) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50 p-4">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <p className="text-center text-gray-600">Платеж не найден</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50 p-4">
      <div className="max-w-4xl mx-auto">
        <button
          onClick={() => navigate('/admin/payments')}
          className="mb-4 text-blue-600 hover:text-blue-800 font-semibold flex items-center gap-2"
        >
          <span>←</span> Назад к списку платежей
        </button>

        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                💳 Детали платежа
              </h1>
              <p className="text-gray-600 font-mono text-sm">{payment.id}</p>
            </div>
            <span
              className={`px-4 py-2 rounded-full text-sm font-semibold ${getStatusColor(
                payment.status
              )}`}
            >
              {getStatusLabel(payment.status)}
            </span>
          </div>

          <div className="space-y-6">
            {/* Основная информация о платеже */}
            <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
              <h2 className="text-xl font-bold text-gray-900 mb-4">💰 Платежная информация</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-white rounded-lg p-4 border-2 border-green-400">
                  <p className="text-sm text-gray-600 mb-2 font-semibold">Сумма</p>
                  <p className="text-3xl font-bold text-green-700">{formatPrice(payment.total_price)}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-1">Payment ID</p>
                  <p className="text-lg font-semibold text-gray-900 font-mono">
                    {payment.payment_id || '-'}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-1">Дата платежа</p>
                  <p className="text-lg font-semibold text-gray-900">
                    {formatDate(payment.payment_date)}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-1">Дата создания</p>
                  <p className="text-lg font-semibold text-gray-900">{formatDate(payment.created_at)}</p>
                </div>
              </div>
            </div>

            {/* Информация о подписке */}
            <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold text-gray-900">🔐 Подписка</h2>
                <button
                  onClick={() => navigate(`/subscriptions/${payment.subscription.id}`)}
                  className="text-blue-600 hover:text-blue-800 font-semibold text-sm"
                >
                  Перейти к подписке →
                </button>
              </div>
              <div className="bg-white rounded-lg p-4 border border-gray-300">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-600 mb-1">ID подписки</p>
                    <p className="text-lg font-semibold text-gray-900 font-mono text-sm">
                      {payment.subscription.id}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Регион</p>
                    <p className="text-lg font-semibold text-gray-900">
                      {payment.subscription.flag} {payment.subscription.name} (
                      {payment.subscription.code})
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Длительность</p>
                    <p className="text-lg font-semibold text-gray-900">
                      {payment.subscription.duration} дней
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Количество устройств</p>
                    <p className="text-lg font-semibold text-gray-900">
                      {payment.subscription.device_count}
                    </p>
                  </div>
                  <div className="md:col-span-2">
                    <p className="text-sm text-gray-600 mb-2">Протоколы</p>
                    <div className="flex flex-wrap gap-2">
                      {payment.subscription.protocol_types.map((protocol) => (
                        <span
                          key={protocol}
                          className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded font-medium"
                        >
                          {protocol}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 mb-1">Статус подписки</p>
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-semibold ${
                        payment.subscription.status === 'active'
                          ? 'bg-green-100 text-green-800'
                          : payment.subscription.status === 'expired'
                          ? 'bg-red-100 text-red-800'
                          : 'bg-yellow-100 text-yellow-800'
                      }`}
                    >
                      {payment.subscription.status === 'active'
                        ? '✅ Активна'
                        : payment.subscription.status === 'expired'
                        ? '⏰ Истекла'
                        : '⏳ Ожидание'}
                    </span>
                  </div>
                  {payment.subscription.start_date && (
                    <div>
                      <p className="text-sm text-gray-600 mb-1">Начало подписки</p>
                      <p className="text-lg font-semibold text-gray-900">
                        {formatDate(payment.subscription.start_date)}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Информация о пользователе */}
            <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold text-gray-900">👤 Пользователь</h2>
                <button
                  onClick={() => navigate(`/admin/users/${payment.user_id}`)}
                  className="text-blue-600 hover:text-blue-800 font-semibold text-sm"
                >
                  Перейти к пользователю →
                </button>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">ID пользователя</p>
                <p className="text-lg font-semibold text-gray-900 font-mono">{payment.user_id}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};




