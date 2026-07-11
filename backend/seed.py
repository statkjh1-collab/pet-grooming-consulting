"""체크리스트 초기 데이터 주입 스크립트. 이미 데이터가 있으면 아무 것도 하지 않는다.

실행: python seed.py  (backend/ 디렉토리 안에서)
"""

from datetime import date

from database import Base, SessionLocal, engine
from models import POI, ChecklistGroup, ChecklistItem, Property, Stage

STAGE1_GROUPS = [
    {
        "title": "데이터의 씨앗 뿌리기",
        "items": [
            {
                "title": "프리랜서 고객의 미용 이력을 실제로 기록하기 시작 (견종·모질·시술·특이사항·재방문)",
                "why": "나중에 '우리만의 데이터' 자산의 출발점. 지금 안 쌓으면 나중에 못 만든다.",
            },
            {
                "title": "고객 동의 문구 한 줄 만들어 사진·정보 기록 시 동의받기",
                "why": "개인정보·저작권 리스크를 처음부터 깔끔하게.",
            },
        ],
    },
    {
        "title": "MVP(예약 앱) 실전 검증",
        "items": [
            {
                "title": "만들고 있는 예약 앱을 본인 프리랜서 고객에게 실제로 써보게 하기",
                "why": "'실사용 검증된 MVP'가 되면 예창패 실현가능성 점수 급상승.",
            },
            {
                "title": "사용하며 나온 불편·버그·요청을 메모로 남기기 (개선 로그)",
                "why": "개선 이력 자체가 '실행력' 증빙이 된다.",
            },
        ],
    },
    {
        "title": "커리큘럼 반응 테스트",
        "items": [
            {
                "title": "초보 미용사 1~2명에게 AI 활용 커리큘럼을 무료/소액으로 테스트",
                "why": "'사람들이 진짜 이걸 원하나?'를 돈 안 들이고 확인하는 단계.",
            },
            {
                "title": "테스트 후 짧은 후기·만족도 한 줄씩 받기",
                "why": "예창패 사업계획서에 넣을 수 있는 첫 고객 반응.",
            },
        ],
    },
    {
        "title": "예창패 준비 (등록은 아직 X)",
        "items": [
            {
                "title": "K-Startup(k-startup.go.kr) 가입 + 예비창업패키지 공고 알림 설정",
                "why": "다음 사이클(2027년 초 예상) 공고를 놓치지 않기 위해.",
            },
            {
                "title": "주요 협회(KKF·KDA 등)에 연간 미용 자격증 배출 인원 문의 (전화 1통)",
                "why": "SOM 시장 근거를 숫자로 보강 — 발표 방어력이 크게 올라감.",
            },
        ],
    },
]

STAGE1_5_GROUPS = [
    {
        "title": "컨설팅, 1건이라도 유료로",
        "items": [
            {
                "title": "지인 창업자 또는 온라인으로 창업 컨설팅 1건을 실제로 돈 받고 진행",
                "why": "'무료로 도와줌'과 '돈 받고 함'은 완전히 다른 증거. 유료 고객 1명 = 사업 검증.",
            },
            {
                "title": "컨설팅 결과를 간단한 후기/사례로 정리",
                "why": "다음 고객 유치 자료이자 예창패 트랙레코드.",
            },
        ],
    },
    {
        "title": "공유 스튜디오, '하루'만 열어보기",
        "items": [
            {
                "title": "미용학원 강의실이나 지인 샵을 시간제로 빌려 '공유 스튜디오'를 하루 실험 운영",
                "why": "본인이 겪은 그 불편을 역이용. 큰 임대 계약 없이 수요를 실측한다.",
            },
            {
                "title": "참여한 초보 미용사에게 대여료를 소액이라도 받아보기",
                "why": "'공유 스튜디오에 돈 낼 사람이 있나?'라는 심사위원 핵심 질문에 대한 실증 답변.",
            },
            {
                "title": "하루 실험의 신청자 수·만족도·재참여 의향 기록",
                "why": "수요 데이터 = 사업계획서 시장성 파트의 강력한 근거.",
            },
        ],
    },
    {
        "title": "증거 묶고 사업계획서 채우기",
        "items": [
            {
                "title": "1단계·1.5단계에서 모은 것(이력 데이터·앱 사용·컨설팅 후기·스튜디오 수요)을 한 폴더에 정리",
                "why": "흩어진 증거를 모으면 그게 곧 사업계획서 별첨이 된다.",
            },
            {
                "title": "기존 예창패 사업계획서 초안의 빈칸(매출 실적·상권·팀 경력)을 실제 숫자로 교체",
                "why": "가정이 아니라 '해봤더니 이랬다'로 바뀌면 서류 설득력이 완전히 달라진다.",
            },
        ],
    },
]

