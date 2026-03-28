from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class VagaORM(Base):
    __tablename__ = "vagas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=False)
    requisitos_tecnicos = Column(Text, nullable=False)   # JSON list
    experiencia_minima = Column(String(100), nullable=False)
    competencias_desejadas = Column(Text, nullable=False)  # JSON list
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    curriculos = relationship("CurriculoORM", back_populates="vaga", cascade="all, delete-orphan")


class CurriculoORM(Base):
    __tablename__ = "curriculos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    vaga_id = Column(Integer, ForeignKey("vagas.id", ondelete="CASCADE"), nullable=False)
    nome_arquivo = Column(String(255), nullable=False)
    caminho_pdf = Column(String(500), nullable=False)
    texto_extraido = Column(Text)
    texto_anonimizado = Column(Text)
    status = Column(String(50), default="pendente")
    enviado_em = Column(DateTime, default=datetime.utcnow)

    vaga = relationship("VagaORM", back_populates="curriculos")
    analise = relationship(
        "AnaliseORM", back_populates="curriculo", uselist=False, cascade="all, delete-orphan"
    )


class AnaliseORM(Base):
    __tablename__ = "analises"

    id = Column(Integer, primary_key=True, autoincrement=True)
    curriculo_id = Column(
        Integer, ForeignKey("curriculos.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    score = Column(Integer, nullable=False)
    justificativa = Column(Text, nullable=False)
    pontos_fortes = Column(Text, nullable=False)   # JSON list
    gaps = Column(Text, nullable=False)            # JSON list
    tokens_usados = Column(Integer, nullable=False)
    analisado_em = Column(DateTime, default=datetime.utcnow)

    curriculo = relationship("CurriculoORM", back_populates="analise")

    __table_args__ = (
        CheckConstraint("score >= 0 AND score <= 100", name="check_score_range"),
    )
