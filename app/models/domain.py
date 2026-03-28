from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class VagaCreate:
    titulo: str
    descricao: str
    requisitos_tecnicos: List[str]
    experiencia_minima: str
    competencias_desejadas: List[str]


@dataclass
class Vaga:
    id: Optional[int]
    titulo: str
    descricao: str
    requisitos_tecnicos: List[str]
    experiencia_minima: str
    competencias_desejadas: List[str]
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None


@dataclass
class Curriculo:
    id: Optional[int]
    vaga_id: int
    nome_arquivo: str
    caminho_pdf: str
    texto_extraido: Optional[str] = None
    texto_anonimizado: Optional[str] = None
    status: str = "pendente"
    enviado_em: Optional[datetime] = None


@dataclass
class Analise:
    id: Optional[int]
    curriculo_id: int
    score: int
    justificativa: str
    pontos_fortes: List[str]
    gaps: List[str]
    tokens_usados: int
    analisado_em: Optional[datetime] = None
