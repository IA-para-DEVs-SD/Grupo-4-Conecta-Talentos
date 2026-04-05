import logging
import uuid
from pathlib import Path

from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.domain import Curriculo
from app.processors.anonimizador import AnonimizadorError, Anonimizador
from app.processors.extrator_pdf import PDFError, extrair_texto_pdf
from app.repositories.curriculo_repository import CurriculoRepository
from app.repositories.vaga_repository import VagaRepository
from backend.src.services.extrator_pdf import ExtratorPDF

logger = logging.getLogger(__name__)

PDF_MAGIC_BYTES = b"%PDF"


class CurriculoError(Exception):
    pass


class ArquivoInvalidoError(CurriculoError):
    pass


class ArquivoMuitoGrandeError(CurriculoError):
    pass


class VagaNaoEncontradaError(CurriculoError):
    pass


class CurriculoNaoEncontradoError(CurriculoError):
    pass


def validar_pdf(conteudo: bytes, nome_arquivo: str, max_size_mb: int = 10) -> None:
    if len(conteudo) == 0:
        raise ArquivoInvalidoError("O arquivo está vazio.")

    if not nome_arquivo.lower().endswith(".pdf"):
        raise ArquivoInvalidoError("Formato inválido. Apenas arquivos PDF são aceitos.")

    if not conteudo[:4].startswith(PDF_MAGIC_BYTES):
        raise ArquivoInvalidoError(
            "O arquivo não é um PDF válido. Verifique o conteúdo."
        )

    max_bytes = max_size_mb * 1024 * 1024
    if len(conteudo) > max_bytes:
        raise ArquivoMuitoGrandeError(f"O arquivo excede o limite de {max_size_mb} MB.")

    if len(conteudo) == 0:
        raise ArquivoInvalidoError("O arquivo está vazio.")


def _gerar_caminho_unico(upload_dir: str, vaga_id: int, nome_original: str) -> Path:
    pasta_vaga = Path(upload_dir) / f"vaga_{vaga_id}"
    pasta_vaga.mkdir(parents=True, exist_ok=True)
    nome_unico = f"{uuid.uuid4().hex[:12]}_{nome_original}"
    return pasta_vaga / nome_unico


class CurriculoService:
    def __init__(self, db: Session):
        self.repo = CurriculoRepository(db)
        self.vaga_repo = VagaRepository(db)
        self.settings = get_settings()
        self.extrator = ExtratorPDF()

    def _extrair_e_persistir(self, curriculo: Curriculo) -> Curriculo:
        """Pipeline: extrai texto do PDF e anonimiza. Erros não interrompem o fluxo."""
        # Etapa 1: extração
        try:
            resultado = extrair_texto_pdf(
                Path(curriculo.caminho_pdf),
                max_paginas=self.settings.max_pdf_pages,
            )
            curriculo.texto_extraido = resultado.conteudo
            curriculo.status = "extraido"
        except PDFError as e:
            logger.warning("Falha na extração do currículo #%s: %s", curriculo.id, e)
            curriculo.status = "erro_extracao"
            return self.repo.atualizar(curriculo) or curriculo
        except Exception as e:
            logger.error("Erro inesperado na extração do currículo #%s: %s", curriculo.id, e)
            curriculo.status = "erro_extracao"
            return self.repo.atualizar(curriculo) or curriculo

        # Etapa 2: anonimização (falha não bloqueia — texto extraído já tem valor)
        try:
            anonimizador = Anonimizador(
                linguagem=self.settings.presidio_language,
                usar_fallback_regex=True,
            )
            resultado_anon = anonimizador.anonimizar(curriculo.texto_extraido)
            curriculo.texto_anonimizado = resultado_anon.texto_anonimizado
            curriculo.status = "anonimizado"
            logger.info(
                "Currículo #%s anonimizado via %s — %d substituições",
                curriculo.id,
                anonimizador.modo,
                resultado_anon.total_substituicoes,
            )
        except AnonimizadorError as e:
            logger.warning(
                "Anonimização falhou para currículo #%s (texto extraído preservado): %s",
                curriculo.id,
                e,
            )
        except Exception as e:
            logger.error(
                "Erro inesperado na anonimização do currículo #%s: %s", curriculo.id, e
            )

        return self.repo.atualizar(curriculo) or curriculo

    def upload(self, vaga_id: int, nome_arquivo: str, conteudo: bytes) -> Curriculo:
        if not self.vaga_repo.obter(vaga_id):
            raise VagaNaoEncontradaError(f"Vaga #{vaga_id} não encontrada.")

        validar_pdf(conteudo, nome_arquivo, self.settings.max_file_size_mb)

        caminho = _gerar_caminho_unico(self.settings.upload_dir, vaga_id, nome_arquivo)
        caminho.write_bytes(conteudo)

        # Extrai texto do PDF
        try:
            resultado = self.extrator.extrair_texto(caminho)
            texto_extraido = resultado.conteudo
        except Exception as e:
            print(f"Erro ao extrair texto do PDF {nome_arquivo}: {e}")
            texto_extraido = None

        return self.repo.criar(
            vaga_id=vaga_id,
            nome_arquivo=nome_arquivo,
            caminho_pdf=str(caminho),
            texto_extraido=texto_extraido,
        )
        return self._extrair_e_persistir(curriculo)

    def upload_multiplos(
        self, vaga_id: int, arquivos: list
    ) -> tuple[list[Curriculo], list[str]]:
        if not self.vaga_repo.obter(vaga_id):
            raise VagaNaoEncontradaError(f"Vaga #{vaga_id} não encontrada.")

        sucessos = []
        erros = []
        for nome, conteudo in arquivos:
            try:
                validar_pdf(conteudo, nome, self.settings.max_file_size_mb)
                caminho = _gerar_caminho_unico(self.settings.upload_dir, vaga_id, nome)
                caminho.write_bytes(conteudo)
                
                # Extrai texto do PDF
                try:
                    resultado = self.extrator.extrair_texto(caminho)
                    texto_extraido = resultado.conteudo
                except Exception as e:
                    print(f"Erro ao extrair texto do PDF {nome}: {e}")
                    texto_extraido = None
                
                curriculo = self.repo.criar(
                    vaga_id=vaga_id,
                    nome_arquivo=nome,
                    caminho_pdf=str(caminho),
                    texto_extraido=texto_extraido,
                )
                curriculo = self._extrair_e_persistir(curriculo)
                sucessos.append(curriculo)
            except CurriculoError as e:
                erros.append(f"{nome}: {e}")
        return sucessos, erros

    def listar_por_vaga(self, vaga_id: int) -> list[Curriculo]:
        return self.repo.listar_por_vaga(vaga_id)

    def obter(self, curriculo_id: int) -> Curriculo:
        curriculo = self.repo.obter(curriculo_id)
        if not curriculo:
            raise CurriculoNaoEncontradoError(
                f"Currículo #{curriculo_id} não encontrado."
            )
        return curriculo

    def deletar(self, curriculo_id: int) -> bool:
        if not self.repo.deletar(curriculo_id):
            raise CurriculoNaoEncontradoError(
                f"Currículo #{curriculo_id} não encontrado."
            )
        return True
