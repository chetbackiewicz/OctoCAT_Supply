<script setup lang="ts">
import { ref, computed } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import axios from 'axios'
import { api } from '@/api/config'
import { useThemeStore } from '@/stores/theme'

interface Product {
  productId: number
  name: string
  description: string
  price: number
  imgName: string
  sku: string
  unit: string
  supplierId: number
  discount?: number
}

const themeStore = useThemeStore()
const quantities = ref<Record<number, number>>({})
const searchTerm = ref('')
const selectedProduct = ref<Product | null>(null)
const showModal = ref(false)

const fetchProducts = async (): Promise<Product[]> => {
  const { data } = await axios.get(`${api.baseURL}${api.endpoints.products}`)
  return data
}

const { data: products, isLoading, error } = useQuery({
  queryKey: ['products'],
  queryFn: fetchProducts
})

const filteredProducts = computed(() => {
  if (!products.value) return []
  return products.value.filter(
    (product) =>
      product.name.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
      product.description.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
})

function handleQuantityChange(productId: number, change: number) {
  quantities.value = {
    ...quantities.value,
    [productId]: Math.max(0, (quantities.value[productId] || 0) + change)
  }
}

function handleAddToCart(productId: number) {
  const quantity = quantities.value[productId] || 0
  if (quantity > 0) {
    // TODO: Implement cart functionality
    alert(`Added ${quantity} items to cart`)
    quantities.value = {
      ...quantities.value,
      [productId]: 0
    }
  }
}

function handleProductClick(product: Product) {
  selectedProduct.value = product
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  selectedProduct.value = null
}

function hasDiscount(product: Product): boolean {
  return product.discount != null && product.discount > 0
}

function getDiscountedPrice(product: Product): number {
  return product.price * (1 - (product.discount || 0))
}
</script>

<template>
  <!-- Loading State -->
  <div
    v-if="isLoading"
    :class="themeStore.darkMode ? 'bg-dark' : 'bg-gray-100'"
    class="min-h-screen pt-20 px-4 transition-colors duration-300"
  >
    <div class="max-w-7xl mx-auto">
      <div class="flex justify-center items-center h-64">
        <div class="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-primary"></div>
      </div>
    </div>
  </div>

  <!-- Error State -->
  <div
    v-else-if="error"
    :class="themeStore.darkMode ? 'bg-dark' : 'bg-gray-100'"
    class="min-h-screen pt-20 px-4 transition-colors duration-300"
  >
    <div class="max-w-7xl mx-auto">
      <div class="text-red-500 text-center">Failed to fetch products</div>
    </div>
  </div>

  <!-- Products List -->
  <div
    v-else
    :class="themeStore.darkMode ? 'bg-dark' : 'bg-gray-100'"
    class="min-h-screen pt-20 pb-16 px-4 transition-colors duration-300"
  >
    <div class="max-w-7xl mx-auto">
      <div class="flex flex-col space-y-6">
        <h1
          :class="themeStore.darkMode ? 'text-light' : 'text-gray-800'"
          class="text-3xl font-bold transition-colors duration-300"
        >
          Products
        </h1>

        <div class="relative">
          <input
            v-model="searchTerm"
            type="text"
            placeholder="Search products..."
            :class="themeStore.darkMode ? 'bg-gray-800 text-light border-gray-700' : 'bg-white text-gray-800 border-gray-300'"
            class="w-full px-4 py-2 rounded-lg border focus:border-primary focus:ring-1 focus:ring-primary focus:outline-none transition-colors duration-300"
            aria-label="Search products"
          />
          <svg
            :class="themeStore.darkMode ? 'text-gray-400' : 'text-gray-500'"
            class="absolute right-3 top-1/2 transform -translate-y-1/2 h-5 w-5 transition-colors duration-300"
            fill="none"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
        </div>

        <!-- Empty state when no products match -->
        <div
          v-if="filteredProducts.length === 0"
          :class="[
            themeStore.darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'
          ]"
          class="flex flex-col items-center justify-center text-center py-20 rounded-lg shadow-sm border"
          role="status"
          aria-live="polite"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            :class="themeStore.darkMode ? 'text-gray-400' : 'text-gray-500'"
            class="h-12 w-12 mb-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h7l2 3h9v13a2 2 0 01-2 2H5a2 2 0 01-2-2V3zm3 7h12" />
          </svg>
          <p :class="themeStore.darkMode ? 'text-light' : 'text-gray-800'" class="text-lg font-medium">
            No products found
          </p>
          <p v-if="searchTerm" :class="themeStore.darkMode ? 'text-gray-400' : 'text-gray-600'" class="mt-2">
            Try clearing or changing your search filters.
          </p>
        </div>

        <!-- Product Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          <div
            v-for="product in filteredProducts"
            :key="product.productId"
            :class="themeStore.darkMode ? 'bg-gray-800' : 'bg-white'"
            class="rounded-lg overflow-hidden shadow-lg transform transition-all duration-300 hover:scale-105 hover:shadow-[0_0_25px_rgba(118,184,82,0.3)] flex flex-col"
          >
            <div
              :class="themeStore.darkMode ? 'bg-gradient-to-t from-gray-700 to-gray-800' : 'bg-gradient-to-t from-gray-100 to-white'"
              class="relative h-56 transition-colors duration-300 cursor-pointer"
              @click="handleProductClick(product)"
            >
              <img
                :src="`/${product.imgName}`"
                :alt="product.name"
                class="w-full h-full object-contain p-2"
              />
              <div
                v-if="hasDiscount(product)"
                class="absolute top-8 left-0 bg-primary text-white px-3 py-1 -rotate-90 transform -translate-x-5 shadow-md"
              >
                {{ Math.round(product.discount! * 100) }}% OFF
              </div>
            </div>

            <div class="p-4 flex flex-col flex-grow">
              <h3
                :class="themeStore.darkMode ? 'text-light' : 'text-gray-800'"
                class="text-xl font-semibold mb-2 transition-colors duration-300"
              >
                {{ product.name }}
              </h3>
              <p
                :class="themeStore.darkMode ? 'text-gray-400' : 'text-gray-600'"
                class="mb-4 flex-grow transition-colors duration-300"
              >
                {{ product.description }}
              </p>
              <div class="space-y-4 mt-auto">
                <div class="flex justify-between items-center">
                  <template v-if="hasDiscount(product)">
                    <div>
                      <span class="text-gray-500 line-through text-sm mr-2">
                        ${{ product.price.toFixed(2) }}
                      </span>
                      <span class="text-primary text-xl font-bold">
                        ${{ getDiscountedPrice(product).toFixed(2) }}
                      </span>
                    </div>
                  </template>
                  <span v-else class="text-primary text-xl font-bold">
                    ${{ product.price.toFixed(2) }}
                  </span>
                </div>

                <div class="flex items-center justify-between">
                  <div
                    :class="themeStore.darkMode ? 'bg-gray-700' : 'bg-gray-200'"
                    class="flex items-center space-x-3 rounded-lg p-1 transition-colors duration-300"
                  >
                    <button
                      @click="handleQuantityChange(product.productId, -1)"
                      :class="themeStore.darkMode ? 'text-light' : 'text-gray-700'"
                      class="w-8 h-8 flex items-center justify-center hover:text-primary transition-colors duration-300"
                      :aria-label="`Decrease quantity of ${product.name}`"
                      :id="`decrease-qty-${product.productId}`"
                    >
                      <span aria-hidden="true">-</span>
                    </button>
                    <span
                      :class="themeStore.darkMode ? 'text-light' : 'text-gray-800'"
                      class="min-w-[2rem] text-center transition-colors duration-300"
                      :aria-label="`Quantity of ${product.name}`"
                      :id="`qty-${product.productId}`"
                    >
                      {{ quantities[product.productId] || 0 }}
                    </span>
                    <button
                      @click="handleQuantityChange(product.productId, 1)"
                      :class="themeStore.darkMode ? 'text-light' : 'text-gray-700'"
                      class="w-8 h-8 flex items-center justify-center hover:text-primary transition-colors duration-300"
                      :aria-label="`Increase quantity of ${product.name}`"
                      :id="`increase-qty-${product.productId}`"
                    >
                      <span aria-hidden="true">+</span>
                    </button>
                  </div>
                  <button
                    @click="handleAddToCart(product.productId)"
                    :class="[
                      quantities[product.productId]
                        ? 'bg-primary hover:bg-accent text-white'
                        : themeStore.darkMode
                          ? 'bg-gray-700 text-gray-400 cursor-not-allowed'
                          : 'bg-gray-200 text-gray-500 cursor-not-allowed'
                    ]"
                    class="px-4 py-2 rounded-lg transition-colors"
                    :disabled="!quantities[product.productId]"
                    :aria-label="`Add ${quantities[product.productId] || 0} ${product.name} to cart`"
                    :id="`add-to-cart-${product.productId}`"
                  >
                    Add to Cart
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Product Modal -->
    <div
      v-if="showModal && selectedProduct"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      @click="closeModal"
    >
      <div
        :class="themeStore.darkMode ? 'bg-gray-800' : 'bg-white'"
        class="rounded-lg p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-xl transition-colors duration-300"
        @click.stop
      >
        <div class="flex justify-end">
          <button
            @click="closeModal"
            :class="themeStore.darkMode ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-black'"
            class="transition-colors duration-300"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
        <div
          :class="themeStore.darkMode ? 'bg-gradient-to-t from-gray-700 to-gray-800' : 'bg-gradient-to-t from-gray-100 to-white'"
          class="rounded-lg mb-6 p-4"
        >
          <img
            :src="`/${selectedProduct.imgName}`"
            :alt="selectedProduct.name"
            class="w-full h-auto object-contain max-h-[400px]"
          />
        </div>
        <h2
          :class="themeStore.darkMode ? 'text-light' : 'text-gray-800'"
          class="text-2xl font-bold mb-4 transition-colors duration-300"
        >
          {{ selectedProduct.name }}
        </h2>
        <p
          :class="themeStore.darkMode ? 'text-gray-300' : 'text-gray-600'"
          class="text-lg transition-colors duration-300"
        >
          {{ selectedProduct.description }}
        </p>
      </div>
    </div>
  </div>
</template>

