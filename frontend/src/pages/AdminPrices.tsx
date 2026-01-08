import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAdmin } from '../contexts/AdminContext';
import { apiClient } from '../services/api';
import { Loading } from '../components/Loading';
import { showTelegramAlert, showTelegramConfirm } from '../utils/telegram';
import type { PriceConfig, AddProtocolPriceRequest, AddRegionPriceRequest } from '../types';

export const AdminPrices: React.FC = () => {
  const navigate = useNavigate();
  const { isAdmin } = useAdmin();
  const [priceConfig, setPriceConfig] = useState<PriceConfig | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [isAddingProtocol, setIsAddingProtocol] = useState(false);
  const [isAddingRegion, setIsAddingRegion] = useState(false);

  // Form states for update
  const [formData, setFormData] = useState({
    daily_rate: 0,
    device_rate_multiplier: 1,
    region_base_multiplier: 1,
    protocol_base_multiplier: 1,
    region_multipliers: {} as Record<string, number>,
    protocol_multipliers: {} as Record<string, number>,
  });

  // Form states for adding protocol/region
  const [newProtocol, setNewProtocol] = useState({ protocol: '', coef: 1 });
  const [newRegion, setNewRegion] = useState({ region: '', coef: 1 });

  useEffect(() => {
    if (!isAdmin) {
      navigate('/');
      return;
    }
    loadPriceConfig();
  }, [isAdmin]);

  const loadPriceConfig = async () => {
    try {
      setIsLoading(true);
      const config = await apiClient.getPriceConfig();
      setPriceConfig(config);
      setFormData({
        daily_rate: config.daily_rate,
        device_rate_multiplier: config.device_rate_multiplier,
        region_base_multiplier: config.region_base_multiplier,
        protocol_base_multiplier: config.protocol_base_multiplier,
        region_multipliers: { ...config.region_multipliers },
        protocol_multipliers: { ...config.protocol_multipliers },
      });
    } catch (error: any) {
      console.error('Failed to load price config:', error);
      const errorMessage =
        error.response?.data?.error?.message || 'Ошибка при загрузке конфигурации цен';
      showTelegramAlert(errorMessage);
      if (error.response?.status === 403 || error.response?.status === 401) {
        navigate('/');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    const confirmed = await showTelegramConfirm(
      'Вы уверены, что хотите обновить конфигурацию цен? Это повлияет на все новые подписки.'
    );

    if (!confirmed) return;

    try {
      setIsSaving(true);
      await apiClient.updatePrice(formData);
      showTelegramAlert('Конфигурация цен успешно обновлена');
      await loadPriceConfig();
    } catch (error: any) {
      console.error('Failed to update price config:', error);
      const errorMessage =
        error.response?.data?.error?.message || 'Ошибка при обновлении конфигурации цен';
      showTelegramAlert(errorMessage);
    } finally {
      setIsSaving(false);
    }
  };

  const handleAddProtocol = async () => {
    if (!newProtocol.protocol.trim()) {
      showTelegramAlert('Укажите название протокола');
      return;
    }

    try {
      setIsAddingProtocol(true);
      const request: AddProtocolPriceRequest = {
        protocol: newProtocol.protocol.trim(),
        coef: newProtocol.coef,
      };
      await apiClient.addProtocolPrice(request);
      showTelegramAlert('Протокол успешно добавлен');
      setNewProtocol({ protocol: '', coef: 1 });
      await loadPriceConfig();
    } catch (error: any) {
      console.error('Failed to add protocol:', error);
      const errorMessage =
        error.response?.data?.error?.message || 'Ошибка при добавлении протокола';
      showTelegramAlert(errorMessage);
    } finally {
      setIsAddingProtocol(false);
    }
  };

  const handleAddRegion = async () => {
    if (!newRegion.region.trim()) {
      showTelegramAlert('Укажите код региона');
      return;
    }

    try {
      setIsAddingRegion(true);
      const request: AddRegionPriceRequest = {
        region: newRegion.region.trim(),
        coef: newRegion.coef,
      };
      await apiClient.addRegionPrice(request);
      showTelegramAlert('Регион успешно добавлен');
      setNewRegion({ region: '', coef: 1 });
      await loadPriceConfig();
    } catch (error: any) {
      console.error('Failed to add region:', error);
      const errorMessage = error.response?.data?.error?.message || 'Ошибка при добавлении региона';
      showTelegramAlert(errorMessage);
    } finally {
      setIsAddingRegion(false);
    }
  };

  const handleRemoveProtocol = (protocol: string) => {
    const updated = { ...formData.protocol_multipliers };
    delete updated[protocol];
    setFormData({ ...formData, protocol_multipliers: updated });
  };

  const handleRemoveRegion = (region: string) => {
    const updated = { ...formData.region_multipliers };
    delete updated[region];
    setFormData({ ...formData, region_multipliers: updated });
  };

  if (isLoading) {
    return <Loading />;
  }

  if (!priceConfig) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50 p-4">
        <div className="max-w-7xl mx-auto">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <p className="text-center text-gray-600">Конфигурация цен не найдена</p>
          </div>
        </div>
      </div>
    );
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
            <h1 className="text-3xl font-bold text-gray-900 leading-tight">💰 Управление ценами</h1>
          </div>

          {/* Base Configuration */}
          <div className="mb-8 bg-gray-50 rounded-lg p-6 border border-gray-200">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">⚙️ Базовая конфигурация</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Дневная ставка (₽)
                </label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={formData.daily_rate}
                  onChange={(e) =>
                    setFormData({ ...formData, daily_rate: parseFloat(e.target.value) || 0 })
                  }
                  className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Множитель устройства
                </label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={formData.device_rate_multiplier}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      device_rate_multiplier: parseFloat(e.target.value) || 0,
                    })
                  }
                  className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Базовый множитель региона
                </label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={formData.region_base_multiplier}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      region_base_multiplier: parseFloat(e.target.value) || 0,
                    })
                  }
                  className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Базовый множитель протокола
                </label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={formData.protocol_base_multiplier}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      protocol_base_multiplier: parseFloat(e.target.value) || 0,
                    })
                  }
                  className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                />
              </div>
            </div>
          </div>

          {/* Protocol Multipliers */}
          <div className="mb-8 bg-gray-50 rounded-lg p-6 border border-gray-200">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">🔐 Множители протоколов</h2>

            {/* Add Protocol */}
            <div className="mb-4 bg-white rounded-lg p-4 border-2 border-blue-300">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Добавить протокол</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Протокол
                  </label>
                  <input
                    type="text"
                    value={newProtocol.protocol}
                    onChange={(e) => setNewProtocol({ ...newProtocol, protocol: e.target.value })}
                    placeholder="vless, vmess, etc."
                    className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Коэффициент
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    value={newProtocol.coef}
                    onChange={(e) =>
                      setNewProtocol({ ...newProtocol, coef: parseFloat(e.target.value) || 0 })
                    }
                    className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                  />
                </div>
                <div className="flex items-end">
                  <button
                    onClick={handleAddProtocol}
                    disabled={isAddingProtocol}
                    className="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-all shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isAddingProtocol ? 'Добавление...' : '+ Добавить'}
                  </button>
                </div>
              </div>
            </div>

            {/* Protocol List */}
            <div className="space-y-2">
              {Object.entries(formData.protocol_multipliers).map(([protocol, coef]) => (
                <div
                  key={protocol}
                  className="bg-white rounded-lg p-4 border-2 border-gray-300 flex items-center justify-between"
                >
                  <div className="flex items-center gap-4">
                    <span className="font-bold text-gray-900 text-lg">{protocol}</span>
                    <span className="text-gray-600">×</span>
                    <input
                      type="number"
                      step="0.01"
                      min="0"
                      value={coef}
                      onChange={(e) => {
                        const updated = { ...formData.protocol_multipliers };
                        updated[protocol] = parseFloat(e.target.value) || 0;
                        setFormData({ ...formData, protocol_multipliers: updated });
                      }}
                      className="px-3 py-1 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none w-24"
                    />
                  </div>
                  <button
                    onClick={() => handleRemoveProtocol(protocol)}
                    className="px-4 py-2 bg-red-500 hover:bg-red-600 text-white font-semibold rounded-lg transition-colors"
                  >
                    Удалить
                  </button>
                </div>
              ))}
              {Object.keys(formData.protocol_multipliers).length === 0 && (
                <p className="text-gray-600 text-center py-4">Нет добавленных протоколов</p>
              )}
            </div>
          </div>

          {/* Region Multipliers */}
          <div className="mb-8 bg-gray-50 rounded-lg p-6 border border-gray-200">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">🌍 Множители регионов</h2>

            {/* Add Region */}
            <div className="mb-4 bg-white rounded-lg p-4 border-2 border-green-300">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Добавить регион</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Код региона
                  </label>
                  <input
                    type="text"
                    value={newRegion.region}
                    onChange={(e) => setNewRegion({ ...newRegion, region: e.target.value })}
                    placeholder="RU, US, etc."
                    className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:border-green-500 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Коэффициент
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    value={newRegion.coef}
                    onChange={(e) =>
                      setNewRegion({ ...newRegion, coef: parseFloat(e.target.value) || 0 })
                    }
                    className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:border-green-500 focus:outline-none"
                  />
                </div>
                <div className="flex items-end">
                  <button
                    onClick={handleAddRegion}
                    disabled={isAddingRegion}
                    className="w-full bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-semibold py-2 px-4 rounded-lg transition-all shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isAddingRegion ? 'Добавление...' : '+ Добавить'}
                  </button>
                </div>
              </div>
            </div>

            {/* Region List */}
            <div className="space-y-2">
              {Object.entries(formData.region_multipliers).map(([region, coef]) => (
                <div
                  key={region}
                  className="bg-white rounded-lg p-4 border-2 border-gray-300 flex items-center justify-between"
                >
                  <div className="flex items-center gap-4">
                    <span className="font-bold text-gray-900 text-lg">{region}</span>
                    <span className="text-gray-600">×</span>
                    <input
                      type="number"
                      step="0.01"
                      min="0"
                      value={coef}
                      onChange={(e) => {
                        const updated = { ...formData.region_multipliers };
                        updated[region] = parseFloat(e.target.value) || 0;
                        setFormData({ ...formData, region_multipliers: updated });
                      }}
                      className="px-3 py-1 border-2 border-gray-300 rounded-lg focus:border-green-500 focus:outline-none w-24"
                    />
                  </div>
                  <button
                    onClick={() => handleRemoveRegion(region)}
                    className="px-4 py-2 bg-red-500 hover:bg-red-600 text-white font-semibold rounded-lg transition-colors"
                  >
                    Удалить
                  </button>
                </div>
              ))}
              {Object.keys(formData.region_multipliers).length === 0 && (
                <p className="text-gray-600 text-center py-4">Нет добавленных регионов</p>
              )}
            </div>
          </div>

          {/* Save Button */}
          <div className="flex justify-end">
            <button
              onClick={handleSave}
              disabled={isSaving}
              className="bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-semibold py-3 px-8 rounded-lg transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed text-lg"
            >
              {isSaving ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white inline-block mr-2"></div>
                  Сохранение...
                </>
              ) : (
                '💾 Сохранить конфигурацию'
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

