import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const darkMode = ref(
    typeof localStorage !== 'undefined' 
      ? localStorage.getItem('theme') === 'dark' 
      : false
  )

  // Watch for changes and update localStorage + document classes
  watch(darkMode, (newValue) => {
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem('theme', newValue ? 'dark' : 'light')
    }

    if (typeof document !== 'undefined') {
      if (newValue) {
        document.documentElement.classList.add('dark')
        document.documentElement.classList.remove('light')
      } else {
        document.documentElement.classList.add('light')
        document.documentElement.classList.remove('dark')
      }
    }
  }, { immediate: true })

  function toggleTheme(): void {
    darkMode.value = !darkMode.value
  }

  return { 
    darkMode, 
    toggleTheme 
  }
})

