from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.repository import contacts as repository_contacts
from src.schemas.contact import Contact, ContactCreate, ContactUpdate
from src.conf.db import get_db

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/", response_model=Contact, summary="Create a new contact", description="Create a new contact with the provided information.")
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return repository_contacts.create_contact(db=db, contact=contact)

@router.get("/", response_model=list[Contact], summary="Read contacts", description="Read a list of contacts with optional filtering by first name, last name, or email.")
def read_contacts(skip: int = 0, limit: int = 100, first_name: str | None = None, last_name: str | None = None, email: str | None = None, db: Session = Depends(get_db)):
    contacts = repository_contacts.get_contacts(db, skip=skip, limit=limit, first_name=first_name, last_name=last_name, email=email)
    return contacts

@router.get("/birthdays", response_model=list[Contact], summary="Upcoming birthdays", description="Get a list of contacts with upcoming birthdays in the next 7 days.")
def upcoming_birthdays(db: Session = Depends(get_db)):
    contacts = repository_contacts.get_upcoming_birthdays(db)
    return contacts

@router.get("/{contact_id}", response_model=Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = repository_contacts.get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.put("/{contact_id}", response_model=Contact, summary="Update a contact", description="Update a contact's information by its ID.")
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    db_contact = repository_contacts.update_contact(db, contact_id=contact_id, contact=contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.delete("/{contact_id}", response_model=Contact, summary="Delete a contact", description="Delete a contact by its ID.")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = repository_contacts.delete_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact
