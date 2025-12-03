from pydantic import BaseModel, ConfigDict, Field


class OrderDetailBase(BaseModel):
    order_id: int = Field(..., alias="orderId")
    product_id: int = Field(..., alias="productId")
    quantity: int
    unit_price: float = Field(..., alias="unitPrice")
    notes: str | None = None

    model_config = ConfigDict(populate_by_name=True)


class OrderDetailCreate(OrderDetailBase):
    pass


class OrderDetailUpdate(BaseModel):
    order_id: int | None = Field(None, alias="orderId")
    product_id: int | None = Field(None, alias="productId")
    quantity: int | None = None
    unit_price: float | None = Field(None, alias="unitPrice")
    notes: str | None = None

    model_config = ConfigDict(populate_by_name=True)


class OrderDetail(OrderDetailBase):
    order_detail_id: int = Field(..., alias="orderDetailId")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
