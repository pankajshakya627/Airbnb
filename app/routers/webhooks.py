from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.checkout_service import CheckoutService

router = APIRouter(prefix="/webhook", tags=["Webhook"])


@router.post("/payment")
async def payment_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Handle Stripe payment webhooks."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")
    
    service = CheckoutService(db)
    await service.handle_payment_webhook(payload, sig_header)
    
    return {"status": "success"}
