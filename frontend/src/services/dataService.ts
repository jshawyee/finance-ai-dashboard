import { fallbackData } from '../data/fallback'
import type { DashboardData } from '../types/finance'

const DATA_URL = `${import.meta.env.BASE_URL}data/dashboard.json`

export async function fetchDashboardData(): Promise<DashboardData> {
  try {
    const response = await fetch(`${DATA_URL}?t=${Date.now()}`, { cache: 'no-store' })
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    return (await response.json()) as DashboardData
  } catch (error) {
    console.warn('Unable to load generated dashboard data, using safe demo data.', error)
    return fallbackData
  }
}

