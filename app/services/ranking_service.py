"""Serviço para geração de ranking de candidatos."""

from sqlalchemy.orm import Session

from app.models.domain import Analise, Curriculo, Vaga
from app.processors.analisador_llm import AnalisadorLLM
from app.processors.exceptions import LLMError
from app.repositories.analise_repository import AnaliseRepository
from app.repositories.curriculo_repository import CurriculoRepository
from app.repositories.vaga_repository import VagaRepository


class RankingService:
    """Serviço para geração e gerenciamento de rankings de candidatos.

    Orquestra a análise de múltiplos currículos para uma vaga e
    gera rankings ordenados por pontuação.

    Attributes:
        db: Sessão do banco de dados
        vaga_repo: Repositório de vagas
        curriculo_repo: Repositório de currículos
        analise_repo: Repositório de análises
        analisador: Analisador LLM para análise de currículos
    """

    def __init__(self, db: Session):
        """Inicializa o serviço de ranking.

        Args:
            db: Sessão do banco de dados
        """
        self.db = db
        self.vaga_repo = VagaRepository(db)
        self.curriculo_repo = CurriculoRepository(db)
        self.analise_repo = AnaliseRepository(db)
        self.analisador = AnalisadorLLM()

    def gerar_ranking(self, vaga_id: int, reprocessar: bool = False) -> list[Analise]:
        """Gera ranking de candidatos para uma vaga.

        Analisa todos os currículos da vaga e retorna lista ordenada
        por pontuação (maior para menor).

        Args:
            vaga_id: ID da vaga
            reprocessar: Se True, reanalisa currículos já analisados.
                        Se False, usa análises existentes quando disponíveis.

        Returns:
            Lista de análises ordenadas por score (decrescente)

        Raises:
            ValueError: Se a vaga não existir
            LLMError: Se houver erro na análise de algum currículo
        """
        # Busca vaga
        vaga = self.vaga_repo.obter_por_id(vaga_id)
        if not vaga:
            raise ValueError(f"Vaga com ID {vaga_id} não encontrada")

        # Busca currículos da vaga
        curriculos = self.curriculo_repo.listar_por_vaga(vaga_id)

        if not curriculos:
            return []

        analises = []

        for curriculo in curriculos:
            # Verifica se já existe análise
            analise_existente = self.analise_repo.obter_por_curriculo(curriculo.id)

            if analise_existente and not reprocessar:
                # Usa análise existente
                analises.append(analise_existente)
            else:
                # Realiza nova análise
                try:
                    resultado = self.analisador.analisar(
                        texto_vaga=self._formatar_texto_vaga(vaga),
                        texto_curriculo=curriculo.texto_extraido,
                        curriculo_id=curriculo.id,
                        vaga_id=vaga_id,
                    )

                    # Cria objeto de domínio Analise
                    analise = Analise(
                        id=None,
                        curriculo_id=resultado.curriculo_id,
                        score=resultado.score,
                        justificativa=resultado.justificativa,
                        pontos_fortes=resultado.pontos_fortes,
                        gaps=resultado.gaps,
                        tokens_usados=resultado.tokens_usados,
                        analisado_em=resultado.data_analise,
                    )

                    # Salva no banco
                    analise_salva = self.analise_repo.criar(analise)
                    analises.append(analise_salva)

                except LLMError as e:
                    # Log do erro mas continua processando outros currículos
                    print(f"Erro ao analisar currículo {curriculo.id}: {e}")
                    continue

        # Ordena por score (maior para menor)
        analises_ordenadas = sorted(analises, key=lambda a: a.score, reverse=True)

        return analises_ordenadas

    async def gerar_ranking_async(
        self, vaga_id: int, reprocessar: bool = False
    ) -> list[Analise]:
        """Versão assíncrona da geração de ranking.

        Args:
            vaga_id: ID da vaga
            reprocessar: Se True, reanalisa currículos já analisados

        Returns:
            Lista de análises ordenadas por score (decrescente)

        Raises:
            ValueError: Se a vaga não existir
            LLMError: Se houver erro na análise de algum currículo
        """
        # Busca vaga
        vaga = self.vaga_repo.obter_por_id(vaga_id)
        if not vaga:
            raise ValueError(f"Vaga com ID {vaga_id} não encontrada")

        # Busca currículos da vaga
        curriculos = self.curriculo_repo.listar_por_vaga(vaga_id)

        if not curriculos:
            return []

        analises = []

        for curriculo in curriculos:
            # Verifica se já existe análise
            analise_existente = self.analise_repo.obter_por_curriculo(curriculo.id)

            if analise_existente and not reprocessar:
                analises.append(analise_existente)
            else:
                # Realiza nova análise de forma assíncrona
                try:
                    resultado = await self.analisador.analisar_async(
                        texto_vaga=self._formatar_texto_vaga(vaga),
                        texto_curriculo=curriculo.texto_extraido,
                        curriculo_id=curriculo.id,
                        vaga_id=vaga_id,
                    )

                    # Cria objeto de domínio Analise
                    analise = Analise(
                        id=None,
                        curriculo_id=resultado.curriculo_id,
                        score=resultado.score,
                        justificativa=resultado.justificativa,
                        pontos_fortes=resultado.pontos_fortes,
                        gaps=resultado.gaps,
                        tokens_usados=resultado.tokens_usados,
                        analisado_em=resultado.data_analise,
                    )

                    # Salva no banco
                    analise_salva = self.analise_repo.criar(analise)
                    analises.append(analise_salva)

                except LLMError as e:
                    print(f"Erro ao analisar currículo {curriculo.id}: {e}")
                    continue

        # Ordena por score (maior para menor)
        analises_ordenadas = sorted(analises, key=lambda a: a.score, reverse=True)

        return analises_ordenadas

    def obter_ranking_existente(self, vaga_id: int) -> list[Analise]:
        """Obtém ranking existente sem reprocessar.

        Retorna apenas análises já realizadas, ordenadas por score.

        Args:
            vaga_id: ID da vaga

        Returns:
            Lista de análises ordenadas por score (decrescente)

        Raises:
            ValueError: Se a vaga não existir
        """
        # Verifica se vaga existe
        vaga = self.vaga_repo.obter_por_id(vaga_id)
        if not vaga:
            raise ValueError(f"Vaga com ID {vaga_id} não encontrada")

        # Busca análises existentes (já vem ordenado do repositório)
        analises = self.analise_repo.listar_por_vaga(vaga_id)

        return analises

    def filtrar_por_score_minimo(
        self, analises: list[Analise], score_minimo: int
    ) -> list[Analise]:
        """Filtra análises por pontuação mínima.

        Args:
            analises: Lista de análises
            score_minimo: Pontuação mínima (0-100)

        Returns:
            Lista filtrada de análises
        """
        return [a for a in analises if a.score >= score_minimo]

    def obter_top_candidatos(self, vaga_id: int, limite: int = 10) -> list[Analise]:
        """Obtém os N melhores candidatos de uma vaga.

        Args:
            vaga_id: ID da vaga
            limite: Número máximo de candidatos a retornar

        Returns:
            Lista com os N melhores candidatos

        Raises:
            ValueError: Se a vaga não existir
        """
        analises = self.obter_ranking_existente(vaga_id)
        return analises[:limite]

    def _formatar_texto_vaga(self, vaga: Vaga) -> str:
        """Formata informações da vaga para análise.

        Args:
            vaga: Objeto Vaga

        Returns:
            Texto formatado da vaga
        """
        texto = f"""Título: {vaga.titulo}

Descrição:
{vaga.descricao}

Requisitos:
{vaga.requisitos}
"""

        if vaga.experiencia_minima:
            texto += f"\nExperiência Mínima: {vaga.experiencia_minima}"

        if vaga.competencias:
            texto += f"\n\nCompetências Desejadas:\n{vaga.competencias}"

        return texto.strip()
