# Legally AI - Frontend

> Modern, multilingual contract analysis interface built with Nuxt 3

## Overview

The Legally AI frontend is a progressive web application (PWA) that provides a delightful user experience for contract analysis across 4 languages (English, Russian, French, Serbian). Built with mobile-first principles and WCAG 2.1 AA accessibility compliance.

## Tech Stack

- **Framework**: [Nuxt 3](https://nuxt.com/) - The Intuitive Vue Framework
- **Language**: TypeScript (strict mode)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/) + Custom Design Tokens
- **State Management**: [Pinia](https://pinia.vuejs.org/)
- **UI Utilities**: [VueUse](https://vueuse.org/)
- **Testing**:
  - Unit: [Vitest](https://vitest.dev/) v3.2.0
  - E2E: [Playwright](https://playwright.dev/)
  - Accessibility: [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)
- **PWA**: [@vite-pwa/nuxt](https://vite-pwa-org.netlify.app/) with Workbox
- **i18n**: [@nuxtjs/i18n](https://i18n.nuxtjs.org/)

## Features

### ✅ Core Features (Complete)

- **Authentication**
  - User registration and login
  - JWT token management
  - Password reset flow (forgot password, reset with token)
  - Email verification
  - Protected routes with middleware

- **Contract Upload**
  - Drag-and-drop file upload
  - File validation (PDF, DOCX, 10MB max)
  - Upload progress tracking
  - Multiple file support

- **Real-Time Analysis**
  - Server-Sent Events (SSE) for live updates
  - Progress timeline with event tracking
  - Confidence score visualization
  - Comprehensive result sections

- **Analysis History**
  - List of past analyses
  - Filtering and sorting
  - Quick access to results

- **User Account**
  - Profile settings
  - Usage statistics
  - Subscription management (UI ready)

### ✨ Premium Features (Complete)

- **Dark Mode**
  - System preference detection
  - Manual toggle
  - Theme persistence in localStorage
  - Smooth transitions

- **Multi-Language Support**
  - 4 languages: English, Russian (Русский), French (Français), Serbian (Српски)
  - Browser language detection
  - Language selector with flags
  - Persistent locale preference

- **Progressive Web App (PWA)**
  - Offline support with service worker
  - Installable on mobile and desktop
  - Smart caching strategies:
    - API: NetworkFirst (1-hour cache)
    - Images: CacheFirst (30-day cache)
  - Auto-update on new versions

- **Notifications System**
  - 4 types: success, error, warning, info
  - Auto-dismiss with configurable duration
  - Manual dismiss option
  - Accessible with ARIA labels

- **Loading Skeletons**
  - Improved perceived performance
  - 4 variants: text, circle, rect, card
  - Smooth pulse animation

- **Export Functionality**
  - Export analysis results
  - PDF/DOCX format (placeholder for full implementation)
  - Metadata inclusion

- **Analytics Tracking**
  - Page view tracking
  - Custom event tracking
  - Router integration
  - Privacy-respecting (client-side only)

### 🎨 Design System

#### Colors
- **Primary**: Blue scale (50-950)
- **Secondary**: Purple scale (50-950)
- **Success**: Green (50, 500, 700)
- **Warning**: Amber (50, 500, 700)
- **Error**: Red (50, 500, 700)
- **Gray**: Neutral scale (50-900)

#### Typography
- **Font Family**: Inter (sans-serif), Fira Code (monospace)
- **Sizes**: xs, sm, base, lg, xl, 2xl, 3xl, 4xl, 5xl
- **Weights**: normal (400), medium (500), semibold (600), bold (700)

#### Spacing
- **Base**: 8px system
- **Scale**: 1 (4px) to 24 (96px)

#### Animations
- **fade-in**: 300ms ease-in-out
- **slide-up**: 300ms ease-out
- **slide-down**: 300ms ease-out
- **spin**: 1s linear infinite

## Project Structure

```
frontend/
├── .nuxt/                      # Auto-generated (gitignored)
├── node_modules/               # Dependencies (gitignored)
├── public/                     # Static assets
│   └── manifest.json          # PWA manifest
├── assets/                     # Compiled assets
│   └── styles/
│       ├── main.scss          # Global styles
│       ├── variables.scss     # CSS variables & design tokens
│       └── tailwind.css       # Tailwind entry point
├── components/                 # Vue components
│   ├── analysis/
│   │   ├── AnalysisSection.vue
│   │   └── FileUpload.vue
│   └── common/
│       ├── NotificationContainer.vue
│       ├── ThemeToggle.vue
│       ├── LanguageSwitcher.vue
│       └── SkeletonLoader.vue
├── composables/                # Composition functions
│   ├── useDarkMode.ts
│   └── useNotifications.ts
├── layouts/                    # Layout components
│   └── default.vue
├── middleware/                 # Route middleware
│   ├── auth.ts                # Protected routes
│   └── guest.ts               # Public-only routes
├── pages/                      # File-based routing
│   ├── index.vue              # Landing page
│   ├── login.vue              # Login
│   ├── register.vue           # Registration
│   ├── upload.vue             # Upload contracts
│   ├── history.vue            # Past analyses
│   ├── account.vue            # User settings
│   ├── analysis/
│   │   └── [id].vue           # Analysis results (SSE)
│   └── auth/
│       ├── forgot-password.vue
│       ├── reset-password.vue
│       └── verify-email.vue
├── plugins/                    # Nuxt plugins
│   ├── auth.client.ts         # Auth initialization
│   └── analytics.client.ts    # Analytics tracking
├── stores/                     # Pinia stores
│   ├── auth.ts                # Authentication state
│   ├── contracts.ts           # Contract uploads
│   └── analyses.ts            # Analysis results & SSE
├── utils/                      # Utility functions
│   └── exportToPDF.ts         # PDF export helper
├── types/                      # TypeScript types
│   └── index.ts
├── .gitignore
├── .eslintrc.cjs              # ESLint config
├── .prettierrc                # Prettier config
├── nuxt.config.ts             # Nuxt configuration
├── tailwind.config.ts         # Tailwind configuration
├── i18n.config.ts             # i18n configuration
├── pwa.config.ts              # PWA configuration
├── tsconfig.json              # TypeScript config
├── vitest.config.ts           # Vitest config
├── playwright.config.ts       # Playwright config
├── package.json
└── README.md                  # This file
```

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- Backend API running (see `/backend/README.md`)

### Installation

```bash
# Install dependencies
npm install

# Copy environment variables (if needed)
cp .env.example .env

# Edit .env with your API base URL
# NUXT_PUBLIC_API_BASE=http://localhost:8000/api
```

### Development

```bash
# Start development server
npm run dev

# Development server runs at http://localhost:3000
```

### Building for Production

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

### Testing

```bash
# Run unit tests
npm run test

# Run unit tests in watch mode
npm run test:watch

# Run unit tests with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e

# Run E2E tests in UI mode
npm run test:e2e:ui

# Run accessibility tests
npm run test:a11y

# Lint code
npm run lint

# Format code
npm run format
```

## Configuration

### Environment Variables

```bash
# Runtime Config (public)
NUXT_PUBLIC_API_BASE=http://localhost:8000/api
NUXT_PUBLIC_ENABLE_ANALYTICS=false
```

### Nuxt Config

Key configurations in `nuxt.config.ts`:

- **TypeScript**: Strict mode enabled
- **Modules**: Tailwind, Pinia, VueUse, i18n, PWA
- **Runtime Config**: API base URL, analytics flag
- **PWA**: Auto-update, offline caching, manifest
- **i18n**: 4 locales, browser detection, cookie persistence

### Tailwind Config

Custom theme extensions in `tailwind.config.ts`:

- **Colors**: Primary, secondary, semantic colors
- **Fonts**: Inter, Fira Code
- **Animations**: Fade, slide, spin
- **Dark Mode**: Selector strategy with `[data-theme="dark"]`

## Key Components

### Authentication

**Stores**: `stores/auth.ts`
- `login(credentials)`: Authenticate user
- `register(data)`: Create new account
- `logout()`: Clear session
- `checkAuth()`: Validate token

**Pages**:
- `/login` - Login form with email/password
- `/register` - Registration form
- `/auth/forgot-password` - Request password reset
- `/auth/reset-password?token=xxx` - Set new password
- `/auth/verify-email?token=xxx` - Verify email address

### Contract Upload

**Store**: `stores/contracts.ts`
- `uploadContract(file)`: Upload single file
- `fetchContracts()`: Get upload history
- `deleteContract(id)`: Remove upload

**Component**: `components/analysis/FileUpload.vue`
- Drag-and-drop zone
- File validation (type, size)
- Progress indicator
- Error handling

### Analysis Results

**Store**: `stores/analyses.ts`
- `connectSSE(analysisId)`: Subscribe to real-time updates
- `disconnectSSE()`: Close SSE connection
- `fetchAnalysis(id)`: Get analysis details
- `submitFeedback(...)`: Send user feedback

**Page**: `/pages/analysis/[id].vue`
- Real-time progress timeline
- Event stream display
- Confidence score badge
- Export button
- Feedback forms

### Notifications

**Composable**: `composables/useNotifications.ts`

```typescript
const { success, error, warning, info } = useNotifications()

// Show success notification
success('Analysis complete', 'Your contract has been analyzed')

// Show error
error('Upload failed', 'Please try again')
```

**Component**: `components/common/NotificationContainer.vue`
- Auto-positioning (top-right)
- Auto-dismiss (configurable)
- Manual dismiss button
- Accessible with ARIA

### Dark Mode

**Composable**: `composables/useDarkMode.ts`

```typescript
const { isDark, toggle, setDark, setLight } = useDarkMode()

// Toggle theme
toggle()

// Set specific theme
setDark()
setLight()

// Check current theme
if (isDark.value) { /* ... */ }
```

**Component**: `components/common/ThemeToggle.vue`
- Sun/moon icon toggle
- Accessible label
- Smooth transitions

### Multi-Language

**Config**: `i18n.config.ts`
- Full translations for EN, RU, FR, SR
- Organized by section (nav, auth, upload, analysis, etc.)

**Component**: `components/common/LanguageSwitcher.vue`
- Dropdown selector
- Flag indicators
- Locale persistence

**Usage**:
```vue
<template>
  <h1>{{ $t('auth.loginTitle') }}</h1>
  <button>{{ $t('nav.upload') }}</button>
</template>
```

## API Integration

All API calls use the runtime config for base URL:

```typescript
const config = useRuntimeConfig()
const baseURL = config.public.apiBase

// Example: Upload contract
await $fetch('/contracts/upload', {
  method: 'POST',
  body: formData,
  baseURL,
  headers: {
    Authorization: `Bearer ${token}`,
  },
})
```

### Server-Sent Events (SSE)

Real-time analysis updates via SSE:

```typescript
const analysisId = route.params.id
const baseURL = useRuntimeConfig().public.apiBase
const url = `${baseURL}/analyses/${analysisId}/stream?token=${token}`

const eventSource = new EventSource(url)

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data)
  // Handle event: parsing | preparation | analysis | formatting | completed
}

eventSource.onerror = () => {
  eventSource.close()
}
```

## Styling Guidelines

### Using Tailwind

Prefer Tailwind utility classes for consistency:

```vue
<template>
  <button class="btn btn--primary">
    Click me
  </button>
</template>
```

### Custom Components

Use SCSS with design tokens from `variables.scss`:

```scss
<style lang="scss" scoped>
.custom-component {
  background: var(--color-background);
  color: var(--color-text);
  border-radius: var(--radius-lg);
  padding: $spacing-4;

  &:hover {
    background: var(--color-background-secondary);
  }
}

// Dark mode support
[data-theme='dark'] & {
  box-shadow: var(--shadow-md);
}
</style>
```

### Responsive Design

Mobile-first approach with Tailwind breakpoints:

```vue
<div class="text-sm md:text-base lg:text-lg">
  <!-- Text size scales with viewport -->
</div>

<div class="flex flex-col md:flex-row">
  <!-- Stack on mobile, row on tablet+ -->
</div>
```

## Accessibility

All components follow WCAG 2.1 AA standards:

- **Semantic HTML**: Proper heading hierarchy, landmarks
- **Keyboard Navigation**: All interactive elements accessible via keyboard
- **Focus Management**: Visible focus indicators, logical tab order
- **ARIA Labels**: Screen reader support for dynamic content
- **Color Contrast**: Minimum 4.5:1 ratio for text
- **Form Validation**: Clear error messages with aria-invalid, aria-describedby

### Accessibility Testing

```bash
# Run Lighthouse CI for accessibility audit
npm run test:a11y

# Manual testing checklist:
# - Tab through all interactive elements
# - Test with screen reader (NVDA, VoiceOver)
# - Verify focus indicators visible
# - Check color contrast (use browser DevTools)
```

## Performance

### Bundle Optimization

- **Code Splitting**: Automatic route-based splitting
- **Tree Shaking**: Unused code eliminated
- **Minification**: Terser for production builds
- **Image Optimization**: Use Nuxt Image for automatic optimization

### PWA Caching

Workbox strategies configured in `nuxt.config.ts`:

- **API Calls**: NetworkFirst (fresh data, fallback to cache)
- **Images**: CacheFirst (cached, fallback to network)
- **Static Assets**: Precached during install

### Performance Budgets

Target metrics:
- **First Contentful Paint**: < 1.5s
- **Time to Interactive**: < 3s
- **Bundle Size**: < 250KB gzipped
- **Lighthouse Score**: > 90 (all categories)

## Deployment

### Build

```bash
# Production build
npm run build

# Output in .output/ directory
```

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Production deployment
vercel --prod
```

### Environment Variables (Production)

Set in Vercel dashboard or via CLI:

```bash
vercel env add NUXT_PUBLIC_API_BASE production
vercel env add NUXT_PUBLIC_ENABLE_ANALYTICS production
```

### PWA Icons

Create icons before deployment:

```
public/
└── icons/
    ├── icon-192x192.png
    └── icon-512x512.png
```

## Known Issues & TODOs

### Pending Implementation

- [ ] Replace PDF export placeholder with actual jsPDF or pdfmake
- [ ] Connect all auth endpoints to backend (forgot-password, reset-password, verify-email)
- [ ] Add Google Analytics or Plausible integration (analytics plugin ready)
- [ ] Create actual PWA icon files (192x192, 512x512)

### Backend Integration TODOs

All pages have placeholder API calls marked with `// TODO:` comments. Search for `TODO` to find:

- Password reset endpoints
- Email verification endpoints
- Analysis feedback endpoints
- Export endpoints

Example:
```typescript
// TODO: Call API to verify email
// await $fetch('/auth/verify-email', {
//   method: 'POST',
//   body: { token: token.value },
//   baseURL: useRuntimeConfig().public.apiBase,
// })
```

## Contributing

### Code Style

- **ESLint**: Airbnb style guide with Vue/Nuxt extensions
- **Prettier**: 2 spaces, single quotes, trailing commas
- **TypeScript**: Strict mode, explicit return types preferred

### Commit Messages

Use conventional commits:

```
feat: add password reset flow
fix: resolve SSE connection timeout
docs: update README with i18n setup
style: format with prettier
refactor: extract notification logic to composable
test: add unit tests for auth store
```

### Pull Request Process

1. Create feature branch: `feat/your-feature-name`
2. Make changes with tests
3. Run `npm run lint` and `npm run test`
4. Commit with conventional commits
5. Push and create PR
6. Wait for CI checks to pass

## Architecture Decisions

### Why Nuxt 3?

- File-based routing (pages become routes)
- Auto-imports (components, composables, utils)
- Server-side rendering (SSR) ready
- SEO-friendly
- Built-in TypeScript support
- Large ecosystem

### Why Pinia?

- Official Vue state management (replaces Vuex)
- TypeScript-first
- Composition API support
- DevTools integration
- Lightweight

### Why Tailwind CSS?

- Utility-first (rapid development)
- Consistent design system
- Small bundle size (PurgeCSS)
- Dark mode built-in
- Responsive utilities

### Why PWA?

- Offline support (reliability)
- Installable (engagement)
- Fast load times (caching)
- Mobile-friendly
- Progressive enhancement

## Resources

- [Nuxt 3 Documentation](https://nuxt.com/docs)
- [Vue 3 Documentation](https://vuejs.org/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [VueUse Documentation](https://vueuse.org/)
- [Vitest Documentation](https://vitest.dev/)
- [Playwright Documentation](https://playwright.dev/)

## License

Proprietary - All rights reserved

## Support

For issues or questions, contact the development team.

---

**Last Updated**: November 9, 2025
**Version**: 1.0.0
**Status**: Phase 3 Complete ✅
