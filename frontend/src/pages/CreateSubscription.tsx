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

    if (!price) {
      showTelegramAlert('Сначала рассчитайте цену');
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
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      <div className="max-w-3xl mx-auto p-4">
        <button
          onClick={() => navigate('/')}
          className="mb-4 text-blue-600 hover:text-blue-800 font-semibold flex items-center gap-2"
        >
          <span>←</span> Назад
        </button>

        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
          <h1 className="text-3xl font-bold text-gray-800 mb-6">✨ Создать подписку</h1>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Duration */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                📅 Длительность (дней)
              </label>
              <div className="grid grid-cols-4 md:grid-cols-7 gap-2">
                {DURATION_OPTIONS.map((days) => (
                  <button
                    key={days}
                    type="button"
                    onClick={() => {
                      setFormData((prev) => ({ ...prev, duration_days: days }));
                      setPrice(null);
                    }}
                    className={`py-3 px-4 rounded-lg border-2 font-semibold transition-all ${
                      formData.duration_days === days
                        ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white border-blue-600 shadow-md'
                        : 'bg-white text-gray-700 border-gray-300 hover:border-blue-500 hover:bg-blue-50'
                    }`}
                  >
                    {days}
                  </button>
                ))}
              </div>
            </div>

            {/* Device Count */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                📱 Количество устройств
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
                    className={`py-3 px-4 rounded-lg border-2 font-semibold transition-all ${
                      formData.device_count === count
                        ? 'bg-gradient-to-r from-purple-500 to-purple-600 text-white border-purple-600 shadow-md'
                        : 'bg-white text-gray-700 border-gray-300 hover:border-purple-500 hover:bg-purple-50'
                    }`}
                  >
                    {count}
                  </button>
                ))}
              </div>
            </div>

            {/* Protocols */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                🔐 Протоколы
              </label>
              <div className="space-y-2">
                {PROTOCOL_TYPES.map((protocol) => (
                  <label
                    key={protocol}
                    className={`flex items-center space-x-3 cursor-pointer p-4 rounded-lg border-2 transition-all ${
                      formData.protocol_types.includes(protocol)
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-300 hover:border-blue-300 bg-white'
                    }`}
                  >
                    <input
                      type="checkbox"
                      checked={formData.protocol_types.includes(protocol)}
                      onChange={() => toggleProtocol(protocol)}
                      className="w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                    />
                    <span className="text-gray-700 font-medium">{protocol}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Price Display */}
            {price !== null && (
              <div className="bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-200 rounded-lg p-6">
                <div className="flex justify-between items-center">
                  <div>
                    <p className="text-sm text-green-700 font-medium mb-1">💰 Итоговая цена</p>
                    <p className="text-3xl font-bold text-green-600">{price.toFixed(2)} ₽</p>
                  </div>
                  <div className="text-4xl">💳</div>
                </div>
              </div>
            )}

            {/* Actions */}
            <div className="flex gap-4 pt-4">
              <button
                type="button"
                onClick={calculatePrice}
                disabled={isCalculatingPrice || formData.protocol_types.length === 0}
                className="flex-1 bg-white hover:bg-gray-50 text-gray-800 font-semibold py-3 px-4 rounded-lg transition-all shadow-md hover:shadow-lg border border-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isCalculatingPrice ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-gray-600 inline-block mr-2"></div>
                    Расчет...
                  </>
                ) : (
                  '💰 Рассчитать цену'
                )}
              </button>
              <button
                type="submit"
                disabled={isLoading || price === null}
                className="flex-1 bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white font-semibold py-3 px-4 rounded-lg transition-all shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
              >
                {isLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Создание...
                  </>
                ) : (
                  <>
                    <span className="mr-2">✨</span>
                    Создать подписку
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};
