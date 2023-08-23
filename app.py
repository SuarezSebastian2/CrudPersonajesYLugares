from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

app = FastAPI()

DATABASE_URL = "mysql://root:1234@localhost/PruebaABC"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Lugar(Base):
    __tablename__ = "lugares"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    personajes = relationship("Personaje", back_populates="origen")

class PersonajeDB(Base):
    __tablename__ = "personajes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    edad = Column(Integer)
    origen_id = Column(Integer, ForeignKey("lugares.id"))
    origen = relationship("Lugar", back_populates="personajes")


class PersonajeCreate(BaseModel):
    nombre: str
    edad: int
    origen_id: int

@app.post("/personajes/")
def crear_personaje(personaje: PersonajeCreate):
    db = SessionLocal()
    db_personaje = PersonajeDB(**personaje.dict())
    db.add(db_personaje)
    db.commit()
    db.refresh(db_personaje)
    db.close()
    return db_personaje

@app.get("/personajes/")
def leer_personajes():
    db = SessionLocal()
    personajes = db.query(PersonajeDB).all()
    db.close()
    return personajes

@app.get("/personajes/{personaje_id}")
def leer_personaje(personaje_id: int):
    db = SessionLocal()
    personaje = db.query(PersonajeDB).filter(PersonajeDB.id == personaje_id).first()
    db.close()
    if personaje is None:
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    return personaje
@app.put("/personajes/{personaje_id}")
def actualizar_personaje(personaje_id: int, personaje: PersonajeCreate):
    db = SessionLocal()
    db_personaje = db.query(PersonajeDB).filter(PersonajeDB.id == personaje_id).first()
    if db_personaje is None:
        db.close()
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    for key, value in personaje.dict().items():
        setattr(db_personaje, key, value)
    db.commit()
    db.refresh(db_personaje)
    db.close()
    return db_personaje

@app.delete("/personajes/{personaje_id}")
def eliminar_personaje(personaje_id: int):
    db = SessionLocal()
    db_personaje = db.query(PersonajeDB).filter(PersonajeDB.id == personaje_id).first()
    if db_personaje is None:
        db.close()
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    db.delete(db_personaje)
    db.commit()
    db.close()
    return {"message": "Personaje eliminado exitosamente"}


