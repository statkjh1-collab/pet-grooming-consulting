from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import PriceHistory, Property
from schemas import (
    MarketSummary,
    PriceHistoryCreate,
    PriceHistoryRead,
    PropertyCreate,
    PropertyRead,
    PropertyUpdate,
)

router = APIRouter(prefix="/api/properties", tags=["properties"])


def _unresolved_checks(p: Property) -> list[str]:
    checks = []
    if p.water_supply == "미확인":
        checks.append("급배수 인입 가능 여부")
    if not p.electric_capacity:
        checks.append("전기 용량")
    if p.floor is None:
        checks.append("층수")
    if p.key_money is None:
        checks.append("권리금 유무")
    if p.maintenance_fee is None:
        checks.append("관리비 (월세 별도인지)")
    return checks


def _to_read(p: Property) -> PropertyRead:
    rent_per_pyeong = round(p.monthly_rent / p.area_pyeong, 1) if p.area_pyeong else 0.0
    return PropertyRead(
        id=p.id,
        name=p.name,
        landmark=p.landmark,
        address=p.address,
        floor=p.floor,
        area_pyeong=p.area_pyeong,
        deposit=p.deposit,
        monthly_rent=p.monthly_rent,
        maintenance_fee=p.maintenance_fee,
        key_money=p.key_money,
        negotiable=p.negotiable,
        expandable=p.expandable,
        expansion_note=p.expansion_note,
        prev_business=p.prev_business,
        water_supply=p.water_supply,
        electric_capacity=p.electric_capacity,
        status=p.status,
        visited_at=p.visited_at,
        memo=p.memo,
        created_at=p.created_at,
        updated_at=p.updated_at,
        price_history=p.price_history,
        rent_per_pyeong=rent_per_pyeong,
        annual_rent=p.monthly_rent * 12,
        initial_cost=p.deposit + (p.key_money or 0),
        unresolved_checks=_unresolved_checks(p),
    )


@router.get("", response_model=list[PropertyRead])
def list_properties(status: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Property)
    if status:
        query = query.filter(Property.status == status)
    properties = query.order_by(Property.created_at.desc()).all()
    return [_to_read(p) for p in properties]


@router.get("/summary", response_model=MarketSummary)
def market_summary(db: Session = Depends(get_db)):
    properties = db.query(Property).all()
    if not properties:
        return MarketSummary(
            count=0,
            area_min=None,
            area_max=None,
            deposit_min=None,
            deposit_max=None,
            rent_min=None,
            rent_max=None,
            rent_per_pyeong_avg=None,
        )

    areas = [p.area_pyeong for p in properties]
    deposits = [p.deposit for p in properties]
    rents = [p.monthly_rent for p in properties]
    rents_per_pyeong = [p.monthly_rent / p.area_pyeong for p in properties if p.area_pyeong]

    return MarketSummary(
        count=len(properties),
        area_min=min(areas),
        area_max=max(areas),
        deposit_min=min(deposits),
        deposit_max=max(deposits),
        rent_min=min(rents),
        rent_max=max(rents),
        rent_per_pyeong_avg=round(sum(rents_per_pyeong) / len(rents_per_pyeong), 1)
        if rents_per_pyeong
        else None,
    )


@router.post("", response_model=PropertyRead, status_code=201)
def create_property(payload: PropertyCreate, db: Session = Depends(get_db)):
    prop = Property(**payload.model_dump())
    db.add(prop)
    db.commit()
    db.refresh(prop)
    return _to_read(prop)


@router.get("/{property_id}", response_model=PropertyRead)
def get_property(property_id: int, db: Session = Depends(get_db)):
    prop = db.get(Property, property_id)
    if prop is None:
        raise HTTPException(status_code=404, detail="매물을 찾을 수 없습니다")
    return _to_read(prop)


@router.patch("/{property_id}", response_model=PropertyRead)
def update_property(property_id: int, payload: PropertyUpdate, db: Session = Depends(get_db)):
    prop = db.get(Property, property_id)
    if prop is None:
        raise HTTPException(status_code=404, detail="매물을 찾을 수 없습니다")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(prop, field, value)

    db.commit()
    db.refresh(prop)
    return _to_read(prop)


@router.delete("/{property_id}", status_code=204)
def delete_property(property_id: int, db: Session = Depends(get_db)):
    prop = db.get(Property, property_id)
    if prop is None:
        raise HTTPException(status_code=404, detail="매물을 찾을 수 없습니다")
    db.delete(prop)
    db.commit()


@router.post("/{property_id}/price-history", response_model=PriceHistoryRead, status_code=201)
def add_price_history(property_id: int, payload: PriceHistoryCreate, db: Session = Depends(get_db)):
    prop = db.get(Property, property_id)
    if prop is None:
        raise HTTPException(status_code=404, detail="매물을 찾을 수 없습니다")

    entry = PriceHistory(
        property_id=property_id,
        recorded_at=payload.recorded_at or date.today(),
        deposit=payload.deposit,
        monthly_rent=payload.monthly_rent,
        is_vacant=payload.is_vacant,
        note=payload.note,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
