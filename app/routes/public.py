from fastapi import APIRouter

router = APIRouter(prefix="/public", tags=["public"])

# Health Check
@router.get('/')
def health_check():
    return {"status": "ok"}