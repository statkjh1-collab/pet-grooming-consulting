from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import ChecklistItem, Stage
from schemas import ItemRead, ItemUpdate, StageRead

router = APIRouter(prefix="/api/checklist", tags=["checklist"])


def _to_stage_read(stage: Stage) -> StageRead:
    total = sum(len(g.items) for g in stage.groups)
    completed = sum(1 for g in stage.groups for item in g.items if item.done)
    pct = round((completed / total) * 100, 1) if total else 0.0
    return StageRead(
        id=stage.id,
        key=stage.key,
        title=stage.title,
        period_label=stage.period_label,
        gate_signal=stage.gate_signal,
        order=stage.order,
        groups=stage.groups,
        total_items=total,
        completed_items=completed,
        progress_pct=pct,
    )


@router.get("", response_model=list[StageRead])
def list_stages(db: Session = Depends(get_db)):
    stages = db.query(Stage).order_by(Stage.order).all()
    return [_to_stage_read(s) for s in stages]


@router.patch("/items/{item_id}", response_model=ItemRead)
def update_item(item_id: int, payload: ItemUpdate, db: Session = Depends(get_db)):
    item = db.get(ChecklistItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="항목을 찾을 수 없습니다")

    if payload.done is not None:
        item.done = payload.done
        item.done_at = datetime.now() if payload.done else None
    if payload.memo is not None:
        item.memo = payload.memo

    db.commit()
    db.refresh(item)
    return item
