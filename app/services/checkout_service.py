import stripe
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi import HTTPException, status

from app.config import get_settings
from app.models.booking import Booking
from app.models.user import User
from app.models.enums import BookingStatus

settings = get_settings()
stripe.api_key = settings.STRIPE_API_KEY


class CheckoutService:
    """Service for payment checkout operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_checkout_session(self, booking_id: int, user: User) -> str:
        """Create Stripe checkout session for a booking."""
        # Get booking
        result = await self.db.execute(
            select(Booking).where(Booking.id == booking_id, Booking.user_id == user.id)
        )
        booking = result.scalar_one_or_none()
        
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Booking not found: {booking_id}"
            )
        
        if booking.booking_status not in [BookingStatus.RESERVED, BookingStatus.GUESTS_ADDED]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Booking cannot proceed to payment"
            )
        
        # Create Stripe checkout session
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": f"Booking #{booking.id}",
                            "description": f"Room booking from {booking.check_in_date} to {booking.check_out_date}"
                        },
                        "unit_amount": int(booking.amount * 100),  # Convert to cents
                    },
                    "quantity": 1,
                }],
                mode="payment",
                success_url=f"{settings.FRONTEND_URL}/booking/{booking.id}/success",
                cancel_url=f"{settings.FRONTEND_URL}/booking/{booking.id}/cancel",
                metadata={
                    "booking_id": str(booking.id)
                }
            )
            
            # Update booking with session ID
            booking.payment_session_id = checkout_session.id
            booking.booking_status = BookingStatus.PAYMENTS_PENDING
            await self.db.flush()
            
            return checkout_session.url
            
        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Payment error: {str(e)}"
            )
    
    async def handle_payment_webhook(self, payload: bytes, sig_header: str) -> None:
        """Handle Stripe webhook events."""
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid payload")
        except stripe.error.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Invalid signature")
        
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            booking_id = int(session["metadata"]["booking_id"])
            
            # Confirm the booking
            result = await self.db.execute(
                select(Booking).where(Booking.id == booking_id)
            )
            booking = result.scalar_one_or_none()
            
            if booking:
                booking.booking_status = BookingStatus.CONFIRMED
                await self.db.flush()