STAGES = [
    {
        "key": "stage1",
        "title": "1단계 — 돈 안 들이고 지금 당장 되는 것",
        "period_label": "0~6개월",
        "gate_signal": "앱을 실제로 써본 고객이 있고, 커리큘럼을 테스트해본 사람이 있으며, 미용 이력 기록이 쌓이기 시작했다.",
        "groups": STAGE1_GROUPS,
    },
    {
        "key": "stage1_5",
        "title": "1.5단계 — 작게, 돈 받아보기",
        "period_label": "6~12개월",
        "gate_signal": "유료 고객(컨설팅)과 유료 참여자(스튜디오)가 각각 최소 1건 이상 생겼고, 사업계획서를 실제 데이터로 채웠다. → 2단계(공간 확보 + 예창패 지원) 준비 완료.",
        "groups": STAGE1_5_GROUPS,
    },
]


PROPERTIES = [
    {
        "name": "시장 근처 (구 프랭크버거)",
        "landmark": "시장 인근, 구 프랭크버거 자리",
        "area_pyeong": 9.5,
        "deposit": 2000,
        "monthly_rent": 140,
        "negotiable": False,
        "expandable": False,
        "water_supply": "미확인",
        "status": "관심",
        "visited_at": date(2026, 7, 11),
        "memo": "9~10평. 층수·권리금·관리비 미확인.",
    },
    {
        "name": "역대급피자 건너편",
        "landmark": "역대급피자 맞은편",
        "area_pyeong": 9,
        "deposit": 2000,
        "monthly_rent": 120,
        "negotiable": False,
        "expandable": False,
        "water_supply": "미확인",
        "status": "관심",
        "visited_at": date(2026, 7, 11),
        "memo": "평당 월세 최저(약 13.3만). 다만 9평은 공유 스튜디오 모델에는 협소.",
    },
    {
        "name": "사과나무학원 1층",
        "landmark": "사과나무학원 건물 1층",
        "floor": 1,
        "area_pyeong": 12,
        "deposit": 2000,
        "monthly_rent": 200,
        "negotiable": True,
        "expandable": True,
        "expansion_note": "1구역(12평)으로 시작, 최대 3구역까지 확장 가능",
        "prev_business": "인테리어 → 안경점",
        "water_supply": "미확인",
        "status": "유력",
        "visited_at": date(2026, 7, 11),
        "memo": (
            "학원 1층 = 학부모 유동인구(반려견 보호자층과 겹침). 1층 접근성 우수. "
            "단계적 확장 가능한 유일한 물건 → 사업 로드맵(직영샵→공유스튜디오→교육공간)과 구조 일치. "
            "주의: 이전 업종이 물을 안 쓰는 업종(인테리어/안경점)이라 급배수 공사 필요 가능성 높음. "
            "안경점이 나간 이유(임대료 부담인지 유동인구 부족인지) 인근 상인에게 확인 필요."
        ),
    },
]

