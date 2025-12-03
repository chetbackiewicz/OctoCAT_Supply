from pydantic import BaseModel, ConfigDict, Field


class OrderDetailDeliveryBase(BaseModel):
    order_detail_id: int = Field(..., alias="orderDetailId")
    delivery_id: int = Field(..., alias="deliveryId")
    quantity: int
    notes: str | None = None

    model_config = ConfigDict(populate_by_name=True)


class OrderDetailDeliveryCreate(OrderDetailDeliveryBase):
    pass


class OrderDetailDeliveryUpdate(BaseModel):
    order_detail_id: int | None = Field(None, alias="orderDetailId")
    delivery_id: int | None = Field(None, alias="deliveryId")
    quantity: int | None = None
    notes: str | None = None

    model_config = ConfigDict(populate_by_name=True)


class OrderDetailDelivery(OrderDetailDeliveryBase):
    order_detail_delivery_id: int = Field(..., alias="orderDetailDeliveryId")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
