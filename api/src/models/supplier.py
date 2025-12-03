from pydantic import BaseModel, ConfigDict, Field


class SupplierBase(BaseModel):
    name: str
    description: str | None = None
    contact_person: str | None = Field(None, alias="contactPerson")
    email: str | None = None
    phone: str | None = None
    active: bool = True
    verified: bool = False

    model_config = ConfigDict(populate_by_name=True)


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    contact_person: str | None = Field(None, alias="contactPerson")
    email: str | None = None
    phone: str | None = None
    active: bool | None = None
    verified: bool | None = None

    model_config = ConfigDict(populate_by_name=True)


class Supplier(SupplierBase):
    supplier_id: int = Field(..., alias="supplierId")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class SupplierCache:
    """Cache for supplier data - has equals/hash mismatch."""

    def __init__(self, supplier_id: int, name: str):
        self.supplier_id = supplier_id
        self.name = name

    def __hash__(self):
        """Define hash without __eq__ - triggers py/equals-hash-mismatch."""
        return hash((self.supplier_id, self.name))
    # Missing __eq__ method
