<template>
  <main class="page">
    <div class="page-head">
      <div>
        <h1 class="page-title">🏘️ 상권·입지</h1>
        <p class="page-desc">매물 시세를 비교하고 시간에 따른 변화를 추적합니다.</p>
      </div>
      <div class="head-actions">
        <RouterLink to="/startup/market" class="btn-secondary">🐾 상권 분석</RouterLink>
        <RouterLink to="/startup/properties/new" class="btn-primary">+ 매물 등록</RouterLink>
      </div>
    </div>

    <div class="reminder">
      📌 지금은 계약이 아니라 <strong>기록하는 단계</strong>입니다. 예창패 선정 후 계약하세요.
      임대차 계약을 하면 예비창업자 자격을 잃습니다.
    </div>

    <div v-if="store.loading" class="state-msg">불러오는 중...</div>
    <div v-else-if="store.error" class="state-msg error">
      {{ store.error }}<br />
      <span class="hint">백엔드(FastAPI)가 실행 중인지 확인하세요 (uvicorn main:app, 8000번 포트).</span>
    </div>

    <template v-else>
      <section v-if="store.summary" class="summary-card">
        <h2>상권 시세 기준선</h2>
        <p class="summary-note">
          이 요약은 예창패 자금소요계획의 근거로 활용할 수 있습니다.
        </p>
        <div v-if="store.summary.count > 0" class="summary-grid">
          <div class="summary-item">
            <span class="label">조사 매물 수</span>
            <span class="value">{{ store.summary.count }}건</span>
          </div>
          <div class="summary-item">
            <span class="label">평수 범위</span>
            <span class="value">{{ store.summary.area_min }}~{{ store.summary.area_max }}평</span>
          </div>
          <div class="summary-item">
            <span class="label">보증금 범위</span>
            <span class="value">
              {{ store.summary.deposit_min.toLocaleString() }}~{{ store.summary.deposit_max.toLocaleString() }}만원
            </span>
          </div>
          <div class="summary-item">
            <span class="label">월세 범위</span>
            <span class="value">
              {{ store.summary.rent_min.toLocaleString() }}~{{ store.summary.rent_max.toLocaleString() }}만원
            </span>
          </div>
          <div class="summary-item highlight">
            <span class="label">평당 월세 평균</span>
            <span class="value">{{ store.summary.rent_per_pyeong_avg }}만원</span>
          </div>
        </div>
        <p v-else class="summary-empty">등록된 매물이 없습니다.</p>
      </section>

      <section class="filter-row">
        <button
          v-for="s in statusFilters"
          :key="s"
          class="filter-chip"
          :class="{ active: statusFilter === s }"
          @click="statusFilter = s"
        >
          {{ s }}
        </button>
      </section>

      <section class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>이름</th>
              <th>층</th>
              <th>평수</th>
              <th>보증금</th>
              <th>월세</th>
              <th class="sortable" @click="toggleSort">평당월세 {{ sortDir === 'asc' ? '▲' : '▼' }}</th>
              <th>급배수</th>
              <th>확장</th>
              <th>상태</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in sortedProperties" :key="p.id" @click="goDetail(p.id)" class="row-link">
              <td>{{ p.name }}</td>
              <td>{{ p.floor ?? '-' }}</td>
              <td>{{ p.area_pyeong }}평</td>
              <td>{{ p.deposit.toLocaleString() }}만</td>
              <td>{{ p.monthly_rent.toLocaleString() }}만</td>
              <td class="rent-per-pyeong">{{ p.rent_per_pyeong }}만</td>
              <td>
                <span class="badge" :class="waterBadgeClass(p.water_supply)">{{ p.water_supply }}</span>
              </td>
              <td>{{ p.expandable ? '가능' : '-' }}</td>
              <td>
                <span class="badge status" :class="'status-' + p.status">{{ p.status }}</span>
              </td>
            </tr>
            <tr v-if="sortedProperties.length === 0">
              <td colspan="9" class="empty-row">해당 상태의 매물이 없습니다.</td>
            </tr>
          </tbody>
        </table>
      </section>

      <section class="poi-section">
        <h2>🗺️ 주변 시설</h2>

        <div v-for="group in poiGroups" :key="group.relation" class="poi-group" :class="{ urgent: group.relation === '응급대응' }">
          <h3>{{ group.icon }} {{ group.relation }}</h3>
          <ul class="poi-list">
            <li v-for="poi in group.items" :key="poi.id" class="poi-item">
              <div class="poi-main">
                <strong>{{ poi.name }}</strong>
                <span v-if="poi.hours" class="poi-hours">{{ poi.hours }}</span>
              </div>
              <p v-if="poi.address" class="poi-address">{{ poi.address }}</p>
              <p v-if="poi.note" class="poi-note">{{ poi.note }}</p>
            </li>
          </ul>
          <p v-if="group.items.length === 0" class="poi-empty">등록된 시설이 없습니다.</p>
        </div>
      </section>
    </template>
  </main>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { usePropertiesStore } from '../../stores/startup/properties'

const store = usePropertiesStore()
const router = useRouter()

onMounted(() => {
  store.loadAll()
})

const statusFilters = ['전체', '관심', '유력', '보류', '제외']
const statusFilter = ref('전체')
const sortDir = ref('asc')

const filteredProperties = computed(() => {
  if (statusFilter.value === '전체') return store.properties
  return store.properties.filter((p) => p.status === statusFilter.value)
})

const sortedProperties = computed(() => {
  const list = [...filteredProperties.value]
  list.sort((a, b) =>
    sortDir.value === 'asc' ? a.rent_per_pyeong - b.rent_per_pyeong : b.rent_per_pyeong - a.rent_per_pyeong,
  )
  return list
})

function toggleSort() {
  sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc'
}

function waterBadgeClass(value) {
  if (value === '불가') return 'badge-danger'
  if (value === '가능') return 'badge-ok'
  return 'badge-unknown'
}

function goDetail(id) {
  router.push(`/startup/properties/${id}`)
}

const POI_GROUP_ORDER = [
  { relation: '응급대응', icon: '🚨' },
  { relation: '수요파이프라인', icon: '⭐' },
  { relation: '제휴후보', icon: '🤝' },
  { relation: '경쟁', icon: '🔍' },
]

const poiGroups = computed(() =>
  POI_GROUP_ORDER.map((g) => ({
    ...g,
    items: store.pois.filter((p) => p.relation === g.relation),
  })),
)
</script>

<style scoped>
.page-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  flex-wrap: wrap;
}

.head-actions {
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
}

.btn-primary {
  background: #f59e0b;
  color: #fff;
  padding: 0.6rem 1.1rem;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.9rem;
  white-space: nowrap;
}

.btn-primary:hover {
  background: #d97706;
}

.btn-secondary {
  background: #fff;
  color: #374151;
  border: 1px solid #e5e7eb;
  padding: 0.55rem 1rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.85rem;
  white-space: nowrap;
}

.btn-secondary:hover {
  background: #f9fafb;
}

.reminder {
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: 10px;
  padding: 0.85rem 1.1rem;
  font-size: 0.85rem;
  color: #713f12;
  line-height: 1.6;
  margin: 1.25rem 0 1.5rem;
}

.state-msg {
  padding: 2rem;
  text-align: center;
  color: #6b7280;
}

.state-msg.error {
  color: #b91c1c;
}

.hint {
  font-size: 0.85rem;
  color: #9ca3af;
}

.summary-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.summary-card h2 {
  font-size: 1rem;
  font-weight: 700;
  margin: 0 0 0.3rem;
}

.summary-note {
  font-size: 0.8rem;
  color: #9ca3af;
  margin: 0 0 1rem;
}

.summary-empty {
  color: #9ca3af;
  font-size: 0.875rem;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1rem;
}

.summary-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.summary-item .label {
  font-size: 0.75rem;
  color: #9ca3af;
}

.summary-item .value {
  font-size: 1.05rem;
  font-weight: 700;
  color: #111;
}

.summary-item.highlight {
  background: #fffbeb;
  border-radius: 8px;
  padding: 0.5rem 0.75rem;
}

.summary-item.highlight .value {
  color: #d97706;
}

.filter-row {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.filter-chip {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  padding: 0.4rem 0.9rem;
  font-size: 0.85rem;
  color: #6b7280;
  cursor: pointer;
}

.filter-chip.active {
  background: #fef3c7;
  border-color: #fde68a;
  color: #d97706;
  font-weight: 700;
}

.table-wrap {
  overflow-x: auto;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  margin-bottom: 2rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

thead {
  background: #fef3c7;
}

th {
  padding: 0.75rem 0.9rem;
  text-align: left;
  font-weight: 700;
  color: #92400e;
  white-space: nowrap;
}

th.sortable {
  cursor: pointer;
  user-select: none;
}

td {
  padding: 0.7rem 0.9rem;
  border-top: 1px solid #f3f4f6;
  color: #374151;
  white-space: nowrap;
}

.row-link {
  cursor: pointer;
}

.row-link:hover {
  background: #fffbeb;
}

.rent-per-pyeong {
  font-weight: 700;
  color: #d97706;
}

.empty-row {
  text-align: center;
  color: #9ca3af;
  padding: 1.5rem;
}

.badge {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.15rem 0.55rem;
  border-radius: 20px;
}

.badge-danger {
  background: #fee2e2;
  color: #b91c1c;
}

.badge-ok {
  background: #dcfce7;
  color: #15803d;
}

.badge-unknown {
  background: #f3f4f6;
  color: #6b7280;
}

.badge.status-관심 {
  background: #f3f4f6;
  color: #6b7280;
}

.badge.status-유력 {
  background: #fef3c7;
  color: #d97706;
}

.badge.status-보류 {
  background: #e0e7ff;
  color: #4338ca;
}

.badge.status-제외 {
  background: #f3f4f6;
  color: #9ca3af;
}

.poi-section h2 {
  font-size: 1.1rem;
  font-weight: 700;
  margin: 0 0 1rem;
}

.poi-group {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 1rem;
}

.poi-group.urgent {
  background: #fef2f2;
  border-color: #fecaca;
}

.poi-group h3 {
  font-size: 0.95rem;
  font-weight: 700;
  margin: 0 0 0.75rem;
  color: #374151;
}

.poi-group.urgent h3 {
  color: #b91c1c;
}

.poi-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.poi-item {
  border-top: 1px solid #f3f4f6;
  padding-top: 0.6rem;
}

.poi-item:first-child {
  border-top: none;
  padding-top: 0;
}

.poi-main {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.poi-hours {
  font-size: 0.75rem;
  color: #d97706;
  font-weight: 600;
}

.poi-address {
  margin: 0.2rem 0 0;
  font-size: 0.8rem;
  color: #6b7280;
}

.poi-note {
  margin: 0.25rem 0 0;
  font-size: 0.8rem;
  color: #9ca3af;
  line-height: 1.5;
}

.poi-empty {
  color: #9ca3af;
  font-size: 0.85rem;
}

@media (max-width: 640px) {
  .summary-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
