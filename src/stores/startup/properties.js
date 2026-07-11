import { ref } from 'vue'
import { defineStore } from 'pinia'
import {
  fetchProperties,
  fetchPropertySummary,
  fetchProperty,
  createProperty as apiCreateProperty,
  updateProperty as apiUpdateProperty,
  deleteProperty as apiDeleteProperty,
  addPriceHistory as apiAddPriceHistory,
  fetchPois,
} from '../../api/startup'

export const usePropertiesStore = defineStore('startupProperties', () => {
  const properties = ref([])
  const summary = ref(null)
  const pois = ref([])
  const loading = ref(false)
  const error = ref('')

  async function loadAll() {
    loading.value = true
    error.value = ''
    try {
      const [propList, summaryData, poiList] = await Promise.all([
        fetchProperties(),
        fetchPropertySummary(),
        fetchPois(),
      ])
      properties.value = propList
      summary.value = summaryData
      pois.value = poiList
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function loadProperty(id) {
    return fetchProperty(id)
  }

  async function createProperty(payload) {
    const created = await apiCreateProperty(payload)
    properties.value.unshift(created)
    return created
  }

  async function updateProperty(id, payload) {
    const updated = await apiUpdateProperty(id, payload)
    const idx = properties.value.findIndex((p) => p.id === id)
    if (idx !== -1) properties.value[idx] = updated
    return updated
  }

  async function deleteProperty(id) {
    await apiDeleteProperty(id)
    properties.value = properties.value.filter((p) => p.id !== id)
  }

  async function addPriceHistory(propertyId, payload) {
    return apiAddPriceHistory(propertyId, payload)
  }

  return {
    properties,
    summary,
    pois,
    loading,
    error,
    loadAll,
    loadProperty,
    createProperty,
    updateProperty,
    deleteProperty,
    addPriceHistory,
  }
})
