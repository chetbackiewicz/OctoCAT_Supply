import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const isLoggedIn = ref(false)
  const userEmail = ref('')

  const isAdmin = computed(() => userEmail.value.endsWith('@github.com'))

  async function login(email: string, password: string): Promise<void> {
    // In a real app, you would validate credentials with an API
    // For now, we'll just check the email domain
    if (email && password) {
      isLoggedIn.value = true
      userEmail.value = email
    }
  }

  function logout(): void {
    isLoggedIn.value = false
    userEmail.value = ''
  }

  return { 
    isLoggedIn, 
    isAdmin, 
    userEmail,
    login, 
    logout 
  }
})

