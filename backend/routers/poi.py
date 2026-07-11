from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import POI
from schemas import POICreate, POIRead, POIUpdate

router = APIRouter(prefix="/api/pois", tags=["pois"])


@router.get("", response_model=list[POIRead])
def list_pois(relation: str | None = None, db: Session = Depends(get_db)):
    query = db.query(POI)
    if relation:
        query = query.filter(POI.relation == relation)
    return query.order_by(POI.relation, POI.name).all()


@router.post("", response_model=POIRead, status_code=201)
def create_poi(payload: POICreate, db: Session = Depends(get_db)):
    poi = POI(**payload.model_dump())
    db.add(poi)
    db.commit()
    db.refresh(poi)
    return poi


@router.patch("/{poi_id}", response_model=POIRead)
def update_poi(poi_id: int, payload: POIUpdate, db: Session = Depends(get_db)):
    poi = db.get(POI, poi_id)
    if poi is None:
        raise HTTPException(status_code=404, detail="시설을 찾을 수 없습니다")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(poi, field, value)

    db.commit()
    db.refresh(poi)
    return poi


@router.delete("/{poi_id}", status_code=204)
def delete_poi(poi_id: int, db: Session = Depends(get_db)):
    poi = db.get(POI, poi_id)
    if poi is None:
        raise HTTPException(status_code=404, detail="시설을 찾을 수 없습니다")
    db.delete(poi)
    db.commit()
