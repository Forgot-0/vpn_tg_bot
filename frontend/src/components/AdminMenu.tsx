import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAdmin } from '../contexts/AdminContext';

export const AdminMenu: React.FC = () => {
  const navigate = useNavigate();
  const { isAdmin } = useAdmin();

  if (!isAdmin) {
    return null;
  }

  return (
    <div className="admin-menu bg-gradient-to-r from-red-600 to-red-700 text-white p-4 rounded-lg shadow-lg mb-4">
      <h2 className="text-2xl font-bold mb-4">⚙️ Админ Панель</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <button
          onClick={() => navigate('/admin/users')}
          className="bg-red-500 hover:bg-red-600 text-white font-semibold py-3 px-4 rounded-lg transition-colors flex items-center justify-center"
        >
          👥 Пользователи
        </button>

        <button
          onClick={() => navigate('/admin/servers')}
          className="bg-red-500 hover:bg-red-600 text-white font-semibold py-3 px-4 rounded-lg transition-colors flex items-center justify-center"
        >
          🖥️ Серверы
        </button>

        <button
          onClick={() => navigate('/admin/payments')}
          className="bg-red-500 hover:bg-red-600 text-white font-semibold py-3 px-4 rounded-lg transition-colors flex items-center justify-center"
        >
          💳 Платежи
        </button>

        <button
          onClick={() => navigate('/admin/subscriptions')}
          className="bg-red-500 hover:bg-red-600 text-white font-semibold py-3 px-4 rounded-lg transition-colors flex items-center justify-center"
        >
          🔐 Подписки
        </button>
      </div>
    </div>
  );
};
