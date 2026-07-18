"""소상공인시장진흥공단 상가업소정보 API로 강서구 반려동물 관련 업소를 조회해
market_snapshots/market_stores 테이블에 이번 달 스냅샷으로 저장한다.

실행: python fetch_market.py  (backend/ 디렉토리 안에서, .venv 활성화 후)

사전 준비:
1. data.go.kr에서 회원가입 후 "상가업소정보" API 활용신청 (승인까지 1~2시간 소요)
2. 발급받은 서비스키를 backend/.env 파일에 DATA_GO_KR_SERVICE_KEY=... 로 저장
   (.env.example 참고. .env는 .gitignore에 포함되어 커밋되지 않는다)
"""

import os
import sys
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from PublicDataReader import SmallShop

from database import Base, SessionLocal, engine
from models import MarketSnapshot, MarketStore

load_dotenv()

GANGSEO_SIGNGU_CD = "11500"

# 반려동물 관련 소분류 코드 — G22001(애완동물/애완용품 소매업, 옛 837분류 체계의 "애완동물 미용실"이
# 2023.03 개편으로 통합됨)과 M11101(동물병원). 그루밍 전용 코드는 라이브 API에 없음 — 상호명 키워드로 근사.
PET_SCLS_CODES = ["G22001", "M11101"]
GROOMING_KEYWORDS = ["미용", "그루밍", "펫살롱"]
GROOMING_BASE_CATEGORY = "애완동물/애완용품 소매업"

REGION = "강서구"


def get_api():
    service_key = os.getenv("DATA_GO_KR_SERVICE_KEY")
    if not service_key:
        sys.exit(
            "DATA_GO_KR_SERVICE_KEY가 backend/.env에 설정되어 있지 않습니다. "
            ".env.example을 참고해 backend/.env를 만들어주세요."
        )
    return SmallShop(service_key)


def fetch_stores_by_scls_codes(api, div_id, code, scls_codes, page_size=1000):
    """소분류 코드 여러 개를 각각 조회해 하나로 합친다.

    서버가 페이지당 최대 1000건으로 응답을 제한하므로, 결과가 page_size건이면
    다음 페이지를 계속 이어붙여 전체 데이터를 확보한다.
    """
    parts = []
    for scls in scls_codes:
        pages = []
        page_no = 1
        while True:
            page = api.get_data(
                service_name="행정동상가",
                divId=div_id,
                key=code,
                indsSclsCd=scls,
                numOfRows=page_size,
                pageNo=page_no,
            )
            if page.empty:
                break
            pages.append(page)
            if len(page) < page_size:
                break
            page_no += 1
        if pages:
            parts.append(pd.concat(pages, ignore_index=True))

    return pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()


def save_snapshot(df: pd.DataFrame):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        snapshot_month = datetime.now().strftime("%Y-%m")

        existing = (
            db.query(MarketSnapshot)
            .filter(MarketSnapshot.region == REGION, MarketSnapshot.snapshot_month == snapshot_month)
            .first()
        )
        if existing:
            db.delete(existing)
            db.flush()

        snapshot = MarketSnapshot(
            region=REGION,
            snapshot_month=snapshot_month,
            source_note="소상공인시장진흥공단 상가업소정보 API (G22001+M11101, 강서구)",
        )
        db.add(snapshot)
        db.flush()

        for _, row in df.iterrows():
            category = row["상권업종소분류명"]
            name = str(row["상호명"])
            is_grooming = category == GROOMING_BASE_CATEGORY and any(k in name for k in GROOMING_KEYWORDS)
            db.add(
                MarketStore(
                    snapshot_id=snapshot.id,
                    name=name,
                    category=category,
                    dong=row["행정동명"],
                    lat=row["위도"],
                    lon=row["경도"],
                    is_grooming_estimate=is_grooming,
                )
            )

        db.commit()
        print(f"{REGION} {snapshot_month} 스냅샷 저장 완료: {len(df)}건")
    finally:
        db.close()


if __name__ == "__main__":
    api = get_api()
    df = fetch_stores_by_scls_codes(api, "signguCd", GANGSEO_SIGNGU_CD, PET_SCLS_CODES)
    if df.empty:
        sys.exit("조회된 업소가 없습니다. API 키·코드를 확인하세요.")
    save_snapshot(df)
