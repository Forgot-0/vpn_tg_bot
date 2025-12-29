import React from 'react';

interface FilterOption {
  value: string;
  label: string;
}

type FilterType = 'select' | 'text' | 'number' | 'date' | 'checkbox' | 'range';

interface BaseFilter {
  label: string;
  type: FilterType;
  value: any;
  onChange: (value: any) => void;
}

interface SelectFilter extends BaseFilter {
  type: 'select';
  options: FilterOption[];
}

interface TextFilter extends BaseFilter {
  type: 'text';
  placeholder?: string;
}

interface NumberFilter extends BaseFilter {
  type: 'number';
  min?: number;
  max?: number;
  placeholder?: string;
}

interface DateFilter extends BaseFilter {
  type: 'date';
}

interface CheckboxFilter extends BaseFilter {
  type: 'checkbox';
  labelTrue?: string;
  labelFalse?: string;
}

interface RangeFilter extends BaseFilter {
  type: 'range';
  min?: number;
  max?: number;
  step?: number;
  minLabel?: string;
  maxLabel?: string;
}

type Filter = SelectFilter | TextFilter | NumberFilter | DateFilter | CheckboxFilter | RangeFilter;

interface FilterBarProps {
  filters: {
    [key: string]: Filter;
  };
  onReset: () => void;
}

export const FilterBar: React.FC<FilterBarProps> = ({ filters, onReset }) => {
  const hasActiveFilters = Object.values(filters).some((f) => {
    if (f.type === 'select') {
      return f.value !== '' && f.value !== 'all';
    }
    if (f.type === 'checkbox') {
      return f.value !== undefined && f.value !== null;
    }
    if (f.type === 'range') {
      return f.value?.min !== undefined || f.value?.max !== undefined;
    }
    return f.value !== '' && f.value !== undefined && f.value !== null;
  });

  const renderFilter = (key: string, filter: Filter) => {
    switch (filter.type) {
      case 'select':
        return (
          <div key={key}>
            <label className="block text-sm font-bold text-gray-900 mb-2">
              {filter.label}
            </label>
            <select
              value={filter.value || 'all'}
              onChange={(e) => filter.onChange(e.target.value)}
              className="w-full px-4 py-2.5 border-2 border-gray-400 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-600 bg-white text-gray-900 font-medium text-base"
            >
              {filter.options.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
        );

      case 'text':
        return (
          <div key={key}>
            <label className="block text-sm font-bold text-gray-900 mb-2">
              {filter.label}
            </label>
            <input
              type="text"
              value={filter.value || ''}
              onChange={(e) => filter.onChange(e.target.value)}
              placeholder={filter.placeholder}
              className="w-full px-4 py-2.5 border-2 border-gray-400 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-600 bg-white text-gray-900 font-medium text-base"
            />
          </div>
        );

      case 'number':
        return (
          <div key={key}>
            <label className="block text-sm font-bold text-gray-900 mb-2">
              {filter.label}
            </label>
            <input
              type="number"
              value={filter.value || ''}
              onChange={(e) => filter.onChange(e.target.value ? Number(e.target.value) : undefined)}
              placeholder={filter.placeholder}
              min={filter.min}
              max={filter.max}
              className="w-full px-4 py-2.5 border-2 border-gray-400 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-600 bg-white text-gray-900 font-medium text-base"
            />
          </div>
        );

      case 'date':
        return (
          <div key={key}>
            <label className="block text-sm font-bold text-gray-900 mb-2">
              {filter.label}
            </label>
            <input
              type="date"
              value={filter.value || ''}
              onChange={(e) => filter.onChange(e.target.value || undefined)}
              className="w-full px-4 py-2.5 border-2 border-gray-400 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-600 bg-white text-gray-900 font-medium text-base"
            />
          </div>
        );

      case 'checkbox':
        return (
          <div key={key} className="flex items-center space-x-3">
            <input
              type="checkbox"
              checked={filter.value === true}
              onChange={(e) => filter.onChange(e.target.checked ? true : undefined)}
              className="w-5 h-5 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
            />
            <label className="text-sm font-bold text-gray-900 cursor-pointer">
              {filter.label}
            </label>
          </div>
        );

      case 'range':
        const rangeValue = filter.value || { min: undefined, max: undefined };
        return (
          <div key={key} className="space-y-2">
            <label className="block text-sm font-bold text-gray-900 mb-2">
              {filter.label}
            </label>
            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="block text-xs text-gray-600 mb-1 font-medium">
                  {filter.minLabel || 'От'}
                </label>
                <input
                  type="number"
                  value={rangeValue.min || ''}
                  onChange={(e) =>
                    filter.onChange({
                      ...rangeValue,
                      min: e.target.value ? Number(e.target.value) : undefined,
                    })
                  }
                  placeholder="Мин"
                  min={filter.min}
                  max={filter.max}
                  step={filter.step}
                  className="w-full px-3 py-2 border-2 border-gray-400 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-600 bg-white text-gray-900 font-medium text-sm"
                />
              </div>
              <div>
                <label className="block text-xs text-gray-600 mb-1 font-medium">
                  {filter.maxLabel || 'До'}
                </label>
                <input
                  type="number"
                  value={rangeValue.max || ''}
                  onChange={(e) =>
                    filter.onChange({
                      ...rangeValue,
                      max: e.target.value ? Number(e.target.value) : undefined,
                    })
                  }
                  placeholder="Макс"
                  min={filter.min}
                  max={filter.max}
                  step={filter.step}
                  className="w-full px-3 py-2 border-2 border-gray-400 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-600 bg-white text-gray-900 font-medium text-sm"
                />
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-5 mb-6 border-2 border-gray-300">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-gray-900">🔍 Фильтры</h3>
        {hasActiveFilters && (
          <button
            onClick={onReset}
            className="text-sm text-blue-700 hover:text-blue-900 font-bold hover:underline transition-colors"
          >
            Сбросить все
          </button>
        )}
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {Object.entries(filters).map(([key, filter]) => renderFilter(key, filter))}
      </div>
    </div>
  );
};
