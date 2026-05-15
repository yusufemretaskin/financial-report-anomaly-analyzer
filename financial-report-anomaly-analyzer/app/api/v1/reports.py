from fastapi import APIRouter, UploadFile, File, Path, HTTPException

router=APIRouter()

ALLOWED_CONTENT_TYPES={
    "text/plain"
}


@router.post("")
def upload_document(file:UploadFile = File(...)):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        return HTTPException(
            status_code=400,
            detail="Only csv and txt files are allowed"
        )
