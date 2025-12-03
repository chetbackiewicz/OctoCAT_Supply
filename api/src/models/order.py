from pydantic import BaseModel, ConfigDict, Field


class OrderBase(BaseModel):
    branch_id: int = Field(..., alias="branchId")
    order_date: str = Field(..., alias="orderDate")
    name: str
    description: str | None = None
    status: str = "pending"

    model_config = ConfigDict(populate_by_name=True)


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    branch_id: int | None = Field(None, alias="branchId")
    order_date: str | None = Field(None, alias="orderDate")
    name: str | None = None
    description: str | None = None
    status: str | None = None

    model_config = ConfigDict(populate_by_name=True)


class Order(OrderBase):
    order_id: int = Field(..., alias="orderId")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
