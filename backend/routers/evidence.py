from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Evidence
from schemas import EvidenceCreate, EvidenceRead, EvidenceUpdate

router = APIRouter(prefix="/api/evidence", tags=["evidence"])


@router.get("", response_model=list[EvidenceRead])
def list_evidence(type: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Evidence)
    if type:
        query = query.filter(Evidence.type == type)
    return query.order_by(Evidence.date.desc(), Evidence.id.desc()).all()


@router.post("", response_model=EvidenceRead, status_code=201)
def create_evidence(payload: EvidenceCreate, db: Session = Depends(get_db)):
    item = Evidence(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.patch("/{evidence_id}", response_model=EvidenceRead)
def update_evidence(evidence_id: int, payload: EvidenceUpdate, db: Session = Depends(get_db)):
    item = db.get(Evidence, evidence_id)
    if item is None:
        raise HTTPException(status_code=404, detail="증빙을 찾을 수 없습니다")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


@router.delete("/{evidence_id}", status_code=204)
def delete_evidence(evidence_id: int, db: Session = Depends(get_db)):
    item = db.get(Evidence, evidence_id)
    if item is None:
        raise HTTPException(status_code=404, detail="증빙을 찾을 수 없습니다")
    db.delete(item)
    db.commit()
