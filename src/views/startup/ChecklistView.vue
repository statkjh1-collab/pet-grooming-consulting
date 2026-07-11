<template>
  <main class="page">
    <h1 class="page-title">✅ 실행 체크리스트</h1>
    <p class="page-desc">1단계·1.5단계 액션을 체크하며 예창패 증빙을 쌓아갑니다.</p>

    <div v-if="store.loading" class="state-msg">불러오는 중...</div>
    <div v-else-if="store.error" class="state-msg error">
      {{ store.error }}<br />
      <span class="hint">백엔드(FastAPI)가 실행 중인지 확인하세요 (uvicorn main:app, 8000번 포트).</span>
    </div>

    <div v-else class="stage-list">
      <section v-for="stage in store.stages" :key="stage.id" class="stage-card">
        <div class="stage-head">
          <div>
            <h2>{{ stage.title }}</h2>
            <span class="period">{{ stage.period_label }}</span>
          </div>
          <div class="progress-wrap">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: stage.progress_pct + '%' }"></div>
            </div>
            <span class="progress-label">
              {{ stage.completed_items }}/{{ stage.total_items }} · {{ stage.progress_pct }}%
            </span>
          </div>
        </div>

        <div class="gate-signal">🚦 다음 단계 신호: {{ stage.gate_signal }}</div>

        <div v-for="group in stage.groups" :key="group.id" class="group-block">
          <h3>{{ group.title }}</h3>
          <ul class="item-list">
            <li v-for="item in group.items" :key="item.id" class="item" :class="{ done: item.done }">
              <label class="item-check">
                <input
                  type="checkbox"
                  :checked="item.done"
                  @change="onToggle(item, $event.target.checked)"
                />
              </label>
              <div class="item-body">
                <p class="item-title">{{ item.title }}</p>
                <p class="item-why">💡 {{ item.why }}</p>
                <p v-if="item.done_at" class="item-done-at">완료: {{ formatDate(item.done_at) }}</p>
                <textarea
                  class="item-memo"
                  placeholder="진행 메모..."
                  :value="item.memo"
                  @blur="onMemoBlur(item, $event.target.value)"
                ></textarea>
              </div>
            </li>
          </ul>
        </div>
      </section>
    </div>
  </main>
</template>

<script setup>
import { onMounted } from 'vue'
import { useChecklistStore } from '../../stores/startup/checklist'

const store = useChecklistStore()

onMounted(() => {
  store.load()
})

function onToggle(item, checked) {
  store.toggleDone(item.id, checked)
}

function onMemoBlur(item, value) {
  if (value === item.memo) return
  store.saveMemo(item.id, value)
}

function formatDate(iso) {
  const d = new Date(iso)
  return d.toLocaleString('ko-KR', { month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' })
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

.hint {
  font-size: 0.85rem;
  color: #9ca3af;
}

.stage-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.stage-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 1.5rem;
}

.stage-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}

.stage-head h2 {
  font-size: 1.15rem;
  font-weight: 700;
  margin: 0 0 0.25rem;
}

.period {
  font-size: 0.8rem;
  color: #92400e;
  background: #fef3c7;
  padding: 0.15rem 0.55rem;
  border-radius: 20px;
  font-weight: 600;
}

.progress-wrap {
  min-width: 160px;
}

.progress-bar {
  width: 160px;
  height: 8px;
  background: #f3f4f6;
  border-radius: 999px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #f59e0b;
  transition: width 0.2s;
}

.progress-label {
  display: block;
  margin-top: 0.3rem;
  font-size: 0.8rem;
  color: #6b7280;
  text-align: right;
}

.gate-signal {
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: 8px;
  padding: 0.6rem 0.9rem;
  font-size: 0.85rem;
  color: #713f12;
  margin-bottom: 1.25rem;
  line-height: 1.5;
}

.group-block {
  margin-bottom: 1.25rem;
}

.group-block h3 {
  font-size: 0.95rem;
  font-weight: 700;
  color: #374151;
  margin: 0 0 0.6rem;
  padding-left: 0.1rem;
}

.item-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.item {
  display: flex;
  gap: 0.6rem;
  border: 1px solid #f0f1f3;
  border-radius: 10px;
  padding: 0.75rem 0.9rem;
  transition: background 0.15s, border-color 0.15s;
}

.item.done {
  background: #f9fafb;
  border-color: #e5e7eb;
}

.item-check {
  padding-top: 0.15rem;
}

.item-check input {
  width: 18px;
  height: 18px;
  accent-color: #f59e0b;
  cursor: pointer;
}

.item-body {
  flex: 1;
  min-width: 0;
}

.item-title {
  margin: 0;
  font-size: 0.9rem;
  font-weight: 600;
  color: #111;
  line-height: 1.5;
}

.item.done .item-title {
  text-decoration: line-through;
  color: #9ca3af;
}

.item-why {
  margin: 0.3rem 0 0;
  font-size: 0.8rem;
  color: #6b7280;
  line-height: 1.5;
}

.item-done-at {
  margin: 0.3rem 0 0;
  font-size: 0.75rem;
  color: #d97706;
}

.item-memo {
  margin-top: 0.5rem;
  width: 100%;
  min-height: 40px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 0.4rem 0.55rem;
  font-size: 0.8rem;
  font-family: inherit;
  resize: vertical;
  box-sizing: border-box;
}

.item-memo:focus {
  outline: none;
  border-color: #f59e0b;
}
</style>
