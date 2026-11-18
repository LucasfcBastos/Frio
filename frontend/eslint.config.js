import js from '@eslint/js';
import prettier from 'eslint-config-prettier';
import reactHooks from 'eslint-plugin-react-hooks';
import reactRefresh from 'eslint-plugin-react-refresh';
import globals from 'globals';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  { ignores: ['dist', 'coverage', 'node_modules'] },
  {
    extends: [js.configs.recommended, ...tseslint.configs.recommended, prettier],
    files: ['**/*.{ts,tsx}'],
    languageOptions: { ecmaVersion: 2022, globals: globals.browser },
    plugins: { 'react-hooks': reactHooks, 'react-refresh': reactRefresh },
    rules: {
      ...reactHooks.configs.recommended.rules,
      'react-refresh/only-export-components': ['warn', { allowConstantExport: true }],
      // Architecture guard: HTTP lives only in services/api.
      'no-restricted-imports': [
        'error',
        { paths: [{ name: 'axios', message: 'Use a service from src/services/api instead.' }] },
      ],
    },
  },
  {
    files: ['src/services/api/**/*.ts'],
    rules: { 'no-restricted-imports': 'off' },
  },
  {
    files: ['src/contexts/**/*.tsx', 'src/test/**/*.tsx'],
    rules: { 'react-refresh/only-export-components': 'off' },
  },
);
