// .eslintrc.js
module.exports = {
  root: true,
  env: {
    node: true,
    browser: true,
  },
  extends: [
    'plugin:vue/vue3-essential', // Плагін для Vue.js 3
    'eslint:recommended',         // Рекомендовані правила ESLint
  ],
  parser: 'vue-eslint-parser',     // Парсер для Vue.js файлів
  parserOptions: {
    parser: '@babel/eslint-parser', // Парсер для JavaScript
    requireConfigFile: false,       // Не потребує окремого Babel конфігураційного файлу
    ecmaVersion: 2020,              // Версія ECMAScript
    sourceType: 'module',           // Використання модулів
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'linebreak-style': 'off', // Вимкнути перевірку стилю переведення рядків
    'vue/multi-word-component-names': 'off', // Тимчасово вимкнути правило для багатослівних імен компонентів
  },
};
