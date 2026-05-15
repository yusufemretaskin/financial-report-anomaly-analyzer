from fastapi import FastAPI
from app.api.v1 import health,reports 
from pandas import pd

app=FastAPI(
    title="Financial Report Anomaly Analyzer",
    version="1.0.0"
)

app.include_router(health.router,prefix="/api/v1",tags="health")
app.include_router(reports.router,prefix="/api/v1/reports")