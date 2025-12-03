<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'

const authStore = useAuthStore()
const themeStore = useThemeStore()
const adminMenuOpen = ref(false)
</script>

<template>
  <nav
    :class="themeStore.darkMode ? 'bg-dark/95' : 'bg-white/95'"
    class="backdrop-blur-sm fixed w-full z-50 shadow-md transition-colors duration-300"
  >
    <div class="max-w-7xl mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <div class="flex-shrink-0 flex items-center">
          <RouterLink to="/" class="flex items-center">
            <img src="/copilot.png" alt="Copilot icon" class="h-8 w-auto" />
            <div class="ml-2">
              <span :class="themeStore.darkMode ? 'text-light' : 'text-gray-800'" class="text-xl font-bold">
                OctoCAT Supply
              </span>
              <span class="block text-xs text-primary">Smart Cat Tech, Powered by AI</span>
            </div>
          </RouterLink>
        </div>
        <div class="hidden md:block">
          <div class="ml-10 flex items-baseline space-x-4">
            <RouterLink
              to="/"
              :class="themeStore.darkMode ? 'text-light hover:text-primary' : 'text-gray-700 hover:text-primary'"
              class="px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Home
            </RouterLink>
            <RouterLink
              to="/products"
              :class="themeStore.darkMode ? 'text-light hover:text-primary' : 'text-gray-700 hover:text-primary'"
              class="px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Products
            </RouterLink>
            <RouterLink
              to="/about"
              :class="themeStore.darkMode ? 'text-light hover:text-primary' : 'text-gray-700 hover:text-primary'"
              class="px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              About us
            </RouterLink>
            <div v-if="authStore.isAdmin" class="relative">
              <button
                @click="adminMenuOpen = !adminMenuOpen"
                :class="themeStore.darkMode ? 'text-light hover:text-primary' : 'text-gray-700 hover:text-primary'"
                class="px-3 py-2 rounded-md text-sm font-medium flex items-center transition-colors"
              >
                Admin
                <svg
                  :class="adminMenuOpen ? 'rotate-180' : ''"
                  class="ml-1 h-4 w-4 transform transition-transform"
                  fill="none"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path d="M19 9l-7 7-7-7"></path>
                </svg>
              </button>
              <div
                v-if="adminMenuOpen"
                :class="themeStore.darkMode ? 'bg-dark' : 'bg-white'"
                class="absolute right-0 mt-2 w-48 rounded-md shadow-lg ring-1 ring-black ring-opacity-5 transition-colors"
              >
                <div class="py-1">
                  <RouterLink
                    to="/admin/products"
                    :class="themeStore.darkMode ? 'text-light hover:bg-primary hover:text-white' : 'text-gray-700 hover:bg-primary hover:text-white'"
                    class="block px-4 py-2 text-sm transition-colors"
                    @click="adminMenuOpen = false"
                  >
                    Manage Products
                  </RouterLink>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="flex items-center space-x-4">
          <button
            @click="themeStore.toggleTheme()"
            class="p-2 rounded-full focus:outline-none transition-colors"
            aria-label="Toggle dark/light mode"
          >
            <svg
              v-if="themeStore.darkMode"
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5 text-yellow-300"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z"
                clip-rule="evenodd"
              />
            </svg>
            <svg
              v-else
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5 text-gray-700"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
            </svg>
          </button>
          <template v-if="authStore.isLoggedIn">
            <span
              :class="themeStore.darkMode ? 'text-light' : 'text-gray-700'"
              class="text-sm transition-colors"
            >
              <span v-if="authStore.isAdmin" class="text-primary">(Admin) </span>
              Welcome!
            </span>
            <button
              @click="authStore.logout()"
              :class="themeStore.darkMode ? 'text-light hover:text-primary' : 'text-gray-700 hover:text-primary'"
              class="px-3 py-2 rounded-md text-sm font-medium transition-colors"
            >
              Logout
            </button>
          </template>
          <RouterLink
            v-else
            to="/login"
            class="bg-primary hover:bg-accent text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
          >
            Login
          </RouterLink>
        </div>
      </div>
    </div>
  </nav>
</template>

