from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers import checklist, evidence, market, poi, property
from seed import seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed()
    yield


app = FastAPI(title="Startup Tracker API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "https://pet-grooming-consulting.vercel.app",
    ],
    allow_origin_regex=r"https://pet-grooming-consulting-.*\.vercel\.app",
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(checklist.router)
app.include_router(property.router)
app.include_router(poi.router)
app.include_router(market.router)
app.include_router(evidence.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
