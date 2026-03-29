// Language Selector
import React from 'react';

function LanguageSelector({ selectedLanguage, onLanguageChange, disabled }) {
  const languages = [
    { code: 'hindi', label: '🇮🇳 Hindi' },
    { code: 'spanish', label: '🇪🇸 Spanish' },
    { code: 'french', label: '🇫🇷 French' },
    { code: 'german', label: '🇩🇪 German' },
    { code: 'japanese', label: '🇯🇵 Japanese' },
    { code: 'arabic', label: '🇸🇦 Arabic' },
  ];

  return (
    <div className="relative">
      <select
        value={selectedLanguage}
        onChange={(e) => onLanguageChange(e.target.value)}
        disabled={disabled}
        className="w-full px-4 py-3 bg-slate-700 text-white border border-slate-600 rounded-lg appearance-none cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed hover:border-blue-500 transition-colors focus:outline-none focus:border-blue-500"
      >
        {languages.map((lang) => (
          <option key={lang.code} value={lang.code}>
            {lang.label}
          </option>
        ))}
      </select>

      {/* Custom dropdown arrow */}
      <svg className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 pointer-events-none" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
      </svg>
    </div>
  );
}

export default LanguageSelector;