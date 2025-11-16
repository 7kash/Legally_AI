# Frontend Redesign Plan - Contract Analysis Display

## Problem Analysis

### Current Issues:
1. **Titles not displaying** - Despite backend sending `{title, content}` structure
2. **Code complexity** - Switching between AnalysisSection (too generic) and manual WidgetCards (too verbose)
3. **Feature loss** - Each refactor loses ELI5, quotes, or other features
4. **Poor maintainability** - 600+ lines of repetitive code in [id].vue
5. **No proper component architecture** - Everything in one massive file

### Backend Data Structure (VERIFIED):
```python
formatted_output = {
    "agreement_type": {
        "title": "Agreement Type",
        "content": "Service Agreement"
    },
    "parties": {
        "title": "Parties",
        "content": [
            {"name": "Company A", "role": "Service Provider"},
            {"name": "Company B", "role": "Client"}
        ]
    },
    "obligations": {
        "title": "Your Obligations",
        "content": [
            {
                "action": "Pay monthly fee",
                "time_window": "Within 30 days",
                "consequence": "Service termination",
                "quote": "Monthly fee shall be paid...",
                "action_simple": "Pay the bill each month"  // ELI5 version
            }
        ]
    },
    "rights": {"title": "Your Rights", "content": [...]},
    "risks": {"title": "Risks & Concerns", "content": [...]},
    "payment_terms": {"title": "Payment Terms", "content": {...}},
    "calendar": {"title": "Key Dates & Deadlines", "content": [...]},
    "mitigations": {"title": "Risk Mitigations", "content": [...]}
}
```

---

## Proposed Solution: Component-Based Architecture

### Strategy: Specialized Widget Components

Instead of:
- ❌ Generic `AnalysisSection` (loses features)
- ❌ Manual repetitive `WidgetCard` sections (unmaintainable)

Use:
- ✅ **Specialized widget components** for each data type
- ✅ **Registry pattern** to map keys to components
- ✅ **Composition** to keep all features (ELI5, quotes, feedback)

---

## New Architecture

### 1. Widget Component Hierarchy

```
frontend/components/analysis/widgets/
├── BaseWidget.vue           # Wrapper with title, icon, color
├── SimpleTextWidget.vue     # For agreement_type, jurisdiction
├── PartiesWidget.vue        # For parties list
├── ObligationsWidget.vue    # Complex: ELI5, quotes, feedback
├── RightsWidget.vue         # Complex: ELI5, quotes, feedback
├── RisksWidget.vue          # Complex: ELI5, quotes, risk levels
├── PaymentTermsWidget.vue   # Structured payment data
├── CalendarWidget.vue       # Date/event list
├── MitigationsWidget.vue    # Mitigation actions + quotes
└── index.ts                 # Widget registry
```

### 2. Widget Registry Pattern

**File: `components/analysis/widgets/index.ts`**
```typescript
import SimpleTextWidget from './SimpleTextWidget.vue'
import PartiesWidget from './PartiesWidget.vue'
import ObligationsWidget from './ObligationsWidget.vue'
// ... other imports

export const WIDGET_REGISTRY = {
  agreement_type: {
    component: SimpleTextWidget,
    icon: 'document',
    color: undefined
  },
  parties: {
    component: PartiesWidget,
    icon: 'users',
    color: undefined
  },
  obligations: {
    component: ObligationsWidget,
    icon: 'clipboard',
    color: 'blue'
  },
  rights: {
    component: RightsWidget,
    icon: 'shield',
    color: 'green'
  },
  risks: {
    component: RisksWidget,
    icon: 'warning',
    color: 'red'
  },
  payment_terms: {
    component: PaymentTermsWidget,
    icon: 'currency',
    color: 'emerald'
  },
  calendar: {
    component: CalendarWidget,
    icon: 'calendar',
    color: 'purple'
  },
  mitigations: {
    component: MitigationsWidget,
    icon: 'shield-check',
    color: 'amber'
  },
  jurisdiction: {
    component: SimpleTextWidget,
    icon: 'globe',
    color: undefined
  }
}
```

### 3. Main Analysis Page (Simplified)

