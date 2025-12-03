from pydantic import BaseModel, ConfigDict, Field


class DeliveryBase(BaseModel):
    supplier_id: int = Field(..., alias="supplierId")
    delivery_date: str = Field(..., alias="deliveryDate")
    name: str
    description: str | None = None
    status: str = "pending"

    model_config = ConfigDict(populate_by_name=True)


class DeliveryCreate(DeliveryBase):
    pass


class DeliveryUpdate(BaseModel):
    supplier_id: int | None = Field(None, alias="supplierId")
    delivery_date: str | None = Field(None, alias="deliveryDate")
    name: str | None = None
    description: str | None = None
    status: str | None = None

    model_config = ConfigDict(populate_by_name=True)


class Delivery(DeliveryBase):
    delivery_id: int = Field(..., alias="deliveryId")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
