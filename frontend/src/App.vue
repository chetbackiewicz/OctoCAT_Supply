<script setup lang="ts">
import { useThemeStore } from '@/stores/theme'
import Navigation from '@/components/Navigation.vue'
import Footer from '@/components/Footer.vue'

const themeStore = useThemeStore()
</script>

<template>
  <div 
    class="flex flex-col min-h-screen transition-colors duration-300"
    :class="themeStore.darkMode ? 'bg-dark' : 'bg-gray-100'"
  >
    <Navigation />
    <main class="flex-grow">
      <RouterView />
    </main>
    <Footer />
  </div>
</template>

