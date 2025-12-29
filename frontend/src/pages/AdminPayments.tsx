import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAdmin } from '../contexts/AdminContext';
import { apiClient } from '../services/api';
import { Loading } from '../components/Loading';
import { FilterBar } from '../components/FilterBar';
import { showTelegramAlert } from '../utils/telegram';
import type { Payment, PaginatedResult } from '../types';

export const AdminPayments: React.FC = () => {
  const navigate = useNavigate();
  const { isAdmin } = useAdmin();
  const [payments, setPayments] = useState<Payment[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [total, setTotal] = useState(0);
  const [statusFilter, setStatusFilter] = useState('all');
  const [userIdFilter, setUserIdFilter] = useState('');
  const [subscriptionIdFilter, setSubscriptionIdFilter] = useState('');
  const [priceRange, setPriceRange] = useState<{ min?: number; max?: number }>({});
  const [paymentDateAfterFilter, setPaymentDateAfterFilter] = useState<string | undefined>(undefined);
  const [paymentDateBeforeFilter, setPaymentDateBeforeFilter] = useState<string | undefined>(undefined);
  const [createdAfterFilter, setCreatedAfterFilter] = useState<string | undefined>(undefined);
  const [createdBeforeFilter, setCreatedBeforeFilter] = useState<string | undefined>(undefined);
  const [hasPaymentIdFilter, setHasPaymentIdFilter] = useState<boolean | undefined>(undefined);
  const [sortBy, setSortBy] = useState('created_at:desc');

  useEffect(() => {
    if (!isAdmin) {
      navigate('/');
      return;
    }
    loadPayments();
  }, [
    isAdmin,
    page,
    statusFilter,
    userIdFilter,
    subscriptionIdFilter,
    priceRange,
    paymentDateAfterFilter,
    paymentDateBeforeFilter,
    createdAfterFilter,
    createdBeforeFilter,
    hasPaymentIdFilter,
    sortBy,
  ]);

  const loadPayments = async () => {
    try {
      setIsLoading(true);
      const filters: {
        status?: string;
        user_id?: string;
        subscription_id?: string;
        min_price?: number;
        max_price?: number;
        payment_date_after?: string;
        payment_date_before?: string;
        created_after?: string;
        created_before?: string;
        has_payment_id?: boolean;
      } = {};
      if (statusFilter !== 'all') {
        filters.status = statusFilter;
      }
      if (userIdFilter.trim()) {
        filters.user_id = userIdFilter.trim();
      }
      if (subscriptionIdFilter.trim()) {
        filters.subscription_id = subscriptionIdFilter.trim();
      }
      if (priceRange.min !== undefined) {
        filters.min_price = priceRange.min;
      }
      if (priceRange.max !== undefined) {
        filters.max_price = priceRange.max;
      }
      if (paymentDateAfterFilter) {
        filters.payment_date_after = paymentDateAfterFilter;
      }
      if (paymentDateBeforeFilter) {
        filters.payment_date_before = paymentDateBeforeFilter;
      }
      if (createdAfterFilter) {
        filters.created_after = createdAfterFilter;
      }
      if (createdBeforeFilter) {
        filters.created_before = createdBeforeFilter;
      }
      if (hasPaymentIdFilter !== undefined) {
        filters.has_payment_id = hasPaymentIdFilter;
      }
      const data: PaginatedResult<Payment> = await apiClient.getPayments(
        page,
        20,
        filters,
        sortBy
      );
      setPayments(data.items);
      setTotalPages(data.total_pages);
      setTotal(data.total);
    } catch (error: any) {
      console.error('Failed to load payments:', error);
      const errorMessage =
        error.response?.data?.error?.message ||
        'Ошибка при загрузке платежей. Убедитесь, что у вас есть права администратора.';
      showTelegramAlert(errorMessage);
      if (error.response?.status === 403 || error.response?.status === 401) {
        navigate('/');
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

  const resetFilters = () => {
    setStatusFilter('all');
    setUserIdFilter('');
    setSubscriptionIdFilter('');
    setPriceRange({});
    setPaymentDateAfterFilter(undefined);
    setPaymentDateBeforeFilter(undefined);
    setCreatedAfterFilter(undefined);
    setCreatedBeforeFilter(undefined);
    setHasPaymentIdFilter(undefined);
    setSortBy('created_at:desc');
    setPage(1);
  };

  if (isLoading) {
    return <Loading />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50 p-4">
      <div className="max-w-7xl mx-auto">
        <button
          onClick={() => navigate('/')}
          className="mb-4 text-blue-600 hover:text-blue-800 font-semibold text-lg flex items-center gap-2 transition-colors"
        >
          <span>←</span> Назад
        </button>

        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-3xl font-bold text-gray-900">💳 История платежей</h1>
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
                  { value: 'succese', label: '✅ Успешно' },
                  { value: 'success', label: '✅ Успешно' },
                  { value: 'pending', label: '⏳ Ожидание' },
                  { value: 'failed', label: '❌ Ошибка' },
                  { value: 'canceled', label: '🚫 Отменено' },
                ],
                value: statusFilter,
                onChange: (value) => {
                  setStatusFilter(value);
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
              subscription_id: {
                type: 'text',
                label: 'Subscription ID',
                value: subscriptionIdFilter,
                onChange: (value) => {
                  setSubscriptionIdFilter(value);
                  setPage(1);
                },
                placeholder: 'UUID подписки',
              },
              price: {
                type: 'range',
                label: 'Сумма (₽)',
                value: priceRange,
                onChange: (value) => {
                  setPriceRange(value);
                  setPage(1);
                },
                min: 0,
                step: 0.01,
                minLabel: 'Мин',
                maxLabel: 'Макс',
              },
              payment_date_after: {
                type: 'date',
                label: 'Дата платежа после',
                value: paymentDateAfterFilter,
                onChange: (value) => {
                  setPaymentDateAfterFilter(value);
                  setPage(1);
                },
              },
              payment_date_before: {
                type: 'date',
                label: 'Дата платежа до',
                value: paymentDateBeforeFilter,
                onChange: (value) => {
                  setPaymentDateBeforeFilter(value);
                  setPage(1);
                },
              },
              created_after: {
                type: 'date',
                label: 'Создан после',
                value: createdAfterFilter,
                onChange: (value) => {
                  setCreatedAfterFilter(value);
                  setPage(1);
                },
              },
              created_before: {
                type: 'date',
                label: 'Создан до',
                value: createdBeforeFilter,
                onChange: (value) => {
                  setCreatedBeforeFilter(value);
                  setPage(1);
                },
              },
              has_payment_id: {
                type: 'checkbox',
                label: 'С Payment ID',
                value: hasPaymentIdFilter,
                onChange: (value) => {
                  setHasPaymentIdFilter(value);
                  setPage(1);
                },
              },
              sort: {
                type: 'select',
                label: 'Сортировка',
                options: [
                  { value: 'created_at:desc', label: 'По дате создания (новые)' },
                  { value: 'created_at:asc', label: 'По дате создания (старые)' },
                  { value: 'total_price:desc', label: 'По сумме (больше)' },
                  { value: 'total_price:asc', label: 'По сумме (меньше)' },
                  { value: 'payment_date:desc', label: 'По дате платежа (новые)' },
                  { value: 'payment_date:asc', label: 'По дате платежа (старые)' },
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
          {payments.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <div className="text-6xl mb-4">💳</div>
              <p className="text-xl font-semibold mb-2">Платежей не найдено</p>
              <p className="text-base">Платежи появятся здесь после оплаты подписок</p>
            </div>
          ) : (
            <div className="overflow-x-auto rounded-lg border border-gray-200">
              <table className="w-full">
                <thead className="bg-gray-800">
                  <tr>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">ID</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">Подписка</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">Сумма</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">Статус</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">Payment ID</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">Дата платежа</th>
                    <th className="px-4 py-4 text-left text-white font-bold text-base">Создан</th>
                  </tr>
                </thead>
                <tbody>
                  {payments.map((payment) => (
                    <tr
                      key={payment.id}
                      className="border-t border-gray-200 bg-white hover:bg-blue-50 transition-colors"
                    >
                      <td className="px-4 py-4 text-gray-900 font-mono text-sm font-semibold">
                        {payment.id.slice(0, 8)}...
                      </td>
                      <td className="px-4 py-4">
                        <div className="flex flex-col">
                          <span className="text-gray-900 font-semibold text-base">
                            {payment.subscription.flag} {payment.subscription.name}
                          </span>
                          <span className="text-gray-600 text-sm font-medium">
                            {payment.subscription.duration} дней, {payment.subscription.device_count} устройств
                          </span>
                        </div>
                      </td>
                      <td className="px-4 py-4">
                        <span className="text-gray-900 font-bold text-lg text-green-700">
                          {formatPrice(payment.total_price)}
                        </span>
                      </td>
                      <td className="px-4 py-4">
                        <span
                          className={`px-3 py-1.5 rounded-full text-sm font-semibold ${getStatusColor(
                            payment.status
                          )}`}
                        >
                          {getStatusLabel(payment.status)}
                        </span>
                      </td>
                      <td className="px-4 py-4">
                        <span className="text-gray-900 font-mono text-sm font-medium">
                          {payment.payment_id || '-'}
                        </span>
                      </td>
                      <td className="px-4 py-4 text-gray-700 text-sm font-medium">
                        {formatDate(payment.payment_date)}
                      </td>
                      <td className="px-4 py-4 text-gray-700 text-sm font-medium">
                        {formatDate(payment.created_at)}
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
                className="px-5 py-2.5 bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-base"
              >
                ← Назад
              </button>
              <span className="text-gray-700 font-semibold text-base">
                Страница {page} из {totalPages} (всего: {total})
              </span>
              <button
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                className="px-5 py-2.5 bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-base"
              >
                Вперед →
              </button>
            </div>
          )}

          {/* Statistics */}
          <div className="mt-8 pt-6 border-t-2 border-gray-300">
            <h2 className="text-xl font-bold text-gray-900 mb-4">📊 Статистика платежей</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-white border-2 border-blue-400 p-5 rounded-lg shadow-md">
                <p className="text-gray-700 text-sm mb-2 font-semibold">Всего платежей</p>
                <p className="text-4xl font-bold text-blue-700">{total}</p>
              </div>
              <div className="bg-white border-2 border-green-400 p-5 rounded-lg shadow-md">
                <p className="text-gray-700 text-sm mb-2 font-semibold">Успешных</p>
                <p className="text-4xl font-bold text-green-700">
                  {payments.filter((p) => p.status.toLowerCase() === 'succese' || p.status.toLowerCase() === 'success').length}
                </p>
              </div>
              <div className="bg-white border-2 border-yellow-400 p-5 rounded-lg shadow-md">
                <p className="text-gray-700 text-sm mb-2 font-semibold">Ожидание</p>
                <p className="text-4xl font-bold text-yellow-700">
                  {payments.filter((p) => p.status.toLowerCase() === 'pending').length}
                </p>
              </div>
              <div className="bg-white border-2 border-red-400 p-5 rounded-lg shadow-md">
                <p className="text-gray-700 text-sm mb-2 font-semibold">Общая сумма</p>
                <p className="text-2xl font-bold text-red-700">
                  {formatPrice(payments.reduce((sum, p) => sum + p.total_price, 0))}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
