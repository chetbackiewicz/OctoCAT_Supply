<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { api } from '@/api/config'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import ProductForm from '@/components/entity/product/ProductForm.vue'

interface Supplier {
  supplierId: number
  name: string
  description: string
  contactPerson: string
  email: string
  phone: string
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
  supplier?: Supplier
  discount?: number
}

type SortField = 'name' | 'price' | 'sku' | 'unit' | 'supplier'
type SortOrder = 'asc' | 'desc'

const authStore = useAuthStore()
const themeStore = useThemeStore()
const router = useRouter()

const products = ref<Product[]>([])
const suppliers = ref<Supplier[]>([])
const editingProduct = ref<Product | undefined>(undefined)
const showForm = ref(false)
const sortField = ref<SortField>('name')
const sortOrder = ref<SortOrder>('asc')

// Redirect if not admin
if (!authStore.isAdmin) {
  router.replace('/')
}

onMounted(() => {
  fetchProducts()
  fetchSuppliers()
})

async function fetchProducts() {
  try {
    const response = await axios.get(`${api.baseURL}${api.endpoints.products}`)
    const productsData = response.data

    // Fetch supplier details for each product
    const productsWithSuppliers = await Promise.all(
      productsData.map(async (product: Product) => {
        try {
          const supplierResponse = await axios.get(
            `${api.baseURL}${api.endpoints.suppliers}/${product.supplierId}`
          )
          return { ...product, supplier: supplierResponse.data }
        } catch (error) {
          console.error(`Error fetching supplier for product ${product.productId}:`, error)
          return product
        }
      })
    )

    products.value = productsWithSuppliers
  } catch (error) {
    console.error('Error fetching products:', error)
  }
}

async function fetchSuppliers() {
  try {
    const response = await axios.get(`${api.baseURL}${api.endpoints.suppliers}`)
    suppliers.value = response.data
  } catch (error) {
    console.error('Error fetching suppliers:', error)
  }
}

function handleSort(field: SortField) {
  if (field === sortField.value) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortOrder.value = 'asc'
  }
}

const sortedProducts = computed(() => {
  return [...products.value].sort((a, b) => {
    const modifier = sortOrder.value === 'asc' ? 1 : -1
    if (sortField.value === 'price') {
      return (a.price - b.price) * modifier
    }
    if (sortField.value === 'supplier') {
      return (a.supplier?.name || '').localeCompare(b.supplier?.name || '') * modifier
    }
    const aVal = a[sortField.value] as string
    const bVal = b[sortField.value] as string
    return aVal.localeCompare(bVal) * modifier
  })
})

function renderSortIcon(field: SortField): string {
  if (field !== sortField.value) {
    return '↕'
  }
  return sortOrder.value === 'asc' ? '↑' : '↓'
}

function openAddForm() {
  editingProduct.value = undefined
  showForm.value = true
}

function openEditForm(product: Product) {
  editingProduct.value = product
  showForm.value = true
}

function closeForm() {
  showForm.value = false
  editingProduct.value = undefined
}

async function deleteProduct(product: Product) {
  if (window.confirm('Are you sure you want to delete this product?')) {
    try {
      await axios.delete(`${api.baseURL}${api.endpoints.products}/${product.productId}`)
      await fetchProducts()
    } catch (error) {
      console.error('Error deleting product:', error)
    }
  }
}
</script>

