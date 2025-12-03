<script setup lang="ts">
import { ref, watch } from 'vue'
import axios from 'axios'
import { api } from '@/api/config'
import { useThemeStore } from '@/stores/theme'

interface Supplier {
  supplierId: number
  name: string
}

interface Product {
  productId: number
  supplierId: number
  name: string
  description: string
  price: number
  sku: string
  unit: string
  imgName: string
  discount?: number
}

const props = defineProps<{
  product?: Product
  suppliers: Supplier[]
}>()

const emit = defineEmits<{
  close: []
  save: []
}>()

const themeStore = useThemeStore()

const formData = ref<Partial<Product>>({
  name: '',
  description: '',
  price: 0,
  sku: '',
  unit: '',
  supplierId: props.suppliers[0]?.supplierId || 0,
  imgName: '',
  discount: undefined
})

// Initialize form data when product prop changes
watch(() => props.product, (newProduct) => {
  if (newProduct) {
    formData.value = { ...newProduct }
  } else {
    formData.value = {
      name: '',
      description: '',
      price: 0,
      sku: '',
      unit: '',
      supplierId: props.suppliers[0]?.supplierId || 0,
      imgName: '',
      discount: undefined
    }
  }
}, { immediate: true })

async function handleSubmit() {
  try {
    if (props.product) {
      await axios.put(`${api.baseURL}${api.endpoints.products}/${props.product.productId}`, formData.value)
    } else {
      await axios.post(`${api.baseURL}${api.endpoints.products}`, formData.value)
    }
    emit('save')
    emit('close')
  } catch (error) {
    console.error('Error saving product:', error)
  }
}

function handleDiscountChange(event: Event) {
  const target = event.target as HTMLInputElement
  const value = target.value === '' ? undefined : parseFloat(target.value) / 100
  formData.value.discount = value
}

function getDiscountDisplayValue(): string | number {
  return formData.value.discount !== undefined ? formData.value.discount * 100 : ''
}
</script>

<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
    <div
      :class="themeStore.darkMode ? 'bg-gray-800' : 'bg-white'"
      class="rounded-lg p-6 w-full max-w-md shadow-xl transition-colors duration-300"
    >
      <h2
        :class="themeStore.darkMode ? 'text-light' : 'text-gray-800'"
        class="text-2xl font-bold mb-4 transition-colors duration-300"
      >
        {{ product ? 'Edit Product' : 'Add New Product' }}
      </h2>
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label
            :class="themeStore.darkMode ? 'text-light' : 'text-gray-700'"
            class="block mb-1 transition-colors duration-300"
          >
            Name
          </label>
          <input
            v-model="formData.name"
            type="text"
            :class="themeStore.darkMode ? 'bg-gray-700 text-light' : 'bg-gray-100 text-gray-800'"
            class="w-full px-3 py-2 rounded transition-colors duration-300"
            required
          />
        </div>
        <div>
          <label
            :class="themeStore.darkMode ? 'text-light' : 'text-gray-700'"
            class="block mb-1 transition-colors duration-300"
          >
            Description
          </label>
          <textarea
            v-model="formData.description"
            :class="themeStore.darkMode ? 'bg-gray-700 text-light' : 'bg-gray-100 text-gray-800'"
            class="w-full px-3 py-2 rounded transition-colors duration-300"
            required
          />
        </div>
        <div>
          <label
            :class="themeStore.darkMode ? 'text-light' : 'text-gray-700'"
            class="block mb-1 transition-colors duration-300"
          >
            Price
          </label>
          <input
            v-model.number="formData.price"
            type="number"
            :class="themeStore.darkMode ? 'bg-gray-700 text-light' : 'bg-gray-100 text-gray-800'"
            class="w-full px-3 py-2 rounded transition-colors duration-300"
            required
            min="0"
            step="0.01"
          />
        </div>
        <div>
          <label
            :class="themeStore.darkMode ? 'text-light' : 'text-gray-700'"
            class="block mb-1 transition-colors duration-300"
          >
            SKU
          </label>
          <input
            v-model="formData.sku"
            type="text"
            :class="themeStore.darkMode ? 'bg-gray-700 text-light' : 'bg-gray-100 text-gray-800'"
            class="w-full px-3 py-2 rounded transition-colors duration-300"
            required
          />
        </div>
        <div>
          <label
            :class="themeStore.darkMode ? 'text-light' : 'text-gray-700'"
            class="block mb-1 transition-colors duration-300"
          >
            Unit
          </label>
          <input
            v-model="formData.unit"
            type="text"
            :class="themeStore.darkMode ? 'bg-gray-700 text-light' : 'bg-gray-100 text-gray-800'"
            class="w-full px-3 py-2 rounded transition-colors duration-300"
            required
          />
        </div>
        <div>
          <label
            :class="themeStore.darkMode ? 'text-light' : 'text-gray-700'"
            class="block mb-1 transition-colors duration-300"
          >
            Image Name
          </label>
          <input
            v-model="formData.imgName"
            type="text"
            :class="themeStore.darkMode ? 'bg-gray-700 text-light' : 'bg-gray-100 text-gray-800'"
            class="w-full px-3 py-2 rounded transition-colors duration-300"
            required
          />
        </div>
        <div>
          <label
            :class="themeStore.darkMode ? 'text-light' : 'text-gray-700'"
            class="block mb-1 transition-colors duration-300"
          >
            Supplier
          </label>
          <select
            v-model.number="formData.supplierId"
            :class="themeStore.darkMode ? 'bg-gray-700 text-light' : 'bg-gray-100 text-gray-800'"
            class="w-full px-3 py-2 rounded transition-colors duration-300"
            required
          >
            <option
              v-for="supplier in suppliers"
              :key="supplier.supplierId"
              :value="supplier.supplierId"
            >
              {{ supplier.name }}
            </option>
          </select>
        </div>
        <div>
          <label
            :class="themeStore.darkMode ? 'text-light' : 'text-gray-700'"
            class="block mb-1 transition-colors duration-300"
          >
            Discount (%)
          </label>
          <input
            type="number"
            :value="getDiscountDisplayValue()"
            @input="handleDiscountChange"
            placeholder="Enter discount percentage (e.g. 25 for 25%)"
            :class="themeStore.darkMode ? 'bg-gray-700 text-light' : 'bg-gray-100 text-gray-800'"
            class="w-full px-3 py-2 rounded transition-colors duration-300"
            min="0"
            max="100"
            step="1"
          />
          <p :class="themeStore.darkMode ? 'text-gray-400' : 'text-gray-500'" class="text-xs mt-1">
            Leave empty for no discount
          </p>
        </div>
        <div class="flex justify-end space-x-2">
          <button
            type="button"
            @click="emit('close')"
            :class="[
              themeStore.darkMode ? 'bg-gray-600 text-white hover:bg-gray-500' : 'bg-gray-300 text-gray-800 hover:bg-gray-400'
            ]"
            class="px-4 py-2 rounded transition-colors duration-300"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="px-4 py-2 bg-primary text-white rounded hover:bg-accent transition-colors duration-300"
          >
            {{ product ? 'Update' : 'Create' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

