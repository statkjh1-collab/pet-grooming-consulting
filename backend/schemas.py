from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

WaterSupply = Literal["가능", "불가", "미확인"]
PropertyStatus = Literal["관심", "유력", "보류", "제외"]
POIType = Literal[
    "경쟁미용실", "동물병원_주간", "동물병원_24시", "유치원호텔", "펫샵", "미용학원", "애견카페"
]
POIRelation = Literal["경쟁", "제휴후보", "응급대응", "수요파이프라인"]


class ItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    why: str
    done: bool
    done_at: datetime | None
    memo: str
    order: int


class ItemUpdate(BaseModel):
    done: bool | None = None
    memo: str | None = None


class GroupRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    order: int
    items: list[ItemRead]


class StageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    key: str
    title: str
    period_label: str
    gate_signal: str
    order: int
    groups: list[GroupRead]
    total_items: int
    completed_items: int
    progress_pct: float


class PriceHistoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    recorded_at: date
    deposit: int
    monthly_rent: int
    is_vacant: bool
    note: str


class PriceHistoryCreate(BaseModel):
    recorded_at: date | None = None
    deposit: int
    monthly_rent: int
    is_vacant: bool = True
    note: str = ""


class PropertyBase(BaseModel):
    name: str
    landmark: str = ""
    address: str = ""
    floor: int | None = None
    area_pyeong: float
    deposit: int = 0
    monthly_rent: int = 0
    maintenance_fee: int | None = None
    key_money: int | None = None
    negotiable: bool = False
    expandable: bool = False
    expansion_note: str = ""
    prev_business: str = ""
    water_supply: WaterSupply = "미확인"
    electric_capacity: str = ""
    status: PropertyStatus = "관심"
    visited_at: date | None = None
    memo: str = ""


class PropertyCreate(PropertyBase):
    pass


class PropertyUpdate(BaseModel):
    name: str | None = None
    landmark: str | None = None
    address: str | None = None
    floor: int | None = None
    area_pyeong: float | None = None
    deposit: int | None = None
    monthly_rent: int | None = None
    maintenance_fee: int | None = None
    key_money: int | None = None
    negotiable: bool | None = None
    expandable: bool | None = None
    expansion_note: str | None = None
    prev_business: str | None = None
    water_supply: WaterSupply | None = None
    electric_capacity: str | None = None
    status: PropertyStatus | None = None
    visited_at: date | None = None
    memo: str | None = None


class PropertyRead(PropertyBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    price_history: list[PriceHistoryRead] = []
    rent_per_pyeong: float
    annual_rent: int
    initial_cost: int
    unresolved_checks: list[str]


class MarketSummary(BaseModel):
    count: int
    area_min: float | None
    area_max: float | None
    deposit_min: int | None
    deposit_max: int | None
    rent_min: int | None
    rent_max: int | None
    rent_per_pyeong_avg: float | None


class POIBase(BaseModel):
    name: str
    type: POIType
    address: str = ""
    lat: float | None = None
    lng: float | None = None
    hours: str = ""
    rating: float | None = None
    relation: POIRelation
    note: str = ""


class POICreate(POIBase):
    pass


class POIUpdate(BaseModel):
    name: str | None = None
    type: POIType | None = None
    address: str | None = None
    lat: float | None = None
    lng: float | None = None
    hours: str | None = None
    rating: float | None = None
    relation: POIRelation | None = None
    note: str | None = None


class POIRead(POIBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class MarketStorePoint(BaseModel):
    name: str
    category: str
    dong: str
    address: str
    lat: float
    lon: float
    is_grooming_estimate: bool


class MarketDongBreakdown(BaseModel):
    dong: str
    total: int
    categories: dict[str, int]


class MarketGroomingEstimate(BaseModel):
    keyword_count: int
    base_count: int
    keywords: list[str]
    note: str


class MarketDistribution(BaseModel):
    region: str
    snapshot_month: str
    fetched_at: datetime
    category_order: list[str]
    total_stores: int
    citywide_categories: dict[str, int]
    by_dong: list[MarketDongBreakdown]
    points: list[MarketStorePoint]
    grooming_estimate: MarketGroomingEstimate


class MarketTrendPoint(BaseModel):
    snapshot_month: str
    total_stores: int
    category_counts: dict[str, int]
    net_change: int | None


class MarketStoreChange(BaseModel):
    name: str
    category: str
    dong: str
    address: str


class MarketChanges(BaseModel):
    from_month: str | None
    to_month: str
    new_stores: list[MarketStoreChange]
    removed_stores: list[MarketStoreChange]
