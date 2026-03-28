"""Pipeline completo: extração → anonimização → otimização → análise LLM."""

import logging
from pathlib import Path
from sqlalchemy.orm import Session

from app.models.domain import Vaga, Curriculo, Analise
from app.processors.extrator_pdf import ExtratorPDF, PDFError
from app.processors.anonimizador import Anonimizador, AnonimizacaoError
from app.processors.otimizador_prompt import OtimizadorPrompt
from app.processors.analisador_llm import AnalisadorLLM, LLMError
from app.repositories.curriculo_repository import CurriculoRepository
from app.repositories.analise_repository import AnaliseRepository

logger = logging.getLogger(__name__)


class ProcessamentoService:
    def __init__(self):
        self.extrator = ExtratorPDF()
        self.anonimizador = Anonimizador()
        self.otimizador = OtimizadorPrompt()
        self.analisador = AnalisadorLLM()

    def processar(self, curriculo: Curriculo, vaga: Vaga, db: Session) -> Analise:
        curriculo_repo = CurriculoRepository(db)
        analise_repo = AnaliseRepository(db)

        # 1. Extrair texto
        logger.info("Extraindo texto — currículo %s", curriculo.id)
        try:
            extraido = self.extrator.extrair_texto(Path(curriculo.caminho_pdf))
            curriculo.texto_extraido = extraido.conteudo
            curriculo.status = "extraido"
            curriculo_repo.atualizar(curriculo)
        except PDFError as e:
            logger.error("Erro PDF: %s", e)
            curriculo.status = "erro"
            curriculo_repo.atualizar(curriculo)
            raise

        # 2. Anonimizar (falha não-crítica)
        logger.info("Anonimizando — currículo %s", curriculo.id)
        try:
            anonimizado = self.anonimizador.anonimizar(curriculo.texto_extraido)
            curriculo.texto_anonimizado = anonimizado.conteudo
        except AnonimizacaoError as e:
            logger.warning("Anonimização falhou (não-crítico): %s", e)
            curriculo.texto_anonimizado = curriculo.texto_extraido
        curriculo_repo.atualizar(curriculo)

        # 3. Otimizar prompt
        prompt = self.otimizador.otimizar(vaga, curriculo.texto_anonimizado)
        logger.info("Tokens estimados: %d", prompt.tokens_estimados)

        # 4. Analisar com LLM
        logger.info("Analisando com LLM — currículo %s", curriculo.id)
        try:
            resultado = self.analisador.analisar(prompt.conteudo)
        except LLMError as e:
            logger.error("Erro LLM: %s", e)
            curriculo.status = "erro_llm"
            curriculo_repo.atualizar(curriculo)
            raise

        analise = analise_repo.criar(
            Analise(
                id=None,
                curriculo_id=curriculo.id,
                score=resultado.score,
                justificativa=resultado.justificativa,
                pontos_fortes=resultado.pontos_fortes,
                gaps=resultado.gaps,
                tokens_usados=resultado.tokens_usados,
            )
        )

        curriculo.status = "concluido"
        curriculo_repo.atualizar(curriculo)
        logger.info("Concluído — score: %d", analise.score)
        return analise