POIS = [
    # 응급 대응 체계
    {
        "name": "우장산동물의료센터",
        "type": "동물병원_주간",
        "address": "강서로 282",
        "hours": "10~20시",
        "relation": "응급대응",
        "note": "상권 한복판. 도보권 1차 대응처",
    },
    {
        "name": "다나동물병원",
        "type": "동물병원_주간",
        "address": "강서로 254",
        "hours": "10~20시(일 휴무)",
        "rating": 4.9,
        "relation": "응급대응",
        "note": "평점 4.9(19건). 과잉진료 없다는 평 다수",
    },
    {
        "name": "율동물의료센터",
        "type": "동물병원_24시",
        "address": "공항대로 228",
        "hours": "24시간",
        "relation": "응급대응",
        "note": "발산역 인근. 대형 장비 보유",
    },
    {
        "name": "아프리카 동물 메디컬센터",
        "type": "동물병원_24시",
        "address": "공항대로 335",
        "hours": "24시간",
        "rating": 3.7,
        "relation": "응급대응",
        "note": "평점 3.7(99건)",
    },
    {
        "name": "24시연동물의료센터",
        "type": "동물병원_24시",
        "address": "화곡로 191",
        "hours": "24시간",
        "relation": "응급대응",
        "note": "남쪽 백업",
    },
    # 수요 파이프라인
    {
        "name": "탑애견미용학원",
        "type": "미용학원",
        "address": "화곡동 광영빌딩 2층",
        "relation": "수요파이프라인",
        "note": (
            "공동대표(배우자)가 자격증을 취득한 학원. 지리적 근접 + 실제 인적 네트워크. "
            "수료생 = 공유 스튜디오 타깃 고객. 하루 실험 운영 시 참가자 모집처"
        ),
    },
    # 제휴 후보
    {
        "name": "커밍커밍",
        "type": "애견카페",
        "address": "강서로 385",
        "relation": "제휴후보",
        "note": "발산역 북단. 유치원 겸업, 평판 좋음",
    },
    {
        "name": "그로우독 애견유치원 호텔",
        "type": "유치원호텔",
        "address": "까치산로 75",
        "relation": "제휴후보",
        "note": "유치원+호텔",
    },
    {
        "name": "투퍼피강서점",
        "type": "유치원호텔",
        "address": "화곡동",
        "relation": "제휴후보",
        "note": "",
    },
    # 경쟁·수요 신호
    {
        "name": "견생낭품 24시 무인펫샵",
        "type": "펫샵",
        "address": "강서로 349 (발산역)",
        "hours": "24시간",
        "relation": "수요파이프라인",
        "note": "무인 = 미용 경쟁자 아님. 펫 수요 존재의 증거",
    },
    {
        "name": "개밥파는고양이 우장산역점",
        "type": "펫샵",
        "address": "강서로 211",
        "hours": "24시간",
        "relation": "수요파이프라인",
        "note": "24시간. 상권 내 반려동물 소비 확인",
    },
    {
        "name": "애견미용 salon 티엔독",
        "type": "경쟁미용실",
        "address": "가로공원로 208",
        "relation": "경쟁",
        "note": "상권 남쪽(화곡 방향)에 위치",
    },
]


def seed_checklist(db):
    if db.query(Stage).count() > 0:
        print("체크리스트 시드 데이터가 이미 있습니다. 건너뜁니다.")
        return

    for stage_order, stage_data in enumerate(STAGES):
        stage = Stage(
            key=stage_data["key"],
            title=stage_data["title"],
            period_label=stage_data["period_label"],
            gate_signal=stage_data["gate_signal"],
            order=stage_order,
        )
        db.add(stage)
        db.flush()

        for group_order, group_data in enumerate(stage_data["groups"]):
            group = ChecklistGroup(stage_id=stage.id, title=group_data["title"], order=group_order)
            db.add(group)
            db.flush()

            for item_order, item_data in enumerate(group_data["items"]):
                db.add(
                    ChecklistItem(
                        group_id=group.id,
                        title=item_data["title"],
                        why=item_data["why"],
                        order=item_order,
                    )
                )

    print("체크리스트 시드 데이터 생성 완료.")


def seed_properties(db):
    if db.query(Property).count() > 0:
        print("매물 시드 데이터가 이미 있습니다. 건너뜁니다.")
        return

    for prop_data in PROPERTIES:
        db.add(Property(**prop_data))

    print("매물 시드 데이터 생성 완료.")


def seed_pois(db):
    if db.query(POI).count() > 0:
        print("주변 시설 시드 데이터가 이미 있습니다. 건너뜁니다.")
        return

    for poi_data in POIS:
        db.add(POI(**poi_data))

    print("주변 시설 시드 데이터 생성 완료.")


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_checklist(db)
        seed_properties(db)
        seed_pois(db)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
