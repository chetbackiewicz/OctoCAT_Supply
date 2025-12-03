from pydantic import BaseModel, ConfigDict, Field


class HeadquartersBase(BaseModel):
    name: str
    description: str | None = None
    address: str | None = None
    contact_person: str | None = Field(None, alias="contactPerson")
    email: str | None = None
    phone: str | None = None

    model_config = ConfigDict(populate_by_name=True)


class HeadquartersCreate(HeadquartersBase):
    pass


class HeadquartersUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    address: str | None = None
    contact_person: str | None = Field(None, alias="contactPerson")
    email: str | None = None
    phone: str | None = None

    model_config = ConfigDict(populate_by_name=True)


class Headquarters(HeadquartersBase):
    headquarters_id: int = Field(..., alias="headquartersId")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
