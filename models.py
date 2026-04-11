from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Profissional(Base):
    __tablename__ = "profissionais"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    cpf = Column(String, unique=True)
    crmv = Column(String, unique=True)
    especialidade = Column(String)
    telefone = Column(String)
    cep = Column(String)
    estado = Column(String)
    rua = Column(String)
    bairro = Column(String)
    numero = Column(String)

    consultas = relationship("Consulta", back_populates="veterinario")

class Paciente(Base):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, index=True)
    nome_animal = Column(String)
    especie = Column(String)
    sexo = Column(String)
    idade = Column(Integer)
    peso = Column(Float)
    nome_tutor = Column(String)
    cpf_tutor = Column(String)
    telefone = Column(String)
    cep = Column(String)
    estado = Column(String)
    rua = Column(String)
    bairro = Column(String)
    numero = Column(String)

    consultas = relationship("Consulta", back_populates="paciente")

class Consulta(Base):
    __tablename__ = "consultas"
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    profissional_id = Column(Integer, ForeignKey("profissionais.id"))
    tipo_consulta = Column(String)
    data_hora = Column(DateTime, default=datetime.datetime.utcnow)
    data_retorno = Column(DateTime, nullable=True)
    valor_total = Column(Float)
    forma_pagamento = Column(String)

    paciente = relationship("Paciente", back_populates="consultas")
    veterinario = relationship("Profissional", back_populates="consultas")