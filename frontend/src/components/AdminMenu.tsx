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
    <div className="admin-menu bg-gradient-to-r from-red-600 via-red-700 to-pink-600 text-white p-6 rounded-xl shadow-xl mb-6 border border-red-500">
      <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
        <span>⚙️</span> Админ Панель
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        <button
          onClick={() => navigate('/admin/users')}
          className="bg-white/20 hover:bg-white/30 backdrop-blur-sm text-white font-semibold py-3 px-4 rounded-lg transition-all shadow-md hover:shadow-lg flex items-center justify-center gap-2 border border-white/30"
        >
          <span>👥</span> Пользователи
        </button>

        <button
          onClick={() => navigate('/admin/servers')}
          className="bg-white/20 hover:bg-white/30 backdrop-blur-sm text-white font-semibold py-3 px-4 rounded-lg transition-all shadow-md hover:shadow-lg flex items-center justify-center gap-2 border border-white/30"
        >
          <span>🖥️</span> Серверы
        </button>

        <button
          onClick={() => navigate('/admin/payments')}
          className="bg-white/20 hover:bg-white/30 backdrop-blur-sm text-white font-semibold py-3 px-4 rounded-lg transition-all shadow-md hover:shadow-lg flex items-center justify-center gap-2 border border-white/30"
        >
          <span>💳</span> Платежи
        </button>

        <button
          onClick={() => navigate('/admin/subscriptions')}
          className="bg-white/20 hover:bg-white/30 backdrop-blur-sm text-white font-semibold py-3 px-4 rounded-lg transition-all shadow-md hover:shadow-lg flex items-center justify-center gap-2 border border-white/30"
        >
          <span>🔐</span> Подписки
        </button>

        <button
          onClick={() => navigate('/admin/prices')}
          className="bg-white/20 hover:bg-white/30 backdrop-blur-sm text-white font-semibold py-3 px-4 rounded-lg transition-all shadow-md hover:shadow-lg flex items-center justify-center gap-2 border border-white/30"
        >
          <span>💰</span> Цены
        </button>
      </div>
    </div>
  );
};
