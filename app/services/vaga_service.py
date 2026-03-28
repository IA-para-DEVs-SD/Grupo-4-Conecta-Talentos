"""Service layer para operações de Vagas."""

import math
from typing import Optional, Tuple, List

from sqlalchemy.orm import Session

from app.models.domain import Vaga, VagaCreate
from app.repositories.vaga_repository import VagaRepository
from app.schemas.vaga_schema import VagaCreateSchema


class VagaNotFoundError(Exception):
    """Vaga não encontrada."""
    pass


class VagaService:
    def __init__(self, db: Session):
        self.repo = VagaRepository(db)

    def criar(self, schema: VagaCreateSchema) -> Vaga:
        """Cria uma nova vaga com dados validados."""
        dados = VagaCreate(
            titulo=schema.titulo,
            descricao=schema.descricao,
            requisitos_tecnicos=schema.requisitos_tecnicos,
            experiencia_minima=schema.experiencia_minima,
            competencias_desejadas=schema.competencias_desejadas,
        )
        return self.repo.criar(dados)

    def listar_paginado(
        self, pagina: int = 1, por_pagina: int = 10
    ) -> Tuple[List[Vaga], int, int]:
        """Retorna vagas paginadas: (vagas, total, total_paginas)."""
        todas = self.repo.listar()
        total = len(todas)
        total_paginas = max(1, math.ceil(total / por_pagina))
        inicio = (pagina - 1) * por_pagina
        fim = inicio + por_pagina
        return todas[inicio:fim], total, total_paginas

    def obter(self, vaga_id: int) -> Vaga:
        """Obtém vaga por ID ou levanta VagaNotFoundError."""
        vaga = self.repo.obter(vaga_id)
        if not vaga:
            raise VagaNotFoundError(f"Vaga #{vaga_id} não encontrada.")
        return vaga

    def atualizar(self, vaga_id: int, schema: VagaCreateSchema) -> Vaga:
        """Atualiza vaga existente ou levanta VagaNotFoundError."""
        dados = VagaCreate(
            titulo=schema.titulo,
            descricao=schema.descricao,
            requisitos_tecnicos=schema.requisitos_tecnicos,
            experiencia_minima=schema.experiencia_minima,
            competencias_desejadas=schema.competencias_desejadas,
        )
        vaga = self.repo.atualizar(vaga_id, dados)
        if not vaga:
            raise VagaNotFoundError(f"Vaga #{vaga_id} não encontrada.")
        return vaga

    def deletar(self, vaga_id: int) -> bool:
        """Deleta vaga ou levanta VagaNotFoundError."""
        if not self.repo.deletar(vaga_id):
            raise VagaNotFoundError(f"Vaga #{vaga_id} não encontrada.")
        return True
