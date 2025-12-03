/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

// Runtime config type definition
declare global {
  interface Window {
    RUNTIME_CONFIG?: {
      API_URL: string;
    };
  }
}

export {}

