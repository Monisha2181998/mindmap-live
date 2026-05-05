from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    content = Column(String)
    concepts = Column(String)  # stored as comma-separated
    timestamp = Column(DateTime, default=datetime.now)

engine = create_engine("sqlite:///mindmap.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def save_note(content, concepts):
    session = Session()
    note = Note(content=content, concepts=",".join(concepts))
    session.add(note)
    session.commit()
    session.close()

def get_all_notes():
    session = Session()
    notes = session.query(Note).all()
    session.close()
    return notes