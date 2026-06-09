<script setup>
import { ref } from 'vue'

const faqs = [
  { q: '자격증 없이도 애견 미용샵을 운영할 수 있나요?', a: '네, 가능합니다. 현재 법적으로 자격증 없이도 동물미용업 신고 후 운영할 수 있습니다. 다만 자격증이 있으면 고객 신뢰도와 마케팅에 유리합니다.' },
  { q: '동물미용업 신고는 어디서 하나요?', a: '관할 시·군·구청 동물보호과에서 신고합니다. 구비서류로는 신분증, 임대차계약서, 위생교육 이수증 등이 필요합니다.' },
  { q: '초기 창업 비용은 얼마나 드나요?', a: '입지와 규모에 따라 다르지만 소형 미용샵(10~15평) 기준 인테리어 포함 3,000~6,000만원 수준으로 보시면 됩니다. 중고 장비 활용 시 절감 가능합니다.' },
  { q: '1인 운영이 가능한가요?', a: '네, 처음에는 1인 운영으로 시작하는 분들이 많습니다. 하루 5~8마리가 1인 기준 적정 수입니다. 매출이 안정되면 직원 채용을 고려하세요.' },
  { q: '네이버 플레이스 등록은 필수인가요?', a: '필수는 아니지만 강력히 권장합니다. 지역 검색 시 가장 먼저 노출되는 채널이기 때문에 초기 고객 유입에 큰 역할을 합니다. 무료로 등록할 수 있습니다.' },
  { q: '수익이 나기까지 얼마나 걸리나요?', a: '보통 오픈 후 3~6개월이 손익분기점 도달 평균 기간입니다. 입지와 마케팅 노력에 따라 크게 달라지므로 최소 6개월치 운영 자금을 확보하고 시작하세요.' },
]

const open = ref(null)

function toggle(i) {
  open.value = open.value === i ? null : i
}
</script>

<template>
  <main class="page">
    <h1 class="page-title">❓ 자주 묻는 질문</h1>
    <p class="page-desc">창업 준비 중 가장 많이 나오는 질문들을 모았습니다.</p>

    <div class="faq-list">
      <div v-for="(f, i) in faqs" :key="i" class="faq-item" :class="{ open: open === i }">
        <button class="faq-q" @click="toggle(i)">
          <span>{{ f.q }}</span>
          <span class="arrow">{{ open === i ? '▲' : '▼' }}</span>
        </button>
        <div v-if="open === i" class="faq-a">{{ f.a }}</div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.faq-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.faq-item {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  overflow: hidden;
}

.faq-item.open {
  border-color: #f59e0b;
}

.faq-q {
  width: 100%;
  background: none;
  border: none;
  padding: 1.1rem 1.25rem;
  text-align: left;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  color: #111;
}

.arrow {
  font-size: 0.75rem;
  color: #9ca3af;
  flex-shrink: 0;
}

.faq-a {
  padding: 0 1.25rem 1.1rem;
  color: #374151;
  font-size: 0.9rem;
  line-height: 1.7;
  border-top: 1px solid #f3f4f6;
  padding-top: 0.9rem;
}
</style>
