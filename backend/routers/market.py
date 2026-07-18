from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import MarketSnapshot, MarketStore
from schemas import (
    MarketChanges,
    MarketDistribution,
    MarketDongBreakdown,
    MarketGroomingEstimate,
    MarketStoreChange,
    MarketStorePoint,
    MarketTrendPoint,
)

router = APIRouter(prefix="/api/market", tags=["market"])

# 고정 카테고리 순서 — 프론트엔드 색상 슬롯과 1:1로 매핑되므로 순서를 바꾸지 않는다.
PET_CATEGORY_ORDER = ["애완동물/애완용품 소매업", "동물병원"]

# 그루밍(애견미용) 근사 추정 — 2023.03 업종분류 개편으로 전용 코드가 없어 상호명 키워드로만 추정한다.
GROOMING_KEYWORDS = ["미용", "그루밍", "펫살롱"]
GROOMING_BASE_CATEGORY = "애완동물/애완용품 소매업"
GROOMING_NOTE = (
    "상호명 키워드 기반 추정치(하한). 2023.03 업종분류 개편으로 '애완동물 미용실' 코드가 "
    "애완동물/애완용품 소매업(G22001)에 통합되어 공식 코드로는 그루밍 업소만 분리할 수 없음."
)


def _group_categories(stores: list[MarketStore]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for s in stores:
        counts[s.category] = counts.get(s.category, 0) + 1
    return {cat: counts[cat] for cat in PET_CATEGORY_ORDER if counts.get(cat)}


def _grooming_estimate(stores: list[MarketStore]) -> MarketGroomingEstimate:
    base = [s for s in stores if s.category == GROOMING_BASE_CATEGORY]
    matched = sum(1 for s in base if s.is_grooming_estimate)
    return MarketGroomingEstimate(
        keyword_count=matched,
        base_count=len(base),
        keywords=GROOMING_KEYWORDS,
        note=GROOMING_NOTE,
    )


def _latest_snapshot(db: Session) -> MarketSnapshot | None:
    return db.query(MarketSnapshot).order_by(MarketSnapshot.snapshot_month.desc()).first()


@router.get("/latest", response_model=MarketDistribution)
def latest_distribution(db: Session = Depends(get_db)):
    snapshot = _latest_snapshot(db)
    if snapshot is None:
        raise HTTPException(
            status_code=404,
            detail="아직 상권 데이터가 없습니다. backend/fetch_market.py로 먼저 스냅샷을 수집하세요.",
        )

    stores = snapshot.stores
    by_dong_map: dict[str, list[MarketStore]] = {}
    for s in stores:
        by_dong_map.setdefault(s.dong, []).append(s)

    by_dong = [
        MarketDongBreakdown(dong=dong, total=len(dong_stores), categories=_group_categories(dong_stores))
        for dong, dong_stores in by_dong_map.items()
    ]
    by_dong.sort(key=lambda d: d.total, reverse=True)

    return MarketDistribution(
        region=snapshot.region,
        snapshot_month=snapshot.snapshot_month,
        fetched_at=snapshot.fetched_at,
        category_order=PET_CATEGORY_ORDER,
        total_stores=len(stores),
        citywide_categories=_group_categories(stores),
        by_dong=by_dong,
        points=[
            MarketStorePoint(
                name=s.name,
                category=s.category,
                dong=s.dong,
                address=s.address,
                lat=s.lat,
                lon=s.lon,
                is_grooming_estimate=s.is_grooming_estimate,
            )
            for s in stores
        ],
        grooming_estimate=_grooming_estimate(stores),
    )


@router.get("/trend", response_model=list[MarketTrendPoint])
def trend(db: Session = Depends(get_db)):
    snapshots = db.query(MarketSnapshot).order_by(MarketSnapshot.snapshot_month).all()

    result = []
    prev_total = None
    for snap in snapshots:
        stores = snap.stores
        total = len(stores)
        result.append(
            MarketTrendPoint(
                snapshot_month=snap.snapshot_month,
                total_stores=total,
                category_counts=_group_categories(stores),
                net_change=None if prev_total is None else total - prev_total,
            )
        )
        prev_total = total

    return result


def _to_change(s: MarketStore) -> MarketStoreChange:
    return MarketStoreChange(name=s.name, category=s.category, dong=s.dong, address=s.address)


@router.get("/changes", response_model=MarketChanges)
def changes(db: Session = Depends(get_db)):
    snapshots = (
        db.query(MarketSnapshot).order_by(MarketSnapshot.snapshot_month.desc()).limit(2).all()
    )
    if not snapshots:
        raise HTTPException(
            status_code=404,
            detail="아직 상권 데이터가 없습니다. backend/fetch_market.py로 먼저 스냅샷을 수집하세요.",
        )

    latest = snapshots[0]
    if len(snapshots) < 2:
        return MarketChanges(from_month=None, to_month=latest.snapshot_month, new_stores=[], removed_stores=[])

    previous = snapshots[1]
    latest_by_biz = {s.biz_no: s for s in latest.stores if s.biz_no}
    prev_by_biz = {s.biz_no: s for s in previous.stores if s.biz_no}

    new_ids = set(latest_by_biz) - set(prev_by_biz)
    removed_ids = set(prev_by_biz) - set(latest_by_biz)

    return MarketChanges(
        from_month=previous.snapshot_month,
        to_month=latest.snapshot_month,
        new_stores=[_to_change(latest_by_biz[i]) for i in new_ids],
        removed_stores=[_to_change(prev_by_biz[i]) for i in removed_ids],
    )
