<template>
  <main class="page">
    <h1 class="page-title">🎓 창업전 라이선스 준비</h1>
    <p class="page-desc">
      펫미용샵 창업의 첫걸음은 자격증 준비입니다. "애견관리사(반려동물관리사)" 자격증 과정에서
      배우는 내용을 정리했습니다. 항목마다 유튜브 영상으로 바로 학습할 수 있어요.
    </p>

    <div class="section">
      <h2>📖 자격증 개요</h2>
      <p class="desc-text">
        <strong>반려동물종합관리사</strong>는 한국애견연맹 등 관련 기관이 주관하는 민간자격으로, 반려동물의
        사육·분양·위탁관리·미용·훈련·영양관리 등 전문 지식을 검증합니다. 애완동물샵, 동물병원, 훈련소,
        애견유치원, 보호소 등에서 활용할 수 있습니다.
      </p>
    </div>

    <div class="section">
      <h2>📝 시험 과목 요약 (5과목)</h2>
      <p class="desc-text">과목당 100점 만점에 40점 이상, 평균 60점 이상이면 자격 취득이 가능합니다.</p>
      <ul>
        <li v-for="subject in subjects" :key="subject.name">
          <span class="tag">{{ subject.no }}과목</span> <strong>{{ subject.name }}</strong>
        </li>
      </ul>
    </div>

    <div class="section">
      <h2>▶️ 영상으로 배우는 실무 커리큘럼</h2>
      <p class="desc-text">각 카드를 누르면 해당 주제의 유튜브 영상을 바로 검색해서 볼 수 있습니다.</p>
      <div class="curriculum-grid">
        <div v-for="group in curriculum" :key="group.title" class="curriculum-card">
          <h3>{{ group.title }}</h3>
          <ul>
            <li v-for="topic in group.topics" :key="topic.name">
              <a :href="youtubeSearchUrl(topic.query)" target="_blank" rel="noopener noreferrer" class="topic-link">
                <span class="play-icon">▶</span> {{ topic.name }}
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div class="section">
      <h2>✅ 취득 요건 & 활동 분야</h2>
      <ul>
        <li>전체 강의 <strong>80% 이상 수강</strong> + 시험 <strong>60점 이상</strong> 통과 시 자격 취득</li>
        <li>활동 분야: 애완동물샵, 동물병원, 반려동물 훈련소, 애견유치원, 보호소 등</li>
        <li>업무 범위: 사육, 분양, 위탁관리, 교육, 미용, 보험, 장례 등</li>
      </ul>
    </div>

    <div class="notice">
      ⚠️ 유튜브 영상 링크는 검색 결과로 연결되며, 채널·영상의 정확성은 각 게시자에게 책임이 있습니다.
      전문 지식은 공식 자격 기관의 교재와 실습 교육을 함께 참고하세요.
    </div>

    <div class="section">
      <h2>🔗 참고 사이트</h2>
      <ul>
        <li><a href="https://www.thekkf.or.kr" target="_blank">한국애견연맹</a> — 반려동물종합관리사 공식 시험 안내</li>
        <li><a href="https://www.lli.or.kr" target="_blank">한국직업능력원격평생교육원</a> — 반려동물관리사 1급 과정</li>
        <li><a href="https://www.ili.or.kr" target="_blank">반려동물관리사 무료교육</a> — 애견훈련사 자격증 1·2급</li>
      </ul>
    </div>
  </main>
</template>

<script setup>
const subjects = [
  { no: 1, name: '반려동물의 품종 및 해부학' },
  { no: 2, name: '질병 관리 및 예방' },
  { no: 3, name: '개의 미용 관리' },
  { no: 4, name: '개의 훈련 관리' },
  { no: 5, name: '영양관리 및 개 미용학' },
]

const curriculum = [
  {
    title: '① 기초 이론',
    topics: [
      { name: '반려동물관리사 직업 소개', query: '반려동물관리사 자격증 소개' },
      { name: '반려동물 품종별 특성', query: '강아지 품종별 특성 설명' },
      { name: '견체학·해부학 기초', query: '강아지 해부학 기초 강의' },
    ],
  },
  {
    title: '② 행동 & 훈련',
    topics: [
      { name: '기본 동작 훈련', query: '강아지 기본 훈련 방법' },
      { name: '반려동물 케어링(돌봄) 기본', query: '강아지 케어링 돌봄 기본' },
      { name: '오비디언스·산책 교육', query: '강아지 오비디언스 산책 훈련' },
      { name: '행동학 이해', query: '강아지 행동학 이해' },
    ],
  },
  {
    title: '③ 건강 & 질병',
    topics: [
      { name: '외부기생충 관리', query: '강아지 외부기생충 관리' },
      { name: 'DHPPL 등 주요 질병', query: '강아지 DHPPL 예방접종 질병' },
      { name: '예방접종 스케줄', query: '강아지 예방접종 시기 종류' },
      { name: '응급 상황 대응', query: '강아지 응급처치 방법' },
    ],
  },
  {
    title: '④ 영양 & 실무',
    topics: [
      { name: '영양 관리 및 사료 급여', query: '강아지 사료 급여량 영양관리' },
      { name: '사육 환경 조성', query: '강아지 사육 환경 조성' },
      { name: '위탁관리 실무', query: '반려동물 위탁관리 펫시터' },
    ],
  },
  {
    title: '⑤ 미용이론',
    topics: [
      { name: '애견미용 기초 이론', query: '애견미용 기초 이론' },
      { name: '견종별 미용 스타일', query: '강아지 견종별 미용 스타일' },
      { name: '미용 도구 종류 및 사용법', query: '애견미용 도구 종류 사용법' },
      { name: '목욕 & 드라이 이론', query: '강아지 목욕 드라이 방법' },
    ],
  },
  {
    title: '⑥ 미용실기',
    topics: [
      { name: '가위질 기초', query: '애견미용 가위질 기초' },
      { name: '클리퍼 클리핑 기술', query: '애견미용 클리퍼 클리핑 기술' },
      { name: '얼굴·발 미용 실습', query: '강아지 얼굴 발 미용 실습' },
      { name: '전신 커트 스타일링', query: '강아지 전신 커트 스타일링' },
    ],
  },
]

function youtubeSearchUrl(query) {
  return `https://www.youtube.com/results?search_query=${encodeURIComponent(query)}`
}
</script>

<style scoped>
.desc-text {
  color: #374151;
  line-height: 1.6;
  margin: 0 0 1rem;
}

.notice {
  background: #fef9c3;
  border: 1px solid #fde047;
  border-radius: 10px;
  padding: 1rem 1.25rem;
  font-size: 0.9rem;
  color: #713f12;
  margin-top: 0.5rem;
}

.section a {
  color: #d97706;
  text-decoration: underline;
}

.curriculum-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.curriculum-card {
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: 10px;
  padding: 1rem 1.25rem;
}

.curriculum-card h3 {
  margin: 0 0 0.6rem;
  font-size: 0.95rem;
  font-weight: 700;
  color: #92400e;
}

.curriculum-card ul {
  margin: 0;
  padding-left: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  font-size: 0.875rem;
  line-height: 1.5;
}

.topic-link {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  color: #374151 !important;
  text-decoration: none !important;
  padding: 0.35rem 0.5rem;
  border-radius: 6px;
  transition: background 0.15s, color 0.15s;
}

.topic-link:hover {
  background: #fef3c7;
  color: #d97706 !important;
}

.play-icon {
  color: #ef4444;
  font-size: 0.7rem;
}

@media (max-width: 640px) {
  .curriculum-grid {
    grid-template-columns: 1fr;
  }
}
</style>
