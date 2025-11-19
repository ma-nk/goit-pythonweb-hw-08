from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date, timedelta

def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

def get_contacts(db: Session, skip: int = 0, limit: int = 100, first_name: str | None = None, last_name: str | None = None, email: str | None = None):
    query = db.query(models.Contact)
    if first_name:
        query = query.filter(models.Contact.first_name.contains(first_name))
    if last_name:
        query = query.filter(models.Contact.last_name.contains(last_name))
    if email:
        query = query.filter(models.Contact.email.contains(email))
    return query.offset(skip).limit(limit).all()

def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, contact: schemas.ContactUpdate):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact



def get_upcoming_birthdays(db: Session):
    today = date.today()
    end_date = today + timedelta(days=7)
    return db.query(models.Contact).filter(
        models.Contact.birthday.between(today, end_date)
    ).all()
