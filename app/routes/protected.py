
from fastapi import APIRouter, Request, Form

router = APIRouter(prefix="/protected", tags=["protected"])

@router.post("/generate-invoice")
async def generate_invoice(request: Request):
    data = await request.form()
    