<template>
  <div
    :class="themeStore.darkMode ? 'bg-dark' : 'bg-gray-100'"
    class="container mx-auto px-4 pt-20 pb-8 min-h-screen transition-colors duration-300"
  >
    <div class="flex justify-between items-center mb-6">
      <h1
        :class="themeStore.darkMode ? 'text-light' : 'text-gray-800'"
        class="text-2xl font-bold transition-colors duration-300"
      >
        Product Management
      </h1>
      <button
        @click="openAddForm"
        class="px-4 py-2 bg-primary hover:bg-accent text-white rounded transition-colors duration-300"
      >
        Add New Product
      </button>
    </div>

    <div class="overflow-x-auto rounded-lg shadow-lg">
      <table
        :class="themeStore.darkMode ? 'bg-dark' : 'bg-white'"
        class="min-w-full rounded-lg overflow-hidden transition-colors duration-300"
      >
        <thead
          :class="themeStore.darkMode ? 'bg-gray-800' : 'bg-gray-200'"
          class="transition-colors duration-300"
        >
          <tr>
            <th
              :class="themeStore.darkMode ? 'text-light' : 'text-gray-700'"
              class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider cursor-pointer hover:bg-opacity-80 transition-colors duration-300"
              @click="handleSort('name')"
            >
              Name {{ renderSortIcon('name') }}
            </th>
            <th
              :class="themeStore.darkMode ? 'text-light' : 'text-gray-700'"
              class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider cursor-pointer hover:bg-opacity-80 transition-colors duration-300"
              @click="handleSort('supplier')"
            >
              Supplier {{ renderSortIcon('supplier') }}
            </th>
            <th
              :class="themeStore.darkMode ? 'text-light' : 'text-gray-700'"
              class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider cursor-pointer hover:bg-opacity-80 transition-colors duration-300"
              @click="handleSort('price')"
            >
              Price {{ renderSortIcon('price') }}
            </th>
            <th
              :class="themeStore.darkMode ? 'text-light' : 'text-gray-700'"
              class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider cursor-pointer hover:bg-opacity-80 transition-colors duration-300"
              @click="handleSort('sku')"
            >
              SKU {{ renderSortIcon('sku') }}
            </th>
            <th
              :class="themeStore.darkMode ? 'text-light' : 'text-gray-700'"
              class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider cursor-pointer hover:bg-opacity-80 transition-colors duration-300"
              @click="handleSort('unit')"
            >
              Unit {{ renderSortIcon('unit') }}
            </th>
            <th
              :class="themeStore.darkMode ? 'text-light' : 'text-gray-700'"
              class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider transition-colors duration-300"
            >
              Discount
            </th>
            <th
              :class="themeStore.darkMode ? 'text-light' : 'text-gray-700'"
              class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider transition-colors duration-300"
            >
              Description
            </th>
            <th
              :class="themeStore.darkMode ? 'text-light' : 'text-gray-700'"
              class="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider transition-colors duration-300"
            >
              Actions
            </th>
          </tr>
        </thead>
        <tbody
          :class="themeStore.darkMode ? 'divide-gray-700' : 'divide-gray-200'"
          class="divide-y transition-colors duration-300"
        >
          <tr
            v-for="product in sortedProducts"
            :key="product.productId"
            class="hover:bg-opacity-50 transition-colors duration-300"
          >
            <td
              :class="themeStore.darkMode ? 'text-light' : 'text-gray-800'"
              class="px-6 py-4 whitespace-nowrap transition-colors duration-300"
            >
              {{ product.name }}
            </td>
            <td
              :class="themeStore.darkMode ? 'text-light' : 'text-gray-800'"
              class="px-6 py-4 whitespace-nowrap transition-colors duration-300"
            >
              {{ product.supplier?.name || 'Unknown' }}
            </td>
            <td
              :class="themeStore.darkMode ? 'text-light' : 'text-gray-800'"
              class="px-6 py-4 whitespace-nowrap transition-colors duration-300"
            >
              ${{ product.price.toFixed(2) }}
            </td>
            <td
              :class="themeStore.darkMode ? 'text-light' : 'text-gray-800'"
              class="px-6 py-4 whitespace-nowrap transition-colors duration-300"
            >
              {{ product.sku }}
            </td>
            <td
              :class="themeStore.darkMode ? 'text-light' : 'text-gray-800'"
              class="px-6 py-4 whitespace-nowrap transition-colors duration-300"
            >
              {{ product.unit }}
            </td>
            <td
              :class="themeStore.darkMode ? 'text-light' : 'text-gray-800'"
              class="px-6 py-4 whitespace-nowrap transition-colors duration-300"
            >
              {{ product.discount ? `${(product.discount * 100).toFixed(0)}%` : '-' }}
            </td>
            <td
              :class="themeStore.darkMode ? 'text-light' : 'text-gray-800'"
              class="px-6 py-4 transition-colors duration-300"
            >
              <div class="max-w-xs truncate">{{ product.description }}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm space-x-2">
              <button
                @click="openEditForm(product)"
                class="inline-flex items-center px-3 py-1 bg-primary text-white rounded hover:bg-accent transition-colors duration-300"
              >
                Edit
              </button>
              <button
                @click="deleteProduct(product)"
                class="inline-flex items-center px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700 transition-colors duration-300"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <ProductForm
      v-if="showForm"
      :product="editingProduct"
      :suppliers="suppliers"
      @close="closeForm"
      @save="fetchProducts"
    />
  </div>
</template>

