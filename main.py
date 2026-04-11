from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="API Consultório Veterinário")

@app.post("/pacientes/", response_model=schemas.Paciente, status_code=201)
def criar_paciente(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = models.Paciente(**paciente.model_dump()) 
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

@app.get("/pacientes/", response_model=List[schemas.Paciente])
def listar_pacientes(db: Session = Depends(get_db)):
    return db.query(models.Paciente).all()

@app.get("/pacientes/{paciente_id}", response_model=schemas.Paciente)
def buscar_paciente(paciente_id: int, db: Session = Depends(get_db)):
    db_paciente = db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return db_paciente

@app.post("/profissionais/", response_model=schemas.Profissional, status_code=201)
def criar_profissional(profissional: schemas.ProfissionalCreate, db: Session = Depends(get_db)):
    db_prof = models.Profissional(**profissional.model_dump())
    db.add(db_prof)
    db.commit()
    db.refresh(db_prof)
    return db_prof

@app.get("/profissionais/", response_model=List[schemas.Profissional])
def listar_profissionais(db: Session = Depends(get_db)):
    return db.query(models.Profissional).all()

@app.post("/consultas/", response_model=schemas.Consulta, status_code=201)
def criar_consulta(consulta: schemas.ConsultaCreate, db: Session = Depends(get_db)):
    db_paciente = db.query(models.Paciente).filter(models.Paciente.id == consulta.paciente_id).first()
    if not db_paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
        
    db_vet = db.query(models.Profissional).filter(models.Profissional.id == consulta.profissional_id).first()
    if not db_vet:
        raise HTTPException(status_code=404, detail="Veterinário não encontrado")

    db_consulta = models.Consulta(**consulta.model_dump())
    db.add(db_consulta)
    db.commit()
    db.refresh(db_consulta)
    return db_consulta

@app.get("/consultas/", response_model=List[schemas.Consulta])
def listar_consultas(db: Session = Depends(get_db)):
    return db.query(models.Consulta).all()