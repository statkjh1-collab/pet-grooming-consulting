<template>
  <main class="page">
    <div class="page-head">
      <div>
        <h1 class="page-title">🐾 강서구 반려동물 상권 분석</h1>
        <p class="page-desc">경쟁 밀도와 상권 포화도를 지도·차트로 파악합니다.</p>
      </div>
      <RouterLink to="/startup/properties" class="btn-secondary">매물 비교로</RouterLink>
    </div>

    <div v-if="loading" class="state-msg">불러오는 중...</div>

    <div v-else-if="error" class="state-msg error">
      {{ error }}
      <div class="setup-hint">
        <p><strong>처음 사용 시 준비:</strong></p>
        <ol>
          <li><a href="https://www.data.go.kr/data/15012005/openapi.do" target="_blank">data.go.kr 상가업소정보 API</a> 활용신청 (승인까지 1~2시간)</li>
          <li>발급받은 서비스키를 <code>backend/.env</code>의 <code>DATA_GO_KR_SERVICE_KEY</code>에 저장</li>
          <li><code>backend</code> 폴더에서 <code>python fetch_market.py</code> 실행</li>
        </ol>
      </div>
    </div>

    <template v-else-if="distribution">
      <p class="snapshot-note">
        소상공인시장진흥공단 상가업소정보 기준 (스냅샷: {{ distribution.snapshot_month }}) · 상권 해석·경쟁 밀도
        참고용이며, 개업 시점은 이 데이터로 확인할 수 없습니다.
      </p>

      <div class="grooming-note">
        📌 참고: "애견미용실"은 2023년 업종분류 개편으로 애완동물/애완용품 소매업 코드에 통합되어 공식 코드로는
        분리되지 않습니다. 상호명에 {{ distribution.grooming_estimate.keywords.join('/') }}이 포함된 업소는
        전체 {{ distribution.grooming_estimate.base_count }}개 중
        <strong>{{ distribution.grooming_estimate.keyword_count }}개</strong> ({{ distribution.grooming_estimate.note }})
      </div>

      <section class="section">
        <h2>업종 구성 — {{ distribution.region }} 전체 {{ distribution.total_stores.toLocaleString() }}건</h2>
        <div class="bar-list">
          <div class="bar-row" v-for="row in citywideSorted" :key="row.category">
            <span class="bar-label">{{ row.category }}</span>
            <div class="bar-track">
              <div
                class="bar-fill"
                :style="{ width: (row.count / citywideMax * 100) + '%', background: categoryColor[row.category] }"
              ></div>
            </div>
            <span class="bar-value">{{ row.count.toLocaleString() }}</span>
          </div>
        </div>
      </section>

      <section class="section">
        <h2>지도로 보기</h2>
        <ul class="legend">
          <li v-for="cat in distribution.category_order" :key="cat">
            <span class="swatch" :style="{ background: categoryColor[cat] }"></span>{{ cat }}
          </li>
        </ul>
        <div ref="mapEl" class="map"></div>
      </section>

      <section class="section">
        <div class="section-head">
          <h2>행정동별 분포 (업소 수 기준 정렬)</h2>
          <button class="toggle-btn" @click="showTable = !showTable">
            {{ showTable ? '차트로 보기' : '표로 보기' }}
          </button>
        </div>

        <div v-if="!showTable" class="stacked-bars">
          <div class="dong-row" v-for="dong in distribution.by_dong" :key="dong.dong">
            <span class="dong-label">{{ dong.dong }}</span>
            <div class="stacked-track" :style="{ width: (dong.total / dongMax * 100) + '%' }">
              <div
                class="segment"
                v-for="seg in segments(dong)"
                :key="seg.category"
                :style="{ width: (seg.count / dong.total * 100) + '%', background: categoryColor[seg.category] }"
                tabindex="0"
                @pointermove="showTooltip($event, dong.dong, seg.category, seg.count, dong.total)"
                @pointerleave="hideTooltip"
                @focus="showTooltip($event, dong.dong, seg.category, seg.count, dong.total)"
                @blur="hideTooltip"
              ></div>
            </div>
            <span class="dong-total">{{ dong.total.toLocaleString() }}</span>
          </div>
        </div>

        <table v-else class="data-table">
          <thead>
            <tr>
              <th>행정동</th>
              <th>합계</th>
              <th v-for="cat in distribution.category_order" :key="cat">{{ cat }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="dong in distribution.by_dong" :key="dong.dong">
              <td>{{ dong.dong }}</td>
              <td class="num">{{ dong.total.toLocaleString() }}</td>
              <td class="num" v-for="cat in distribution.category_order" :key="cat">{{ dong.categories[cat] ?? 0 }}</td>
            </tr>
          </tbody>
        </table>
      </section>

      <section v-if="trend.length" class="section">
        <h2>📈 월별 추적 (스냅샷 이력)</h2>
        <p class="desc-text">
          매달 스냅샷을 쌓아 변화를 추적합니다. API에 개업일자 필드가 없어 "순증감"은 전월 대비 총 업소 수
          차이로 근사한 값입니다 (폐업·신규 구분 불가).
        </p>
        <table class="data-table">
          <thead>
            <tr>
              <th>월</th>
              <th>총 업소 수</th>
              <th>전월 대비</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="t in trend" :key="t.snapshot_month">
              <td>{{ t.snapshot_month }}</td>
              <td class="num">{{ t.total_stores.toLocaleString() }}</td>
              <td class="num" :class="changeClass(t.net_change)">
                {{ t.net_change === null ? '-' : (t.net_change > 0 ? '+' : '') + t.net_change }}
              </td>
            </tr>
          </tbody>
        </table>
      </section>
    </template>

    <div
      class="tooltip"
      v-if="tooltip"
      :style="{ left: tooltip.x + 12 + 'px', top: tooltip.y + 12 + 'px' }"
      @pointermove="moveTooltip"
    >
      <strong>{{ tooltip.count.toLocaleString() }}건 ({{ tooltip.ratio.toFixed(1) }}%)</strong>
      <span>{{ tooltip.dong }} · {{ tooltip.category }}</span>
    </div>
  </main>
</template>

<script setup>
import { computed, nextTick, onMounted, ref } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { fetchMarketLatest, fetchMarketTrend } from '../../api/startup'

const SLOT_COLORS = ['#2a78d6', '#1baf7a', '#eda100', '#008300', '#4a3aa7', '#e34948', '#e87ba4', '#eb6834']

const distribution = ref(null)
const trend = ref([])
const loading = ref(true)
const error = ref('')
const showTable = ref(false)
const tooltip = ref(null)
const mapEl = ref(null)
let map = null

onMounted(async () => {
  try {
    const [dist, trendData] = await Promise.all([fetchMarketLatest(), fetchMarketTrend()])
    distribution.value = dist
    trend.value = trendData
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }

  if (distribution.value) {
    await nextTick()
    initMap()
    renderPoints()
  }
})

const categoryColor = computed(() => {
  if (!distribution.value) return {}
  const map = {}
  distribution.value.category_order.forEach((cat, i) => {
    map[cat] = SLOT_COLORS[i % SLOT_COLORS.length]
  })
  return map
})

const citywideSorted = computed(() => {
  if (!distribution.value) return []
  return Object.entries(distribution.value.citywide_categories)
    .map(([category, count]) => ({ category, count }))
    .sort((a, b) => b.count - a.count)
})
const citywideMax = computed(() => citywideSorted.value[0]?.count ?? 1)
const dongMax = computed(() =>
  distribution.value ? Math.max(...distribution.value.by_dong.map((d) => d.total)) : 1,
)

function segments(dong) {
  return distribution.value.category_order
    .filter((cat) => dong.categories[cat])
    .map((cat) => ({ category: cat, count: dong.categories[cat] }))
}

function showTooltip(evt, dong, category, count, total) {
  tooltip.value = { x: evt.clientX, y: evt.clientY, dong, category, count, ratio: total ? (count / total) * 100 : 0 }
}
function moveTooltip(evt) {
  if (tooltip.value) {
    tooltip.value.x = evt.clientX
    tooltip.value.y = evt.clientY
  }
}
function hideTooltip() {
  tooltip.value = null
}

function changeClass(change) {
  if (change === null || change === 0) return ''
  return change > 0 ? 'positive' : 'negative'
}

// 우장산역 (서울 지하철 5호선, 강서구 후보 상권 중심)
const UJANGSAN_STATION = [37.5489, 126.8364]

function initMap() {
  if (map || !mapEl.value) return
  map = L.map(mapEl.value, { preferCanvas: true }).setView(UJANGSAN_STATION, 15)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 19,
  }).addTo(map)
}

