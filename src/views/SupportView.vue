<template>
  <main class="page">
    <h1 class="page-title">🏛️ 국가 창업 지원</h1>
    <p class="page-desc">2026년 기준, 펫미용샵 창업 시 활용할 수 있는 정부 지원 프로그램을 정리했습니다.</p>

    <div class="section">
      <h2>💰 자금 지원</h2>
      <ul>
        <li><strong>소상공인 정책자금</strong> — 소상공인시장진흥공단, 저금리 창업·운영 자금 대출</li>
        <li><strong>청년전용창업자금</strong> — 만 39세 이하, 연 2.5% 고정금리, 최대 1억원 대출</li>
        <li><strong>중소벤처기업진흥공단 정책자금</strong> — 2026년 총 4.43조원 규모 공급</li>
        <li><strong>희망리턴패키지</strong> — 재창업 시 최대 2,000만원 지원, 점포 철거비 최대 600만원</li>
      </ul>
    </div>

    <div class="section">
      <h2>🎓 교육 & 컨설팅 지원</h2>
      <ul>
        <li><strong>청년창업사관학교</strong> — 만 39세 이하, 사업비 최대 1억원(70% 이내) + 공간·코칭 지원</li>
        <li><strong>예비창업패키지</strong> — 창업진흥원, 사업화 자금 + 멘토링 지원</li>
        <li><strong>소상공인 무료 경영컨설팅</strong> — 소상공인시장진흥공단 전국 센터 방문 신청</li>
        <li><strong>세무 무료 상담</strong> — 전국 세무서에서 창업 초기 세금 상담 무료 제공</li>
      </ul>
    </div>

    <div class="section">
      <h2>🤖 디지털 전환 지원</h2>
      <ul>
        <li><strong>혁신 소상공인 AI 활용 지원사업</strong> — 2026년 신규, AI 도구 활용 비용 절감 지원</li>
        <li><strong>온라인 판로 지원</strong> — 스마트스토어·SNS 마케팅 교육 및 광고비 지원</li>
        <li><strong>키오스크·예약시스템 도입 지원</strong> — 지자체별 디지털화 지원금 별도 확인 필요</li>
      </ul>
    </div>

    <div class="section">
      <h2>🧾 세제 혜택</h2>
      <ul>
        <li><strong>청년 창업 세액감면</strong> — 만 34세 이하 창업 시 최대 5년간 소득세 감면</li>
        <li><strong>영세·중소가맹점 카드 수수료 우대</strong> — 연매출 30억 이하 시 우대 수수료 자동 적용</li>
        <li><strong>간이과세자 부가세 혜택</strong> — 연매출 1억400만원 이하 시 부가세 납부 경감</li>
      </ul>
    </div>

    <div class="section">
      <h2>🔗 신청 & 정보 확인 사이트</h2>
      <ul>
        <li><a href="https://www.k-startup.go.kr" target="_blank">K-Startup</a> — 창업진흥원 통합 지원 포털</li>
        <li><a href="https://www.smes.go.kr" target="_blank">소상공인시장진흥공단</a> — 소상공인 지원사업 공고</li>
        <li><a href="https://www.kosmes.or.kr" target="_blank">중소벤처기업진흥공단</a> — 정책자금 융자 신청</li>
        <li><a href="https://www.bizinfo.go.kr" target="_blank">기업마당(bizinfo)</a> — 정부 지원사업 통합 검색</li>
        <li><a href="https://www.gov.kr" target="_blank">정부24</a> — 청년전용창업자금 등 민원 신청</li>
      </ul>
    </div>

    <div class="notice">
      ⚠️ 지원 사업은 매년 공고 일정과 조건이 변경됩니다. 반드시 각 기관 공식 사이트에서 최신 공고를 확인하세요.
    </div>

    <h2 class="table-title">📋 2026년 주요 사업 공고 현황</h2>
    <p class="page-desc" style="margin-bottom:1rem">출처: <a href="https://www.smes.go.kr/main/sportsBsnsPolicy" target="_blank">중소벤처24 사업공고</a></p>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>사업명</th>
            <th>지원 대상</th>
            <th>주요 지원 내용</th>
            <th>신청 기간</th>
            <th>지원기관</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in announcements" :key="item.name">
            <td><a :href="item.url" target="_blank">{{ item.name }}</a></td>
            <td>{{ item.target }}</td>
            <td>{{ item.content }}</td>
            <td>{{ item.period }}</td>
            <td>{{ item.org }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </main>
</template>

<script setup>
const announcements = [
  {
    name: '소상공인 지원사업 통합 공고',
    url: 'https://www.smes.go.kr/main/sportsBsnsPolicy/view?viewPblancSeq=238669530',
    target: '예비창업자, 소상공인, 폐업 소상공인',
    content: '기업가형 육성, 성장지원, 디지털 역량강화, 재기지원 등 7개 분야',
    period: '세부사업별 상이',
    org: '중소벤처기업부',
  },
  {
    name: '소상공인 정책자금 융자사업',
    url: 'https://www.smes.go.kr/main/sportsBsnsPolicy/view?viewPblancSeq=238669527',
    target: '소상공인기본법 해당 소상공인',
    content: '일반·긴급 경영안정자금, 재도전특별자금, 청년고용연계자금, 성장기반자금 등',
    period: '세부사업별 상이',
    org: '소상공인시장진흥공단',
  },
  {
    name: '[충북] 소상공인 육성자금 지원',
    url: 'https://www.smes.go.kr/main/sportsBsnsPolicy/view?viewPblancSeq=238915105',
    target: '충북 도내 소상공인',
    content: '신규창업 초기 운전자금, 시설개보수자금 (최대 7천만원)',
    period: '예산 소진시까지',
    org: '충청북도',
  },
  {
    name: '디지털커머스 전문기관 (소담스퀘어 광주)',
    url: 'https://www.smes.go.kr/main/sportsBsnsPolicy/view?viewPblancSeq=238839548',
    target: '디지털 전환 필요 소상공인',
    content: '디지털 콘텐츠 제작, 온라인시장 진출, 라이브커머스 지원 (연 700개사)',
    period: '2025.12.31 ~ 2026.12.31',
    org: '소상공인시장진흥공단',
  },
  {
    name: '에코스타트업 지원사업 (일반창업)',
    url: 'https://www.smes.go.kr/main/sportsBsnsPolicy/view?viewPblancSeq=249483459',
    target: '녹색산업 예비창업자 및 창업기업',
    content: '창업 자금 및 역량강화 프로그램 지원',
    period: '2026.02.19 ~ 2026.03.03',
    org: '창업진흥원',
  },
  {
    name: '경기창업공모 도약리그',
    url: 'https://www.smes.go.kr/main/sportsBsnsPolicy/view?viewPblancSeq=253062986',
    target: '경기도 창업자 및 초기기업',
    content: '창업 경진대회 및 사업화 지원',
    period: '2026.06.08 ~ 2026.06.30',
    org: '경기도경제과학진흥원',
  },
]
</script>

<style scoped>
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

.table-title {
  font-size: 1.2rem;
  font-weight: 700;
  margin: 2rem 0 0.5rem;
}

.table-wrap {
  overflow-x: auto;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
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
  padding: 0.85rem 1rem;
  text-align: left;
  font-weight: 700;
  color: #92400e;
  white-space: nowrap;
}

td {
  padding: 0.8rem 1rem;
  border-top: 1px solid #f3f4f6;
  color: #374151;
  vertical-align: top;
  line-height: 1.5;
}

tbody tr:hover {
  background: #fffbeb;
}

td a {
  color: #d97706;
  text-decoration: underline;
  font-weight: 600;
}
</style>
