<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'

const email = ref('')
const password = ref('')
const error = ref('')

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const themeStore = useThemeStore()

onMounted(() => {
  const errorMsg = route.query.error as string | undefined
  if (errorMsg) {
    error.value = errorMsg
  }
})

async function handleSubmit() {
  try {
    await authStore.login(email.value, password.value)
    router.push('/')
  } catch {
    error.value = 'Login failed. Please try again.'
  }
}
</script>

<template>
  <div
    :class="themeStore.darkMode ? 'bg-dark' : 'bg-gray-100'"
    class="min-h-screen pt-20 flex items-center justify-center px-4 transition-colors duration-300"
  >
    <div
      :class="themeStore.darkMode ? 'bg-gray-800' : 'bg-white'"
      class="max-w-md w-full rounded-lg shadow-lg p-8 transition-colors duration-300"
    >
      <h2
        :class="themeStore.darkMode ? 'text-light' : 'text-gray-800'"
        class="text-3xl font-bold mb-6 transition-colors duration-300"
      >
        Login
      </h2>

      <div
        v-if="error"
        class="bg-red-500/10 border border-red-500 text-red-500 rounded-md p-3 mb-4"
        v-html="error"
      />

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div>
          <label
            for="email"
            :class="themeStore.darkMode ? 'text-light' : 'text-gray-700'"
            class="block mb-2 transition-colors duration-300"
          >
            Email Address
          </label>
          <input
            id="email"
            v-model="email"
            type="email"
            :class="themeStore.darkMode ? 'bg-gray-700 text-light' : 'bg-gray-100 text-gray-800'"
            class="w-full rounded px-3 py-2 transition-colors duration-300"
            required
            autofocus
          />
        </div>

        <div>
          <label
            for="password"
            :class="themeStore.darkMode ? 'text-light' : 'text-gray-700'"
            class="block mb-2 transition-colors duration-300"
          >
            Password
          </label>
          <input
            id="password"
            v-model="password"
            type="password"
            :class="themeStore.darkMode ? 'bg-gray-700 text-light' : 'bg-gray-100 text-gray-800'"
            class="w-full rounded px-3 py-2 transition-colors duration-300"
            required
          />
        </div>

        <button
          type="submit"
          class="w-full bg-primary hover:bg-accent text-white py-2 px-4 rounded transition-colors"
        >
          Login
        </button>
      </form>
    </div>
  </div>
</template>

