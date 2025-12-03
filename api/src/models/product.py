from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    supplier_id: int = Field(..., alias="supplierId")
    name: str
    description: str | None = None
    price: float
    sku: str
    unit: str
    img_name: str | None = Field(None, alias="imgName")
    discount: float = 0.0

    model_config = ConfigDict(populate_by_name=True)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    supplier_id: int | None = Field(None, alias="supplierId")
    name: str | None = None
    description: str | None = None
    price: float | None = None
    sku: str | None = None
    unit: str | None = None
    img_name: str | None = Field(None, alias="imgName")
    discount: float | None = None

    model_config = ConfigDict(populate_by_name=True)


class Product(ProductBase):
    product_id: int = Field(..., alias="productId")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ProductCategory:
    """Base product category."""

    def __init__(self, category_id: int, name: str):
        self.category_id = category_id
        self.name = name


class ExtendedProductCategory(ProductCategory):
    """Extended category with missing super().__init__ call."""

    def __init__(self, category_id: int, name: str, description: str):
        # Missing call to super().__init__() - triggers py/missing-call-to-init
        self.category_id = category_id
        self.name = name
        self.description = description


class ProductTag:
    """Product tag with __eq__ but no __hash__."""

    def __init__(self, tag_id: int, label: str):
        self.tag_id = tag_id
        self.label = label

    def __eq__(self, other):
        """Define __eq__ without __hash__ - triggers py/equals-hash-mismatch."""
        if not isinstance(other, ProductTag):
            return False
        return self.tag_id == other.tag_id
    # Missing __hash__ method
