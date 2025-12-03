from pydantic import BaseModel, ConfigDict, Field


class BranchBase(BaseModel):
    headquarters_id: int = Field(..., alias="headquartersId")
    name: str
    description: str | None = None
    address: str | None = None
    contact_person: str | None = Field(None, alias="contactPerson")
    email: str | None = None
    phone: str | None = None

    model_config = ConfigDict(populate_by_name=True)


class BranchCreate(BranchBase):
    pass


class BranchUpdate(BaseModel):
    headquarters_id: int | None = Field(None, alias="headquartersId")
    name: str | None = None
    description: str | None = None
    address: str | None = None
    contact_person: str | None = Field(None, alias="contactPerson")
    email: str | None = None
    phone: str | None = None

    model_config = ConfigDict(populate_by_name=True)


class Branch(BranchBase):
    branch_id: int = Field(..., alias="branchId")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
