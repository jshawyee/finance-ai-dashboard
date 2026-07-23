import { computed, onMounted, ref } from 'vue'
import { fetchDashboardData } from '../services/dataService'
import type { DashboardData } from '../types/finance'

export function useDashboardData() {
  const data = ref<DashboardData | null>(null)
  const loading = ref(true)
  const error = ref('')
  const isHealthy = computed(() => data.value?.meta.status === 'fresh')

  async function refresh() {
    loading.value = true
    error.value = ''
    try {
      data.value = await fetchDashboardData()
    } catch (cause) {
      error.value = cause instanceof Error ? cause.message : '数据加载失败'
    } finally {
      loading.value = false
    }
  }

  onMounted(refresh)
  return { data, loading, error, isHealthy, refresh }
}
