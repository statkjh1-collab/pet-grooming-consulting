<template>
  <main class="page">
    <div class="page-head">
      <div>
        <h1 class="page-title">🧾 증빙 수집함</h1>
        <p class="page-desc">예창패 사업계획서에 넣을 근거를 유형별로 모읍니다.</p>
      </div>
      <button class="btn-primary" @click="formOpen = !formOpen">{{ formOpen ? '닫기' : '+ 증빙 추가' }}</button>
    </div>

    <form v-if="formOpen" class="form" @submit.prevent="onCreate">
      <div class="field">
        <label>유형</label>
        <select v-model="form.type">
          <option v-for="t in TYPES" :key="t" :value="t">{{ t }}</option>
        </select>
      </div>
      <div class="field">
        <label>내용</label>
        <textarea v-model="form.content" rows="4" placeholder="무엇을 확인했는지, 왜 근거가 되는지" required></textarea>
      </div>
      <div class="field-row">
        <div class="field">
          <label>출처</label>
          <input v-model="form.source" type="text" placeholder="예: 네이버카페 '애견미용사 날다'" />
        </div>
        <div class="field">
          <label>날짜</label>
          <input v-model="form.date" type="date" required />
        </div>
      </div>
      <div class="field">
        <label>첨부 (URL, 선택)</label>
        <input v-model="form.attachment" type="text" placeholder="캡처·게시글 링크 등" />
      </div>
      <div class="form-actions">
        <button type="submit" class="btn-primary">저장</button>
      </div>
      <p v-if="saveError" class="save-error">{{ saveError }}</p>
    </form>

    <div class="filter-row">
      <button class="filter-chip" :class="{ active: typeFilter === '' }" @click="setFilter('')">전체</button>
      <button
        v-for="t in TYPES"
        :key="t"
        class="filter-chip"
        :class="{ active: typeFilter === t }"
        @click="setFilter(t)"
      >
        {{ t }}
      </button>
    </div>

    <div v-if="store.loading" class="state-msg">불러오는 중...</div>
    <div v-else-if="store.error" class="state-msg error">{{ store.error }}</div>
    <div v-else-if="store.items.length === 0" class="state-msg">아직 등록된 증빙이 없습니다.</div>

    <ul v-else class="evidence-list">
      <li v-for="item in store.items" :key="item.id" class="evidence-card">
        <div class="evidence-head">
          <span class="tag">{{ item.type }}</span>
          <span class="evidence-date">{{ item.date }}</span>
          <button class="delete-btn" @click="onDelete(item.id)" aria-label="삭제">삭제</button>
        </div>
        <p class="evidence-content">{{ item.content }}</p>
        <div class="evidence-meta">
          <span v-if="item.source">출처: {{ item.source }}</span>
          <a v-if="item.attachment" :href="item.attachment" target="_blank" rel="noopener noreferrer">첨부 보기</a>
        </div>
      </li>
    </ul>
  </main>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useEvidenceStore } from '../../stores/startup/evidence'

const TYPES = ['고객이력', '앱사용후기', '컨설팅후기', '스튜디오수요', '시장데이터', '기타']

const store = useEvidenceStore()
const typeFilter = ref('')
const formOpen = ref(false)
const saveError = ref('')

const form = reactive({
  type: '시장데이터',
  content: '',
  source: '',
  date: new Date().toISOString().slice(0, 10),
  attachment: '',
})

onMounted(() => {
  store.load()
})

function setFilter(type) {
  typeFilter.value = type
  store.load(type || undefined)
}

async function onCreate() {
  saveError.value = ''
  try {
    await store.createItem({ ...form })
    form.content = ''
    form.source = ''
    form.attachment = ''
    formOpen.value = false
    if (typeFilter.value && typeFilter.value !== form.type) {
      // 현재 필터와 다른 유형으로 등록한 경우 필터를 초기화해 방금 등록한 항목이 보이게 함
      setFilter('')
    }
  } catch (e) {
    saveError.value = e.message
  }
}

async function onDelete(id) {
  if (!confirm('이 증빙을 삭제할까요?')) return
  await store.deleteItem(id)
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

.btn-primary {
  background: #f59e0b;
  color: #fff;
  border: none;
  padding: 0.6rem 1.1rem;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  white-space: nowrap;
}

.btn-primary:hover {
  background: #d97706;
}

.form {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin: 1.25rem 0;
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

.field input,
.field select,
.field textarea {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 0.6rem 0.75rem;
  font-size: 0.9rem;
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

.form-actions {
  display: flex;
}

.save-error {
  color: #b91c1c;
  font-size: 0.85rem;
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 1.25rem 0;
}

.filter-chip {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  padding: 0.35rem 0.9rem;
  font-size: 0.85rem;
  color: #6b7280;
  cursor: pointer;
}

.filter-chip:hover {
  border-color: #f59e0b;
  color: #d97706;
}

.filter-chip.active {
  background: #fef3c7;
  border-color: #fde68a;
  color: #d97706;
  font-weight: 700;
}

.state-msg {
  padding: 2rem;
  text-align: center;
  color: #6b7280;
}

.state-msg.error {
  color: #b91c1c;
}

.evidence-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.evidence-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.1rem 1.3rem;
}

.evidence-head {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 0.5rem;
}

.evidence-date {
  font-size: 0.78rem;
  color: #9ca3af;
}

.delete-btn {
  margin-left: auto;
  background: none;
  border: none;
  color: #9ca3af;
  font-size: 0.78rem;
  cursor: pointer;
  padding: 0.2rem 0.4rem;
}

.delete-btn:hover {
  color: #b91c1c;
}

.evidence-content {
  margin: 0 0 0.6rem;
  font-size: 0.9rem;
  color: #111;
  line-height: 1.6;
  white-space: pre-wrap;
}

.evidence-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.8rem;
  color: #6b7280;
}

.evidence-meta a {
  color: #d97706;
  text-decoration: underline;
}

@media (max-width: 640px) {
  .field-row {
    flex-direction: column;
  }
}
</style>
