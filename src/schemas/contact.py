from pydantic import BaseModel, EmailStr, validator
from datetime import date

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date
    additional_data: str | None = None

class ContactCreate(ContactBase):
    @validator('birthday')
    def birthday_cannot_be_in_the_future(cls, v):
        if v > date.today():
            raise ValueError('Birthday cannot be in the future')
        return v

class ContactUpdate(ContactBase):
    pass

class Contact(ContactBase):
    id: int

    class Config:
        from_attributes = True
