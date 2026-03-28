import os
import shutil
from pathlib import Path
from typing import List
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.domain import Curriculo
from app.repositories.curriculo_repository import CurriculoRepository
from app.repositories.analise_repository import AnaliseRepository
from app.services.vaga_service import VagaService
from app.services.processamento_service import ProcessamentoService

settings = get_settings()


class CurriculoService:
    def __init__(self, db: Session):
        self.db = db
        self.curriculo_repo = CurriculoRepository(db)
        self.analise_repo = AnaliseRepository(db)

    def salvar_e_processar(self, vaga_id: int, nome_arquivo: str, conteudo: bytes) -> Curriculo:
        """Salva PDF em disco, persiste no banco e dispara pipeline."""
        # Garantir diretório
        upload_dir = Path(settings.upload_dir) / f"vaga_{vaga_id}"
        upload_dir.mkdir(parents=True, exist_ok=True)

        caminho = upload_dir / nome_arquivo
        caminho.write_bytes(conteudo)

        curriculo = self.curriculo_repo.criar(
            vaga_id=vaga_id,
            nome_arquivo=nome_arquivo,
            caminho_pdf=str(caminho),
        )

        # Buscar vaga e processar
        vaga_service = VagaService(self.db)
        vaga = vaga_service.obter_vaga(vaga_id)

        processamento = ProcessamentoService()
        processamento.processar(curriculo, vaga, self.db)

        return curriculo

    def listar_por_vaga(self, vaga_id: int) -> List[Curriculo]:
        return self.curriculo_repo.listar_por_vaga(vaga_id)
