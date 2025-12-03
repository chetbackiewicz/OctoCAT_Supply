# Vue 3 + TypeScript + Vite

This is the OctoCAT Supply frontend built with Vue 3, TypeScript, and Vite.

## Tech Stack

- **Vue 3** with Composition API (`<script setup>`)
- **TypeScript** for type safety
- **Vite** for fast development and building
- **Pinia** for state management
- **Vue Router** for client-side routing
- **TanStack Vue Query** for server state management
- **Tailwind CSS** for styling
- **Swiper** for carousels

## Project Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## ESLint Configuration

The project uses ESLint with Vue-specific rules. For production applications, you can enhance the configuration:

```js
// eslint.config.js
import pluginVue from 'eslint-plugin-vue'
import vueTsEslintConfig from '@vue/eslint-config-typescript'

export default [
  ...pluginVue.configs['flat/recommended'],
  ...vueTsEslintConfig(),
  {
    rules: {
      'vue/multi-word-component-names': 'off',
      'vue/no-v-html': 'warn',
    }
  }
]
```

## Directory Structure

```
src/
├── api/           # API configuration
├── components/    # Vue components
├── router/        # Vue Router configuration
├── stores/        # Pinia stores
├── App.vue        # Root component
├── main.ts        # Application entry point
└── index.css      # Global styles
```
