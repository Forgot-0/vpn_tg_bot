import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { showTelegramAlert } from '../utils/telegram';

export const Login: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      setIsLoading(true);
      await login();
      navigate('/');
    } catch (error: any) {
      console.error('Login failed:', error);
      const errorMessage =
        typeof error === 'string' ? error : 'Ошибка входа. Пожалуйста, попробуйте еще раз.';
      showTelegramAlert(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full border border-gray-200">
        <div className="text-center mb-8">
          <div className="text-6xl mb-4">🔐</div>
          <h1 className="text-4xl font-bold text-gray-800 mb-2 bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
            VPN Subscription
          </h1>
          <p className="text-gray-600">Войдите через Telegram для продолжения</p>
        </div>

        <button
          onClick={handleLogin}
          disabled={isLoading}
          className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white font-semibold py-4 px-4 rounded-xl transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center text-lg"
        >
          {isLoading ? (
            <>
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-3"></div>
              Вход...
            </>
          ) : (
            <>
              <span className="mr-2">📱</span>
              Войти через Telegram
            </>
          )}
        </button>

        <p className="text-sm text-gray-500 text-center mt-6">
          Нажимая кнопку, вы соглашаетесь с условиями использования сервиса
        </p>
      </div>
    </div>
  );
};
