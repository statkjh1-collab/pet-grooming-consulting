<template>
  <main class="page">
    <h1 class="page-title">{{ isEdit ? '✏️ 매물 수정' : '➕ 매물 등록' }}</h1>
    <p class="page-desc">현장에서 바로 입력할 수 있도록 필요한 정보만 채우면 됩니다.</p>

    <div v-if="loading" class="state-msg">불러오는 중...</div>
    <div v-else-if="loadError" class="state-msg error">{{ loadError }}</div>

    <template v-else>
      <section class="calc-bar">
        <div class="calc-item highlight">
          <span class="label">평당 월세</span>
          <span class="value">{{ rentPerPyeong }}만원</span>
        </div>
        <div class="calc-item">
          <span class="label">연 임대료</span>
          <span class="value">{{ annualRent.toLocaleString() }}만원</span>
        </div>
        <div class="calc-item">
          <span class="label">초기 비용(보증금+권리금)</span>
          <span class="value">{{ initialCost.toLocaleString() }}만원</span>
        </div>
      </section>

      <form class="form" @submit.prevent="onSave">
        <div class="field">
          <label>매물 식별명 *</label>
          <input v-model="form.name" type="text" placeholder="예: 사과나무학원 1층" required />
        </div>

        <div class="field">
          <label>위치 설명 (랜드마크)</label>
          <input v-model="form.landmark" type="text" placeholder="예: 사과나무학원 건물 1층" />
        </div>

        <div class="field">
          <label>주소</label>
          <input v-model="form.address" type="text" />
        </div>

        <div class="field-row">
          <div class="field">
            <label>층수</label>
            <input v-model.number="form.floor" type="number" placeholder="미확인" />
          </div>
          <div class="field">
            <label>평수 *</label>
            <input v-model.number="form.area_pyeong" type="number" step="0.1" required />
          </div>
        </div>

        <div class="field-row">
          <div class="field">
            <label>보증금 (만원)</label>
            <input v-model.number="form.deposit" type="number" />
          </div>
          <div class="field">
            <label>월세 (만원)</label>
            <input v-model.number="form.monthly_rent" type="number" />
          </div>
        </div>

        <div class="field-row">
          <div class="field">
            <label>관리비 (만원)</label>
            <input v-model.number="form.maintenance_fee" type="number" placeholder="미확인" />
          </div>
          <div class="field">
            <label>권리금 (만원)</label>
            <input v-model.number="form.key_money" type="number" placeholder="미확인 (없으면 0)" />
          </div>
        </div>

        <div class="field-row checkbox-row">
          <label class="checkbox-field">
            <input v-model="form.negotiable" type="checkbox" />
            네고 가능
          </label>
          <label class="checkbox-field">
            <input v-model="form.expandable" type="checkbox" />
            확장 가능
          </label>
        </div>

        <div v-if="form.expandable" class="field">
          <label>확장 메모</label>
          <input v-model="form.expansion_note" type="text" placeholder="예: 최대 3구역까지" />
        </div>

        <div class="field">
          <label>이전 업종</label>
          <input v-model="form.prev_business" type="text" placeholder="예: 인테리어 → 안경점" />
        </div>

        <div class="field-row">
          <div class="field">
            <label>급배수 <span class="killer">킬러 조건</span></label>
            <select v-model="form.water_supply">
              <option value="미확인">미확인</option>
              <option value="가능">가능</option>
              <option value="불가">불가</option>
            </select>
            <p class="field-hint">펫미용은 욕조·온수 필수. 급배수 안 되면 다른 조건이 좋아도 사용 불가.</p>
          </div>
          <div class="field">
            <label>전기 용량</label>
            <input v-model="form.electric_capacity" type="text" placeholder="미확인" />
            <p class="field-hint">드라이룸·온수기가 전력을 많이 씁니다.</p>
          </div>
        </div>

        <div class="field">
          <label>상태</label>
          <select v-model="form.status">
            <option value="관심">관심</option>
            <option value="유력">유력</option>
            <option value="보류">보류</option>
            <option value="제외">제외</option>
          </select>
        </div>

        <div class="field">
          <label>방문일</label>
          <input v-model="form.visited_at" type="date" />
        </div>

        <div class="field">
          <label>메모</label>
          <textarea v-model="form.memo" rows="4"></textarea>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-primary">{{ isEdit ? '저장' : '등록' }}</button>
          <button v-if="isEdit" type="button" class="btn-danger" @click="onDelete">삭제</button>
        </div>
        <p v-if="saveError" class="save-error">{{ saveError }}</p>
      </form>

      <section v-if="isEdit && unresolvedChecks.length" class="checklist-widget">
        <h2>🔍 다음 방문 시 확인할 것</h2>
        <ul>
          <li v-for="check in unresolvedChecks" :key="check">{{ check }}</li>
          <li>공실 사유 확인 (인근 상인에게 문의)</li>
        </ul>
      </section>

      <section v-if="isEdit" class="price-history">
        <h2>📈 시세 이력</h2>
        <ul v-if="priceHistory.length" class="history-list">
          <li v-for="h in priceHistory" :key="h.id">
            <span class="history-date">{{ h.recorded_at }}</span>
            <span>보증금 {{ h.deposit.toLocaleString() }}만 · 월세 {{ h.monthly_rent.toLocaleString() }}만</span>
            <span v-if="h.is_vacant" class="history-vacant">공실</span>
            <span v-if="h.note" class="history-note">{{ h.note }}</span>
          </li>
        </ul>
        <p v-else class="history-empty">아직 시세 이력이 없습니다.</p>

        <form class="history-form" @submit.prevent="onAddHistory">
          <input v-model.number="historyForm.deposit" type="number" placeholder="보증금(만원)" required />
          <input v-model.number="historyForm.monthly_rent" type="number" placeholder="월세(만원)" required />
          <label class="checkbox-field">
            <input v-model="historyForm.is_vacant" type="checkbox" />
            공실
          </label>
          <input v-model="historyForm.note" type="text" placeholder="메모 (예: 월세 200→180 인하)" />
          <button type="submit" class="btn-secondary">추가</button>
        </form>
      </section>
    </template>
  </main>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePropertiesStore } from '../../stores/startup/properties'

