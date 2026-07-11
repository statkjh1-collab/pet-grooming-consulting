import { ref } from 'vue'
import { defineStore } from 'pinia'
import { fetchChecklist, updateChecklistItem } from '../../api/startup'

export const useChecklistStore = defineStore('startupChecklist', () => {
  const stages = ref([])
  const loading = ref(false)
  const error = ref('')

  async function load() {
    loading.value = true
    error.value = ''
    try {
      stages.value = await fetchChecklist()
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  function findItem(itemId) {
    for (const stage of stages.value) {
      for (const group of stage.groups) {
        const item = group.items.find((i) => i.id === itemId)
        if (item) return { stage, item }
      }
    }
    return null
  }

  function recomputeStageProgress(stage) {
    const total = stage.groups.reduce((sum, g) => sum + g.items.length, 0)
    const completed = stage.groups.reduce(
      (sum, g) => sum + g.items.filter((i) => i.done).length,
      0,
    )
    stage.total_items = total
    stage.completed_items = completed
    stage.progress_pct = total ? Math.round((completed / total) * 1000) / 10 : 0
  }

  async function toggleDone(itemId, done) {
    const found = findItem(itemId)
    if (!found) return
    const updated = await updateChecklistItem(itemId, { done })
    Object.assign(found.item, updated)
    recomputeStageProgress(found.stage)
  }

  async function saveMemo(itemId, memo) {
    const found = findItem(itemId)
    if (!found) return
    const updated = await updateChecklistItem(itemId, { memo })
    Object.assign(found.item, updated)
  }

  return { stages, loading, error, load, toggleDone, saveMemo }
})
