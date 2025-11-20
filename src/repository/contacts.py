from sqlalchemy.orm import Session
from src.models.contact import Contact
from src.schemas.contact import ContactCreate, ContactUpdate
from datetime import date, timedelta

def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

def get_contacts(db: Session, skip: int = 0, limit: int = 100, first_name: str | None = None, last_name: str | None = None, email: str | None = None):
    query = db.query(Contact)
    if first_name:
        query = query.filter(Contact.first_name.contains(first_name))
    if last_name:
        query = query.filter(Contact.last_name.contains(last_name))
    if email:
        query = query.filter(Contact.email.contains(email))
    return query.offset(skip).limit(limit).all()

def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, contact: ContactUpdate):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        for key, value in contact.model_dump().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact

def get_upcoming_birthdays(db: Session):
    today = date.today()
    end_date = today + timedelta(days=7)
    return db.query(Contact).filter(
        Contact.birthday.between(today, end_date)
    ).all()
