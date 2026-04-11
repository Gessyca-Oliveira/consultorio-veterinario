from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProfissionalBase(BaseModel):
    nome: str
    cpf: str
    crmv: str
    especialidade: str
    telefone: str
    cep: str
    estado: str
    rua: str
    bairro: str
    numero: str

class ProfissionalCreate(ProfissionalBase):
    pass 

class Profissional(ProfissionalBase):
    id: int

    class Config:
        from_attributes = True

class PacienteBase(BaseModel):
    nome_animal: str
    especie: str
    sexo: str
    idade: int
    peso: float
    nome_tutor: str
    cpf_tutor: str
    telefone: str
    cep: str
    estado: str
    rua: str
    bairro: str
    numero: str

class PacienteCreate(PacienteBase):
    pass

class Paciente(PacienteBase):
    id: int

    class Config:
        from_attributes = True

class ConsultaBase(BaseModel):
    paciente_id: int
    profissional_id: int
    tipo_consulta: str
    data_hora: datetime
    data_retorno: Optional[datetime] = None
    valor_total: float
    forma_pagamento: str

class ConsultaCreate(ConsultaBase):
    pass

class Consulta(ConsultaBase):
    id: int
    paciente: Optional[Paciente] = None
    veterinario: Optional[Profissional] = None

    class Config:
        from_attributes = True