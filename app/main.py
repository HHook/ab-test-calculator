from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from calculator import run_calculation

app = FastAPI(title="A/B Test Duration Calculator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this to your Hugo domain later
    allow_methods=["*"],
    allow_headers=["*"],
)

class CalcInput(BaseModel):
    baseline_conversion_rate: float = Field(..., gt=0, le=100)
    expected_relative_pct_change: float = Field(..., gt=0)
    daily_traffic: int = Field(..., gt=0)
    statistical_power: float = Field(0.80, gt=0, lt=1)
    significance_level: float = Field(0.05, gt=0, lt=1)
    traffic_allocation: float = Field(1.0, gt=0, le=1)
    allocation_ratio: float = Field(1.0, gt=0)

@app.post("/calculate")
def calculate(inputs: CalcInput):
    return run_calculation(**inputs.model_dump())

@app.get("/health")
def health():
    return {"status": "ok"}
# test deploy
