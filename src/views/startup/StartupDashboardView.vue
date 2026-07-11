<template>
  <main class="page">
    <h1 class="page-title">🚀 창업 관리 (Startup Tracker)</h1>
    <p class="page-desc">예비창업패키지를 목표로 준비 과정을 한눈에 관리합니다.</p>

    <section class="principles">
      <h2>이 1년의 3원칙</h2>
      <ol>
        <li>
          <strong>사업자등록 아직 X</strong> — 예비창업자 자격을 지켜야 예창패 지원 가능. 등록은 선정 후에.
        </li>
        <li>
          <strong>프리랜서 수입 유지</strong> — 안전판이 있을 때가 실험하기 가장 좋은 때. 전업 전환 서두르지 않기.
        </li>
        <li>
          <strong>목표는 매출 아닌 '증거'</strong> — "돈 내고 쓰는 사람이 있다"는 증거 하나가 사업계획서를 다른
          급으로 만든다.
        </li>
      </ol>
    </section>

    <section class="menu-grid">
      <RouterLink to="/startup/checklist" class="menu-card">
        <span class="menu-icon">✅</span>
        <strong>실행 체크리스트</strong>
        <p>1단계·1.5단계 액션 트래커</p>
      </RouterLink>
      <RouterLink to="/startup/properties" class="menu-card">
        <span class="menu-icon">🏘️</span>
        <strong>상권·입지</strong>
        <p>매물 비교, 시세 이력, 주변 시설</p>
      </RouterLink>
      <div class="menu-card disabled">
        <span class="menu-icon">📁</span>
        <strong>산출물 보관함</strong>
        <p>사업계획서·커리큘럼 등 자료 정리 (준비중)</p>
      </div>
      <div class="menu-card disabled">
        <span class="menu-icon">🧾</span>
        <strong>증빙 수집함</strong>
        <p>예창패용 근거 자료 모음 (준비중)</p>
      </div>
      <div class="menu-card disabled">
        <span class="menu-icon">📚</span>
        <strong>커리큘럼 운영</strong>
        <p>5주 AI 활용 과정 진행 관리 (준비중)</p>
      </div>
      <div class="menu-card disabled">
        <span class="menu-icon">💡</span>
        <strong>아이디어/메모</strong>
        <p>떠오른 생각 저장 (준비중)</p>
      </div>
    </section>
  </main>
</template>

<script setup></script>

<style scoped>
.principles {
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: 14px;
  padding: 1.5rem 1.75rem;
  margin-bottom: 2rem;
}

.principles h2 {
  font-size: 1rem;
  font-weight: 700;
  color: #92400e;
  margin: 0 0 0.75rem;
}

.principles ol {
  margin: 0;
  padding-left: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  color: #713f12;
  font-size: 0.9rem;
  line-height: 1.6;
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1rem;
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
  text-decoration: none;
  transition: box-shadow 0.2s, border-color 0.2s;
}

.menu-card:not(.disabled):hover {
  border-color: #f59e0b;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.15);
}

.menu-card.disabled {
  color: #9ca3af;
  cursor: not-allowed;
}

.menu-icon {
  font-size: 1.75rem;
}

.menu-card strong {
  font-size: 0.95rem;
  font-weight: 700;
}

.menu-card p {
  margin: 0;
  font-size: 0.8rem;
  color: #6b7280;
  line-height: 1.5;
}

.menu-card.disabled p {
  color: #b0b3ba;
}
</style>
