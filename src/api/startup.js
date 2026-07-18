const BASE = '/api'

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const body = await res.text()
    throw new Error(`API 요청 실패 (${res.status}): ${body}`)
  }
  if (res.status === 204) return null
  return res.json()
}

export function fetchChecklist() {
  return request('/checklist')
}

export function updateChecklistItem(itemId, payload) {
  return request(`/checklist/items/${itemId}`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  })
}

export function fetchProperties(status) {
  const qs = status ? `?status=${encodeURIComponent(status)}` : ''
  return request(`/properties${qs}`)
}

export function fetchPropertySummary() {
  return request('/properties/summary')
}

export function fetchProperty(id) {
  return request(`/properties/${id}`)
}

export function createProperty(payload) {
  return request('/properties', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function updateProperty(id, payload) {
  return request(`/properties/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  })
}

export function deleteProperty(id) {
  return request(`/properties/${id}`, { method: 'DELETE' })
}

export function addPriceHistory(propertyId, payload) {
  return request(`/properties/${propertyId}/price-history`, {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function fetchPois(relation) {
  const qs = relation ? `?relation=${encodeURIComponent(relation)}` : ''
  return request(`/pois${qs}`)
}

export function fetchMarketLatest() {
  return request('/market/latest')
}

export function fetchMarketTrend() {
  return request('/market/trend')
}