**File: `pages/analysis/[id].vue`** (Reduced from 1200 to ~200 lines)
```vue
<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8">
    <div class="container-custom max-w-4xl">
      <!-- Header, Loading, Error states... -->
      
      <div v-else-if="analysesStore.hasResults" class="space-y-6">
        <!-- ELI5 Toggle -->
        <ELI5Toggle v-model="eli5Enabled" :loading="eli5Loading" @toggle="handleELI5Toggle" />
        
        <!-- Important Limits & Screening Badge -->
        <ImportantLimits />
        <ScreeningBadge :variant="screeningResult" />
        <ConfidenceLevel :score="confidenceScore" :reason="confidenceReason" />
        <AboutSection :summary="aboutSummary" />
        
        <!-- Dynamic Widget Rendering -->
        <component
          v-for="(section, key) in orderedSections"
          :key="key"
          :is="getWidgetComponent(key)"
          :title="section.title"
          :content="section.content"
          :section-key="key"
          :eli5-enabled="eli5Enabled"
          :eli5-data="eli5Data"
          @feedback="handleFeedback"
        />
        
        <!-- Actions -->
        <AnalysisActions @export="handleExport" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { WIDGET_REGISTRY } from '~/components/analysis/widgets'

const orderedSections = computed(() => {
  const output = formattedOutput.value
  const order = ['agreement_type', 'parties', 'jurisdiction', 'obligations', 
                 'rights', 'payment_terms', 'calendar', 'risks', 'mitigations']
  
  return order
    .filter(key => output[key] && hasContent(output[key]))
    .reduce((acc, key) => ({ ...acc, [key]: output[key] }), {})
})

function getWidgetComponent(key: string) {
  return WIDGET_REGISTRY[key]?.component || SimpleTextWidget
}
</script>
```

### 4. Example Widget: ObligationsWidget.vue

```vue
<template>
  <BaseWidget :title="title" icon="clipboard" color="blue">
    <div class="space-y-4">
      <div
        v-for="(item, index) in content"
        :key="index"
        class="border-l-4 border-blue-500 pl-4 py-3 bg-blue-50 rounded-r-lg"
      >
        <!-- ELI5 Mode -->
        <p v-if="eli5Enabled && item.action_simple" class="text-gray-800 leading-relaxed">
          {{ item.action_simple }}
        </p>
        
        <!-- Normal Mode -->
        <template v-else>
          <p class="font-semibold text-gray-900">{{ item.action }}</p>
          <div v-if="item.time_window || item.trigger" class="mt-2 space-y-1">
            <p v-if="item.trigger" class="text-sm text-gray-700">
              <span class="font-medium">When:</span> {{ item.trigger }}
            </p>
            <p v-if="item.time_window" class="text-sm text-gray-700">
              <span class="font-medium">Deadline:</span> {{ item.time_window }}
            </p>
          </div>
          <p v-if="item.consequence" class="mt-2 text-sm text-red-700 bg-red-50 p-2 rounded">
            <span class="font-medium">⚠️ If not done:</span> {{ item.consequence }}
          </p>
        </template>
        
        <!-- Quote Toggle -->
        <QuoteToggle :quote="item.quote" :quote-translated="item.quote_translated" />
      </div>
    </div>
  </BaseWidget>
</template>

<script setup lang="ts">
interface Props {
  title: string
  content: any[]
  sectionKey: string
  eli5Enabled?: boolean
  eli5Data?: any
}

defineProps<Props>()
</script>
```

### 5. Reusable Components

**BaseWidget.vue** - Title, icon, color wrapper
**QuoteToggle.vue** - "Tell me more" / "Not found" logic
**ELI5Toggle.vue** - Toggle button + banner
**FeedbackButtons.vue** - Thumbs up/down for sections

---

## Implementation Plan

### Phase 1: Foundation (Day 1 - 2 hours)
1. ✅ Create `components/analysis/widgets/` directory
2. ✅ Build `BaseWidget.vue` (title, icon, color props)
3. ✅ Build `QuoteToggle.vue` (reusable quote display)
4. ✅ Build `ELI5Toggle.vue` (toggle button + banner)
5. ✅ Create widget registry `index.ts`

