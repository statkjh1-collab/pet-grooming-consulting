<template>
  <main class="home">
    <section class="hero">
      <div class="hero-inner">
        <h1>🐾 펫미용샵 창업<br>이제 체계적으로 준비하세요</h1>
        <p>인허가부터 운영, 마케팅, 재무까지<br>창업의 모든 단계를 안내합니다.</p>
        <div class="hero-btns">
          <RouterLink to="/pre-open" class="btn-primary">창업 준비 시작하기</RouterLink>
          <RouterLink to="/faq" class="btn-secondary">자주 묻는 질문</RouterLink>
        </div>
      </div>
    </section>

    <section class="menu-grid page">
      <RouterLink v-for="m in menus" :key="m.path" :to="m.path" class="menu-card">
        <span class="menu-icon">{{ m.icon }}</span>
        <strong>{{ m.name }}</strong>
        <p>{{ m.desc }}</p>
      </RouterLink>
    </section>
  </main>
</template>

<script setup>
import { RouterLink } from 'vue-router'

const menus = [
  { icon: '📋', path: '/pre-open', name: '사업장 오픈 전', desc: '인허가, 자격증, 입지 선정, 초기 비용 등 오픈 전 필수 체크리스트' },
  { icon: '🏪', path: '/operations', name: '미용샵 운영 관리', desc: '고객 관리, 예약 시스템, 직원 채용 및 일상 운영 노하우' },
  { icon: '📣', path: '/marketing', name: '마케팅 & 홍보', desc: 'SNS, 카카오 채널, 네이버 플레이스 활용법' },
  { icon: '💰', path: '/finance', name: '수익 & 재무 관리', desc: '가격 책정, 매출 관리, 세금 신고 가이드' },
  { icon: '🏛️', path: '/support', name: '국가 창업 지원', desc: '정부 지원금, 저금리 대출, 세제 혜택 등 활용 가능한 지원 총정리' },
  { icon: '❓', path: '/faq', name: '자주 묻는 질문', desc: '창업자들이 가장 많이 묻는 질문 모음' },
]
</script>

<style scoped>
.hero {
  background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
  padding: 5rem 1.5rem;
  text-align: center;
}

.hero-inner {
  max-width: 600px;
  margin: 0 auto;
}

.hero h1 {
  font-size: 2.2rem;
  font-weight: 900;
  line-height: 1.3;
  margin-bottom: 1rem;
}

.hero p {
  color: #6b7280;
  font-size: 1.1rem;
  line-height: 1.7;
  margin-bottom: 2rem;
}

.hero-btns {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-primary {
  background: #f59e0b;
  color: #fff;
  padding: 0.8rem 1.75rem;
  border-radius: 8px;
  font-weight: 700;
  font-size: 1rem;
}

.btn-primary:hover { background: #d97706; }

.btn-secondary {
  background: #fff;
  color: #374151;
  padding: 0.8rem 1.75rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  border: 1px solid #e5e7eb;
}

.btn-secondary:hover { background: #f3f4f6; }

.menu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1rem;
  padding-top: 2.5rem;
  padding-bottom: 2.5rem;
}

.menu-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  color: #111;
  transition: box-shadow 0.2s, border-color 0.2s;
}

.menu-card:hover {
  border-color: #f59e0b;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.15);
}

.menu-icon { font-size: 2rem; }

.menu-card strong { font-size: 1rem; font-weight: 700; }

.menu-card p { color: #6b7280; font-size: 0.875rem; margin: 0; line-height: 1.5; }
</style>
