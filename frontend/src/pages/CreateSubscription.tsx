import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiClient } from '../services/api';
import { showTelegramAlert } from '../utils/telegram';
import { Loading } from '../components/Loading';

const PROTOCOL_TYPES = ['vless', 'vmess', 'trojan'];
const DURATION_OPTIONS = [7, 14, 30, 60, 90, 180, 365];
const DEVICE_COUNT_OPTIONS = [1, 2, 3, 4, 5];

export const CreateSubscription: React.FC = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [isCalculatingPrice, setIsCalculatingPrice] = useState(false);
  const [price, setPrice] = useState<number | null>(null);

  const [formData, setFormData] = useState({
    duration_days: 30,
    device_count: 1,
    protocol_types: ['vless'] as string[],
  });

  const calculatePrice = async () => {
    try {
      setIsCalculatingPrice(true);
      const calculatedPrice = await apiClient.getPrice(formData);
      setPrice(calculatedPrice);
    } catch (error) {
      console.error('Failed to calculate price:', error);
      showTelegramAlert('Не удалось рассчитать цену');
    } finally {
      setIsCalculatingPrice(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (formData.protocol_types.length === 0) {
      showTelegramAlert('Выберите хотя бы один протокол');
      return;
    }

    try {
      setIsLoading(true);
      const paymentUrl = await apiClient.createSubscription(formData);
      
      // Перенаправляем на страницу оплаты
      window.location.href = paymentUrl;
    } catch (error) {
      console.error('Failed to create subscription:', error);
      showTelegramAlert('Ошибка при создании подписки. Попробуйте еще раз.');
    } finally {
      setIsLoading(false);
    }
  };

  const toggleProtocol = (protocol: string) => {
    setFormData((prev) => ({
      ...prev,
      protocol_types: prev.protocol_types.includes(protocol)
        ? prev.protocol_types.filter((p) => p !== protocol)
        : [...prev.protocol_types, protocol],
    }));
    setPrice(null); // Сбрасываем цену при изменении
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-2xl mx-auto p-4">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h1 className="text-2xl font-bold text-gray-800 mb-6">Создать подписку</h1>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Длительность (дней)
              </label>
              <div className="grid grid-cols-4 gap-2">
                {DURATION_OPTIONS.map((days) => (
                  <button
                    key={days}
                    type="button"
                    onClick={() => {
                      setFormData((prev) => ({ ...prev, duration_days: days }));
                      setPrice(null);
                    }}
                    className={`py-2 px-4 rounded-lg border transition-colors ${
                      formData.duration_days === days
                        ? 'bg-blue-500 text-white border-blue-500'
                        : 'bg-white text-gray-700 border-gray-300 hover:border-blue-500'
                    }`}
                  >
                    {days}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Количество устройств
              </label>
              <div className="grid grid-cols-5 gap-2">
                {DEVICE_COUNT_OPTIONS.map((count) => (
                  <button
                    key={count}
                    type="button"
                    onClick={() => {
                      setFormData((prev) => ({ ...prev, device_count: count }));
                      setPrice(null);
                    }}
                    className={`py-2 px-4 rounded-lg border transition-colors ${
                      formData.device_count === count
                        ? 'bg-blue-500 text-white border-blue-500'
                        : 'bg-white text-gray-700 border-gray-300 hover:border-blue-500'
                    }`}
                  >
                    {count}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Протоколы
              </label>
              <div className="space-y-2">
                {PROTOCOL_TYPES.map((protocol) => (
                  <label
                    key={protocol}
                    className="flex items-center space-x-2 cursor-pointer p-3 rounded-lg border border-gray-300 hover:border-blue-500 transition-colors"
                  >
                    <input
                      type="checkbox"
                      checked={formData.protocol_types.includes(protocol)}
                      onChange={() => toggleProtocol(protocol)}
                      className="w-5 h-5 text-blue-600 rounded"
                    />
                    <span className="text-gray-700">{protocol}</span>
                  </label>
                ))}
              </div>
            </div>

            {price !== null && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex justify-between items-center">
                  <span className="text-lg font-semibold text-gray-800">Цена:</span>
                  <span className="text-2xl font-bold text-blue-600">{price.toFixed(2)} ₽</span>
                </div>
              </div>
            )}

            <div className="flex gap-4">
              <button
                type="button"
                onClick={calculatePrice}
                disabled={isCalculatingPrice || formData.protocol_types.length === 0}
                className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-2 px-4 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isCalculatingPrice ? 'Расчет...' : 'Рассчитать цену'}
              </button>
              <button
                type="submit"
                disabled={isLoading || price === null}
                className="flex-1 bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
              >
                {isLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Создание...
                  </>
                ) : (
                  'Создать подписку'
                )}
              </button>
            </div>

            <button
              type="button"
              onClick={() => navigate('/')}
              className="w-full bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-2 px-4 rounded-lg transition-colors"
            >
              Отмена
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