### Phase 2: Simple Widgets (Day 1 - 1 hour)
6. ✅ `SimpleTextWidget.vue` (agreement_type, jurisdiction)
7. ✅ `PartiesWidget.vue` (parties list)
8. ✅ `PaymentTermsWidget.vue` (payment data)
9. ✅ `CalendarWidget.vue` (dates/events)

### Phase 3: Complex Widgets (Day 1 - 2 hours)
10. ✅ `ObligationsWidget.vue` (ELI5 + quotes + feedback)
11. ✅ `RightsWidget.vue` (ELI5 + quotes + feedback)
12. ✅ `RisksWidget.vue` (risk levels + ELI5 + quotes)
13. ✅ `MitigationsWidget.vue` (quotes + related risks)

### Phase 4: Page Refactor (Day 1 - 1 hour)
14. ✅ Simplify `pages/analysis/[id].vue`
15. ✅ Use registry to render widgets dynamically
16. ✅ Clean up old code
17. ✅ Test all features work

### Phase 5: Polish (Day 2 - 1 hour)
18. ✅ Add loading skeletons
19. ✅ Improve transitions
20. ✅ Mobile responsiveness
21. ✅ Accessibility (ARIA labels)

---

## Benefits

### ✅ Maintainability
- Each widget is self-contained (50-100 lines vs 1200)
- Easy to modify one widget without breaking others
- Clear separation of concerns

### ✅ Reusability
- QuoteToggle used across 4 widgets
- BaseWidget provides consistent styling
- Easy to add new widget types

### ✅ Feature Preservation
- ELI5 mode built into complex widgets
- Quote functionality in QuoteToggle component
- Feedback buttons where needed
- All existing features retained

### ✅ Type Safety
- TypeScript interfaces for each widget
- Props validation
- Better IDE support

### ✅ Testing
- Each widget can be tested independently
- Storybook-ready
- Unit tests easier to write

### ✅ Performance
- Vue's reactivity optimized per widget
- Lazy loading possible
- Better change detection

---

## Technical Decisions

### Why Not Use a UI Library?

**Current Stack**: Nuxt 3 + Vue 3 + Tailwind CSS

**Considered Libraries**:
1. **Headless UI** (Tailwind team)
   - ✅ Unstyled, fully accessible
   - ❌ Doesn't help with our specific widget needs
   
2. **PrimeVue**
   - ✅ Rich component set
   - ❌ Heavy, opinionated styling conflicts with Tailwind
   
3. **Vuetify**
   - ✅ Material Design
   - ❌ Material Design != our design, bundle size
   
4. **Naive UI**
   - ✅ Modern, TypeScript
   - ❌ Learning curve, different design system

**Decision**: **Stick with Tailwind CSS + Custom Components**
- Already integrated
- Full design control
- Lightweight
- Team knows it
- Our widgets are domain-specific (legal contracts)

### Component Library Choice

We'll create our own **internal component library**:
- `components/analysis/widgets/` - Domain widgets
- `components/ui/` - Generic reusable UI (if needed)
- Focus on composition over library dependencies

---

## Migration Strategy

### Backward Compatibility
- Keep old components during transition
- Feature flag for new architecture
- Gradual rollout

### Rollback Plan
- Git branch for new architecture
- Old code commented, not deleted
- Easy revert if issues found

---

## Success Criteria

✅ All titles display correctly  
✅ ELI5 mode works for obligations, rights, risks  
✅ Quote toggles work ("Tell me more" / "Not found")  
✅ Screening badge displays  
✅ Confidence level shows actual score  
✅ Important limits disclaimer shows  
✅ Code reduced from 1200 to ~400 lines  
✅ Each widget < 150 lines  
✅ All features from current version work  
✅ Mobile responsive  
✅ Accessible (keyboard nav, screen readers)  

---

## Next Steps

1. **Review this plan** with team
2. **Create feature branch**: `feature/widget-architecture`
3. **Implement Phase 1-2** (foundation + simple widgets)
4. **Demo** simple widgets working
5. **Get approval** to continue
6. **Complete Phase 3-4** (complex widgets + page refactor)
7. **QA testing**
8. **Merge to main**

---

**Estimated Time**: 6-8 hours development + 2 hours testing = **1-2 days**

**Risk Level**: Low (can rollback, feature flag)

**Impact**: High (maintainability, reliability, performance)
