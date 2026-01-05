import { apiFetch } from './client'

export function listHabits() {
  return apiFetch('/api/habits')
}

export function getHabit(id) {
  return apiFetch(`/api/habits/${id}`)
}

export function createHabit(payload) {
  return apiFetch('/api/habits', { method: 'POST', body: JSON.stringify(payload) })
}

export function updateHabit(id, payload) {
  return apiFetch(`/api/habits/${id}`, { method: 'PATCH', body: JSON.stringify(payload) })
}

export function deleteHabit(id) {
  return apiFetch(`/api/habits/${id}`, { method: 'DELETE' })
}

export function listRecords(id) {
  return apiFetch(`/api/habits/${id}/records`)
}

export function upsertRecord(id, payload) {
  return apiFetch(`/api/habits/${id}/records`, { method: 'POST', body: JSON.stringify(payload) })
}

export function getDue(windowMinutes = 60) {
  return apiFetch(`/api/due?window_minutes=${encodeURIComponent(windowMinutes)}`)
}
