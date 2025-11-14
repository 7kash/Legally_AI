import { defineVitestConfig } from '@nuxt/test-utils/config'

export default defineVitestConfig({
  test: {
    environment: 'happy-dom',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],
      include: [
        'components/**/*.{vue,ts}',
        'composables/**/*.ts',
        'utils/**/*.ts',
        'stores/**/*.ts',
      ],
      exclude: [
        'node_modules/',
        '.nuxt/',
        'dist/',
        '**/*.spec.ts',
        '**/*.test.ts',
        '**/*.d.ts',
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },
    globals: true,
    setupFiles: ['./test/setup.ts'],
  },
})