const route = useRoute()
const router = useRouter()
const store = usePropertiesStore()

const isEdit = computed(() => !!route.params.id)

const form = reactive({
  name: '',
  landmark: '',
  address: '',
  floor: null,
  area_pyeong: null,
  deposit: 0,
  monthly_rent: 0,
  maintenance_fee: null,
  key_money: null,
  negotiable: false,
  expandable: false,
  expansion_note: '',
  prev_business: '',
  water_supply: '미확인',
  electric_capacity: '',
  status: '관심',
  visited_at: '',
  memo: '',
})

const priceHistory = ref([])
const unresolvedChecks = ref([])
const loading = ref(false)
const loadError = ref('')
const saveError = ref('')

const historyForm = reactive({
  deposit: null,
  monthly_rent: null,
  is_vacant: true,
  note: '',
})

onMounted(async () => {
  if (!isEdit.value) return
  loading.value = true
  try {
    const prop = await store.loadProperty(route.params.id)
    Object.assign(form, {
      name: prop.name,
      landmark: prop.landmark,
      address: prop.address,
      floor: prop.floor,
      area_pyeong: prop.area_pyeong,
      deposit: prop.deposit,
      monthly_rent: prop.monthly_rent,
      maintenance_fee: prop.maintenance_fee,
      key_money: prop.key_money,
      negotiable: prop.negotiable,
      expandable: prop.expandable,
      expansion_note: prop.expansion_note,
      prev_business: prop.prev_business,
      water_supply: prop.water_supply,
      electric_capacity: prop.electric_capacity,
      status: prop.status,
      visited_at: prop.visited_at || '',
      memo: prop.memo,
    })
    priceHistory.value = prop.price_history
    unresolvedChecks.value = prop.unresolved_checks
  } catch (e) {
    loadError.value = e.message
  } finally {
    loading.value = false
  }
})

const rentPerPyeong = computed(() => {
  if (!form.area_pyeong) return '0.0'
  return (form.monthly_rent / form.area_pyeong).toFixed(1)
})

const annualRent = computed(() => (form.monthly_rent || 0) * 12)

const initialCost = computed(() => (form.deposit || 0) + (form.key_money || 0))

async function onSave() {
  saveError.value = ''
  const payload = { ...form, visited_at: form.visited_at || null }
  try {
    if (isEdit.value) {
      await store.updateProperty(route.params.id, payload)
    } else {
      const created = await store.createProperty(payload)
      router.push(`/startup/properties/${created.id}`)
      return
    }
    router.push('/startup/properties')
  } catch (e) {
    saveError.value = e.message
  }
}

