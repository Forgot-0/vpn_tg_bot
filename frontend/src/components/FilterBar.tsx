import React from 'react';

interface FilterOption {
  value: string;
  label: string;
}

interface FilterBarProps {
  filters: {
    [key: string]: {
      label: string;
      options: FilterOption[];
      value: string;
      onChange: (value: string) => void;
    };
  };
  onReset: () => void;
}

export const FilterBar: React.FC<FilterBarProps> = ({ filters, onReset }) => {
  const hasActiveFilters = Object.values(filters).some((f) => f.value !== '' && f.value !== 'all');

  return (
    <div className="bg-white rounded-lg shadow-lg p-5 mb-6 border-2 border-gray-300">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-gray-900">🔍 Фильтры</h3>
        {hasActiveFilters && (
          <button
            onClick={onReset}
            className="text-sm text-blue-700 hover:text-blue-900 font-bold hover:underline"
          >
            Сбросить все
          </button>
        )}
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {Object.entries(filters).map(([key, filter]) => (
          <div key={key}>
            <label className="block text-sm font-bold text-gray-900 mb-2">
              {filter.label}
            </label>
            <select
              value={filter.value}
              onChange={(e) => filter.onChange(e.target.value)}
              className="w-full px-4 py-2.5 border-2 border-gray-400 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-600 bg-white text-gray-900 font-medium"
            >
              {filter.options.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
        ))}
      </div>
    </div>
  );
};

