# app/routers/shopify.py
from fastapi import APIRouter, HTTPException
from app.schemas import URI, requestResponse
from app.lib.getData import Data

router = APIRouter(prefix="/shopify", tags=["shopify"])

@router.get("/")
def health():
    return {"status": "ok"}

@router.post("/", response_model=requestResponse)
def get_product(payload: URI):
    try:
        return Data(payload)  # pass the Pydantic model, not a dict
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
