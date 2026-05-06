from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    content = Column(String)
    concepts = Column(String)
    timestamp = Column(DateTime, default=datetime.now)

# Database connection
engine = create_engine("sqlite:///mindmap.db", connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def save_note(content, concepts):
    session = Session()
    clean_concepts = ",".join([c.lower().strip() for c in concepts])
    note = Note(content=content, concepts=clean_concepts)
    session.add(note)
    session.commit()
    session.close()

def get_all_notes():
    session = Session()
    notes = session.query(Note).order_by(Note.timestamp.asc()).all()
    session.close()
    return notes

def delete_note_by_id(note_id):
    """Deletes a specific note and its connections."""
    session = Session()
    note = session.query(Note).filter(Note.id == note_id).first()
    if note:
        session.delete(note)
        session.commit()
    session.close()