function renderPoints() {
  if (!map || !distribution.value) return
  const layer = L.layerGroup()
  distribution.value.points.forEach((pt) => {
    const color = categoryColor.value[pt.category] ?? '#9ca3af'
    L.circleMarker([pt.lat, pt.lon], {
      radius: 4,
      color,
      weight: 1,
      fillColor: color,
      fillOpacity: 0.7,
    })
      .bindPopup(`<strong>${pt.name}</strong><br>${pt.category} · ${pt.dong}`)
      .addTo(layer)
  })
  layer.addTo(map)
}
</script>

<style scoped>
.page-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  flex-wrap: wrap;
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

.state-msg {
  padding: 2rem;
  text-align: center;
  color: #6b7280;
}

.state-msg.error {
  color: #b91c1c;
  text-align: left;
}

.setup-hint {
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: 10px;
  padding: 1rem 1.25rem;
  margin-top: 1rem;
  color: #713f12;
  font-size: 0.85rem;
}

.setup-hint ol {
  margin: 0.5rem 0 0;
  padding-left: 1.25rem;
  line-height: 1.8;
}

.setup-hint code {
  background: #fef3c7;
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
  font-size: 0.8rem;
}

.snapshot-note {
  color: #6b7280;
  font-size: 0.85rem;
  line-height: 1.6;
  margin: 1rem 0 0.75rem;
}

