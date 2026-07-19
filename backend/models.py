from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Stage(Base):
    __tablename__ = "stages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(30), unique=True)
    title: Mapped[str] = mapped_column(String(200))
    period_label: Mapped[str] = mapped_column(String(50))
    gate_signal: Mapped[str] = mapped_column(Text)
    order: Mapped[int] = mapped_column(Integer, default=0)

    groups: Mapped[list["ChecklistGroup"]] = relationship(
        back_populates="stage", cascade="all, delete-orphan", order_by="ChecklistGroup.order"
    )


class ChecklistGroup(Base):
    __tablename__ = "checklist_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stage_id: Mapped[int] = mapped_column(ForeignKey("stages.id"))
    title: Mapped[str] = mapped_column(String(200))
    order: Mapped[int] = mapped_column(Integer, default=0)

    stage: Mapped["Stage"] = relationship(back_populates="groups")
    items: Mapped[list["ChecklistItem"]] = relationship(
        back_populates="group", cascade="all, delete-orphan", order_by="ChecklistItem.order"
    )


class ChecklistItem(Base):
    __tablename__ = "checklist_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("checklist_groups.id"))
    title: Mapped[str] = mapped_column(String(300))
    why: Mapped[str] = mapped_column(Text, default="")
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    done_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    memo: Mapped[str] = mapped_column(Text, default="")
    order: Mapped[int] = mapped_column(Integer, default=0)

    group: Mapped["ChecklistGroup"] = relationship(back_populates="items")


class Property(Base):
    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    landmark: Mapped[str] = mapped_column(String(300), default="")
    address: Mapped[str] = mapped_column(String(300), default="")
    floor: Mapped[int | None] = mapped_column(Integer, nullable=True)
    area_pyeong: Mapped[float] = mapped_column(Float)
    deposit: Mapped[int] = mapped_column(Integer, default=0)
    monthly_rent: Mapped[int] = mapped_column(Integer, default=0)
    maintenance_fee: Mapped[int | None] = mapped_column(Integer, nullable=True)
    key_money: Mapped[int | None] = mapped_column(Integer, nullable=True)
    negotiable: Mapped[bool] = mapped_column(Boolean, default=False)
    expandable: Mapped[bool] = mapped_column(Boolean, default=False)
    expansion_note: Mapped[str] = mapped_column(Text, default="")
    prev_business: Mapped[str] = mapped_column(String(100), default="")
    water_supply: Mapped[str] = mapped_column(String(10), default="미확인")
    electric_capacity: Mapped[str] = mapped_column(String(100), default="")
    status: Mapped[str] = mapped_column(String(10), default="관심")
    visited_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    memo: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    price_history: Mapped[list["PriceHistory"]] = relationship(
        back_populates="property", cascade="all, delete-orphan", order_by="PriceHistory.recorded_at"
    )


class PriceHistory(Base):
    __tablename__ = "price_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"))
    recorded_at: Mapped[date] = mapped_column(Date, default=date.today)
    deposit: Mapped[int] = mapped_column(Integer)
    monthly_rent: Mapped[int] = mapped_column(Integer)
    is_vacant: Mapped[bool] = mapped_column(Boolean, default=True)
    note: Mapped[str] = mapped_column(Text, default="")

    property: Mapped["Property"] = relationship(back_populates="price_history")


class POI(Base):
    __tablename__ = "pois"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    type: Mapped[str] = mapped_column(String(30))
    address: Mapped[str] = mapped_column(String(300), default="")
    lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    lng: Mapped[float | None] = mapped_column(Float, nullable=True)
    hours: Mapped[str] = mapped_column(String(100), default="")
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    relation: Mapped[str] = mapped_column(String(20))
    note: Mapped[str] = mapped_column(Text, default="")


class MarketSnapshot(Base):
    __tablename__ = "market_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    region: Mapped[str] = mapped_column(String(50))
    snapshot_month: Mapped[str] = mapped_column(String(7))  # "YYYY-MM"
    fetched_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    source_note: Mapped[str] = mapped_column(Text, default="")

    stores: Mapped[list["MarketStore"]] = relationship(
        back_populates="snapshot", cascade="all, delete-orphan"
    )


class MarketStore(Base):
    __tablename__ = "market_stores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    snapshot_id: Mapped[int] = mapped_column(ForeignKey("market_snapshots.id"))
    biz_no: Mapped[str] = mapped_column(String(30), default="")  # 상가업소번호 — 스냅샷 간 동일 업소 매칭용 영구 ID
    name: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(100))
    dong: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(300), default="")
    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)
    is_grooming_estimate: Mapped[bool] = mapped_column(Boolean, default=False)

    snapshot: Mapped["MarketSnapshot"] = relationship(back_populates="stores")


class Evidence(Base):
    __tablename__ = "evidence"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(Text)
    source: Mapped[str] = mapped_column(String(200), default="")
    date: Mapped[date] = mapped_column(Date, default=date.today)
    attachment: Mapped[str] = mapped_column(String(500), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
