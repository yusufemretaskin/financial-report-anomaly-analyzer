from fastapi import APIRouter, UploadFile, File, Path, HTTPException
import pandas as pd
from pathlib import Path
from app.services.report_analyzer import analyze_report
from app.services.llm_service import generate_anomaly_summary

router=APIRouter()



ALLOWED_CONTENT_TYPES={
    "text/csv",
    "application/vnd.ms-excel"
}

REPORT_UPLOAD_DIR=Path("uploads/reports")
REPORT_UPLOAD_DIR.mkdir( parents=True,exist_ok=True)


@router.post("")
async def upload_document(file:UploadFile = File(...)):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        return HTTPException(
            status_code=400,
            detail="Only csv and txt files are allowed"
        )
    pth=REPORT_UPLOAD_DIR / file.filename
    content=await file.read()
    
    with open(pth ,"wb") as f:
        f.write(content)

    dt=pd.read_csv(pth)

    return {
        "file_name": file.filename,
        "row_count": len(dt),
        "columns": list(dt.columns),
        "preview": dt.head(5).to_dict(orient="records"),
        "status": "uploaded"
    }

@router.get("")
def get_reports():
    reports=[]
    for file in REPORT_UPLOAD_DIR.iterdir():
        reports.append({
            "file_name": file.name,
            "size_bytes": file.stat().st_size,
            "path": str(file)
        })
    return reports

@router.get("/{file_name}/anomalies")
def get_report_anomalies(file_name:str):
    file=Path(file_name).name
    file_path=REPORT_UPLOAD_DIR / file

    if not file_path.exists():
        HTTPException(
            status_code=404,
            detail="file not found."
        )
    result=analyze_report(file_path)

    return {
        "file_name":file_name,
        "result":result
    }   



@router.get("/{file_name}/summary")
def get_report_anomalies_summary(file_name:str):
    file=Path(file_name).name
    file_path=REPORT_UPLOAD_DIR / file

    if not file_path.exists():
        HTTPException(
            status_code=404,
            detail="file not found."
        )
    result=analyze_report(file_path)
    summary=generate_anomaly_summary(result["anomalies"])
    return {
        "file_name": file_name,
        "summary": summary
    }  