from pydantic import BaseModel, Field


class KakaoPayReadyForBuyProductRequest(BaseModel):
    product_id: int = Field(...)
    payment_type: str = Field(...)
    quantity: int = Field(...)
    order_phone_number: str = Field(...)
