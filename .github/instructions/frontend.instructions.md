---
description: "Guidance for editing and reviewing frontend code changes in the Vue 3 + Vite + Tailwind stack."
applyTo: "frontend/src/**, frontend/index.html, frontend/vite.config.ts, frontend/tailwind.config.js"
---
# Frontend Review Guidance
Focus on UX quality, accessibility, performance, and maintainability of the Vue 3 + Vite + Tailwind stack.

## Key Principles
- Accessibility first: semantic HTML, proper labels, ARIA only when semantics insufficient, maintain focus order.
- State management: Prefer TanStack Vue Query for server cache; use Pinia for global client state; keep local UI state local with `ref()` and `reactive()`.
- Performance: Split lazy routes/components, avoid large bundle additions, prefer dynamic import for rarely used views.
- Styling: Tailwind utility classes preferred; abstract repeated class groups into small components rather than custom CSS.
- Types: Avoid `any`; type API responses with shared DTO types; use TypeScript with `<script setup lang="ts">`.

## Review Checklist
1. Data fetching uses TanStack Vue Query (`useQuery`, `useMutation`) with proper error handling and loading states, not ad-hoc `onMounted` + `axios`.
2. Components remain small & focused (< ~150 LOC). Suggest extraction when crossing concerns (data + complex layout + formatting).
3. Responsive: verify critical views at mobile (≤640px), md (~768px), lg (≥1024px).
4. Form inputs: keyboard accessible, visible focus ring, validation feedback with text, not only color. Use `v-model` for two-way binding.
5. Images: optimized (correct size, `alt` text), avoid layout shift (width/height or aspect-ratio set).
6. Routing: use Vue Router 4 patterns with lazy-loaded route components.
7. Security: never use `v-html` with untrusted content; sanitize if unavoidable.

## Vue 3 Composition API Patterns
- Use `<script setup lang="ts">` for all components
- Define props with `defineProps<{}>()` and emits with `defineEmits<{}>()`
- Use `ref()` for primitive reactive values, `reactive()` for objects
- Use `computed()` for derived state
- Use `watch()` or `watchEffect()` for side effects
- Access stores with `useStore()` pattern from Pinia

## Testing Guidance
- Encourage Vue Test Utils tests for complex logic (conditional rendering, form validation, composables).
- Snapshot tests only for stable presentational components.

## Performance Flags
- Re-render hotspots (large lists) should use `v-memo` or virtual scrolling when count > ~200.
- Avoid anonymous inline functions in `v-for` loops where measurable.

## Anti-Patterns to Nudge
- Overuse of Pinia for simple prop passing (prefer props/emits).
- Mixing data fetching + presentational markup in one large component.
- Custom CSS files duplicating Tailwind utilities.
- Using Options API instead of Composition API.

## Example Feedback Style
"Consider extracting the price formatting into a `formatCurrency()` utility because it's duplicated in ProductCard and OrderSummary and risks divergence."