.grooming-note {
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: 10px;
  padding: 0.85rem 1.1rem;
  font-size: 0.85rem;
  color: #713f12;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.desc-text {
  color: #6b7280;
  font-size: 0.85rem;
  line-height: 1.6;
  margin: 0 0 1rem;
}

.bar-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.bar-row {
  display: grid;
  grid-template-columns: 180px 1fr 60px;
  align-items: center;
  gap: 0.75rem;
}

.bar-label {
  font-size: 0.85rem;
  color: #374151;
  text-align: right;
}

.bar-track {
  height: 22px;
  background: #f3f4f6;
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 4px;
}

.bar-value {
  font-size: 0.85rem;
  color: #111;
  font-variant-numeric: tabular-nums;
}

.legend {
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem 1rem;
  padding: 0;
  margin: 0 0 1rem;
  font-size: 0.8rem;
  color: #6b7280;
}

.legend li {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.swatch {
  width: 10px;
  height: 10px;
  border-radius: 2px;
  display: inline-block;
}

.map {
  height: 420px;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #e5e7eb;
}

.section-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}

.toggle-btn {
  border: 1px solid #e5e7eb;
  background: #fff;
  color: #6b7280;
  border-radius: 6px;
  padding: 0.3rem 0.7rem;
  font-size: 0.8rem;
  cursor: pointer;
}

.toggle-btn:hover {
  border-color: #f59e0b;
  color: #d97706;
}

.stacked-bars {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.dong-row {
  display: grid;
  grid-template-columns: 80px 1fr 56px;
  align-items: center;
  gap: 0.6rem;
}

.dong-label {
  font-size: 0.85rem;
  color: #374151;
  text-align: right;
}

.dong-total {
  font-size: 0.85rem;
  font-variant-numeric: tabular-nums;
  color: #111;
}

.stacked-track {
  height: 22px;
  display: flex;
  border-radius: 4px;
  overflow: hidden;
  background: #f3f4f6;
  min-width: 4%;
}

.segment {
  height: 100%;
  border-right: 2px solid #fff;
}

.segment:last-child {
  border-right: none;
}

.segment:hover,
.segment:focus-visible {
  filter: brightness(1.08);
  outline: 2px solid #111;
  outline-offset: -2px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
}

.data-table th,
.data-table td {
  padding: 0.5rem 0.6rem;
  border-bottom: 1px solid #f3f4f6;
  text-align: left;
}

.data-table .num {
  text-align: right;
  font-variant-numeric: tabular-nums;
}

.data-table th {
  color: #6b7280;
  font-weight: 600;
}

.data-table .positive {
  color: #d97706;
  font-weight: 700;
}

.data-table .negative {
  color: #2563eb;
  font-weight: 700;
}

.tooltip {
  position: fixed;
  z-index: 20;
  background: #111;
  color: #fff;
  padding: 0.4rem 0.65rem;
  border-radius: 6px;
  font-size: 0.8rem;
  pointer-events: none;
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.tooltip strong {
  font-size: 0.9rem;
}
</style>
