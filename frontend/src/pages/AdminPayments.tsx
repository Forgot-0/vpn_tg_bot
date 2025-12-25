import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAdmin } from '../contexts/AdminContext';

export const AdminPayments: React.FC = () => {
  const navigate = useNavigate();
  const { isAdmin } = useAdmin();

  if (!isAdmin) {
    navigate('/');
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-6xl mx-auto">
        <button
          onClick={() => navigate('/')}
          className="mb-4 text-blue-600 hover:text-blue-800 font-semibold"
        >
          ← Назад
        </button>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h1 className="text-2xl font-bold text-gray-800 mb-6">💳 История платежей</h1>

          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
            <div className="text-4xl mb-4">🚧</div>
            <h2 className="text-xl font-bold text-yellow-800 mb-2">
              Функция в разработке
            </h2>
            <p className="text-yellow-700 mb-4">
              Endpoint для получения списка платежей еще не реализован на бэкенде.
            </p>
            <p className="text-yellow-600 text-sm">
              Платежи обрабатываются через webhook от YooKassa и хранятся в базе данных.
              Для просмотра платежей необходимо добавить соответствующий endpoint в API.
            </p>
          </div>

          <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="font-semibold text-blue-800 mb-2">Рекомендуемый endpoint:</h3>
            <code className="text-sm text-blue-700 bg-blue-100 px-2 py-1 rounded">
              GET /api/v1/payments/ (требует CurrentAdminJWTData)
            </code>
          </div>
        </div>
      </div>
    </div>
  );
};
