import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAdmin } from '../contexts/AdminContext';
import { Loading } from '../components/Loading';
import { showTelegramAlert } from '../utils/telegram';

interface Payment {
  id: string;
  user_id: string;
  amount: number;
  status: 'pending' | 'confirmed' | 'failed';
  payment_id: string;
  created_at: string;
}

export const AdminPayments: React.FC = () => {
  const navigate = useNavigate();
  const { isAdmin } = useAdmin();
  const [payments, setPayments] = useState<Payment[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState<string>('all');

  useEffect(() => {
    if (!isAdmin) {
      navigate('/');
      return;
    }
    loadPayments();
  }, [isAdmin]);

  const loadPayments = async () => {
    try {
      setIsLoading(true);
      // TODO: Добавить endpoint в backend для получения списка платежей
      showTelegramAlert('Функция в разработке. Нужен endpoint GET /admin/payments');
    } catch (error) {
      console.error('Failed to load payments:', error);
      showTelegramAlert('Ошибка при загрузке платежей');
    } finally {
      setIsLoading(false);
    }
  };

  const filteredPayments = payments.filter(payment =>
    filterStatus === 'all' || payment.status === filterStatus
  );

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
          <h1 className="text-3xl font-bold text-gray-800 mb-6">💳 История платежей</h1>

          {/* Фильтры */}
          <div className="mb-6 flex gap-2 flex-wrap">
            {['all', 'pending', 'confirmed', 'failed'].map((status) => (
              <button
                key={status}
                onClick={() => setFilterStatus(status)}
                className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
                  filterStatus === status
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {status === 'all' ? 'Все' : status === 'pending' ? '⏳ Ожидание' : status === 'confirmed' ? '✅ Подтверждены' : '❌ Ошибки'}
              </button>
            ))}
          </div>

          {/* Таблица платежей */}
          {filteredPayments.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <p className="text-lg">📭 Платежей не найдено</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-100">
                  <tr>
                    <th className="px-4 py-2 text-left text-gray-700 font-semibold">ID платежа</th>
                    <th className="px-4 py-2 text-left text-gray-700 font-semibold">ID пользователя</th>
                    <th className="px-4 py-2 text-left text-gray-700 font-semibold">Сумма</th>
                    <th className="px-4 py-2 text-left text-gray-700 font-semibold">Статус</th>
                    <th className="px-4 py-2 text-left text-gray-700 font-semibold">Дата</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredPayments.map((payment) => (
                    <tr key={payment.id} className="border-t hover:bg-gray-50">
                      <td className="px-4 py-2 text-gray-800 font-mono text-sm">{payment.payment_id}</td>
                      <td className="px-4 py-2 text-gray-800">{payment.user_id}</td>
                      <td className="px-4 py-2 text-gray-800 font-semibold">${payment.amount.toFixed(2)}</td>
                      <td className="px-4 py-2">
                        <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                          payment.status === 'confirmed'
                            ? 'bg-green-100 text-green-800'
                            : payment.status === 'pending'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {payment.status === 'confirmed' ? '✅ Подтверждён' : payment.status === 'pending' ? '⏳ Ожидание' : '❌ Ошибка'}
                        </span>
                      </td>
                      <td className="px-4 py-2 text-gray-600 text-sm">{new Date(payment.created_at).toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Статистика */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <h2 className="text-xl font-bold text-gray-800 mb-4">📊 Статистика платежей</h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-gray-600 text-sm">Всего платежей</p>
                <p className="text-2xl font-bold text-blue-600">{filteredPayments.length}</p>
              </div>
              <div className="bg-yellow-50 p-4 rounded-lg">
                <p className="text-gray-600 text-sm">На рассмотрении</p>
                <p className="text-2xl font-bold text-yellow-600">
                  {filteredPayments.filter(p => p.status === 'pending').length}
                </p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <p className="text-gray-600 text-sm">Успешных</p>
                <p className="text-2xl font-bold text-green-600">
                  {filteredPayments.filter(p => p.status === 'confirmed').length}
                </p>
              </div>
              <div className="bg-red-50 p-4 rounded-lg">
                <p className="text-gray-600 text-sm">Ошибок</p>
                <p className="text-2xl font-bold text-red-600">
                  {filteredPayments.filter(p => p.status === 'failed').length}
                </p>
              </div>
            </div>
            
            <div className="mt-4 bg-purple-50 p-4 rounded-lg">
              <p className="text-gray-600 text-sm">Общая сумма</p>
              <p className="text-3xl font-bold text-purple-600">
                ${filteredPayments.reduce((sum, p) => sum + p.amount, 0).toFixed(2)}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