async function onDelete() {
  if (!confirm('이 매물을 삭제할까요?')) return
  await store.deleteProperty(route.params.id)
  router.push('/startup/properties')
}

async function onAddHistory() {
  const entry = await store.addPriceHistory(route.params.id, historyForm)
  priceHistory.value.push(entry)
  historyForm.deposit = null
  historyForm.monthly_rent = null
  historyForm.is_vacant = true
  historyForm.note = ''
}
</script>

<style scoped>
.state-msg {
  padding: 2rem;
  text-align: center;
  color: #6b7280;
}

.state-msg.error {
  color: #b91c1c;
}

.calc-bar {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1rem 1.25rem;
  margin-bottom: 1.5rem;
}

.calc-item {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.calc-item .label {
  font-size: 0.75rem;
  color: #9ca3af;
}

.calc-item .value {
  font-size: 1rem;
  font-weight: 700;
}

.calc-item.highlight {
  background: #fffbeb;
  border-radius: 8px;
  padding: 0.4rem 0.75rem;
}

.calc-item.highlight .value {
  color: #d97706;
  font-size: 1.2rem;
}

.form {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
  margin-bottom: 1.5rem;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  flex: 1;
}

.field-row {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.field label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #374151;
}

.killer {
  display: inline-block;
  background: #fee2e2;
  color: #b91c1c;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.1rem 0.5rem;
  border-radius: 20px;
  margin-left: 0.4rem;
}

.field input,
.field select,
.field textarea {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 0.65rem 0.8rem;
  font-size: 0.95rem;
  font-family: inherit;
  box-sizing: border-box;
  width: 100%;
}

.field input:focus,
.field select:focus,
.field textarea:focus {
  outline: none;
  border-color: #f59e0b;
}

.field-hint {
  margin: 0;
  font-size: 0.75rem;
  color: #9ca3af;
  line-height: 1.5;
}

.checkbox-row {
  gap: 1.5rem;
}

.checkbox-field {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.9rem;
  color: #374151;
  cursor: pointer;
}

.checkbox-field input {
  width: 18px;
  height: 18px;
  accent-color: #f59e0b;
}

.form-actions {
  display: flex;
  gap: 0.75rem;
}

.btn-primary {
  background: #f59e0b;
  color: #fff;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
}

.btn-primary:hover {
  background: #d97706;
}

.btn-danger {
  background: #fff;
  color: #b91c1c;
  border: 1px solid #fecaca;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
}

.btn-danger:hover {
  background: #fef2f2;
}

.save-error {
  color: #b91c1c;
  font-size: 0.85rem;
}

.checklist-widget {
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 1.5rem;
}

.checklist-widget h2 {
  font-size: 0.95rem;
  font-weight: 700;
  color: #92400e;
  margin: 0 0 0.6rem;
}

.checklist-widget ul {
  margin: 0;
  padding-left: 1.25rem;
  color: #713f12;
  font-size: 0.85rem;
  line-height: 1.7;
}

.price-history {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 1.5rem;
}

.price-history h2 {
  font-size: 1rem;
  font-weight: 700;
  margin: 0 0 1rem;
}

.history-list {
  list-style: none;
  margin: 0 0 1.25rem;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.history-list li {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  align-items: center;
  font-size: 0.85rem;
  color: #374151;
  border-top: 1px solid #f3f4f6;
  padding-top: 0.5rem;
}

.history-list li:first-child {
  border-top: none;
  padding-top: 0;
}

.history-date {
  font-weight: 700;
  color: #d97706;
}

.history-vacant {
  background: #f3f4f6;
  color: #6b7280;
  font-size: 0.75rem;
  padding: 0.1rem 0.5rem;
  border-radius: 20px;
}

.history-note {
  color: #9ca3af;
}

.history-empty {
  color: #9ca3af;
  font-size: 0.85rem;
  margin-bottom: 1.25rem;
}

.history-form {
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
  border-top: 1px solid #f3f4f6;
  padding-top: 1.25rem;
}

.history-form input[type='number'] {
  width: 120px;
}

.history-form input[type='text'] {
  flex: 1;
  min-width: 160px;
}

.history-form input {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 0.5rem 0.7rem;
  font-size: 0.85rem;
}

.btn-secondary {
  background: #fef3c7;
  color: #92400e;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.85rem;
  cursor: pointer;
}

.btn-secondary:hover {
  background: #fde68a;
}

@media (max-width: 640px) {
  .field-row {
    flex-direction: column;
  }
}
</style>
