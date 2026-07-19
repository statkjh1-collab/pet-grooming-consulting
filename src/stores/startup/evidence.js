import { ref } from 'vue'
import { defineStore } from 'pinia'
import {
  fetchEvidence,
  createEvidence as apiCreateEvidence,
  updateEvidence as apiUpdateEvidence,
  deleteEvidence as apiDeleteEvidence,
} from '../../api/startup'

export const useEvidenceStore = defineStore('startupEvidence', () => {
  const items = ref([])
  const loading = ref(false)
  const error = ref('')

  async function load(type) {
    loading.value = true
    error.value = ''
    try {
      items.value = await fetchEvidence(type)
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function createItem(payload) {
    const created = await apiCreateEvidence(payload)
    items.value.unshift(created)
    return created
  }

  async function updateItem(id, payload) {
    const updated = await apiUpdateEvidence(id, payload)
    const idx = items.value.findIndex((i) => i.id === id)
    if (idx !== -1) items.value[idx] = updated
    return updated
  }

  async function deleteItem(id) {
    await apiDeleteEvidence(id)
    items.value = items.value.filter((i) => i.id !== id)
  }

  return { items, loading, error, load, createItem, updateItem, deleteItem }
})
