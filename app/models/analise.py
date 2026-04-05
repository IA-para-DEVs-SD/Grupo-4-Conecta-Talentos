"""Modelos de domínio para análise de currículos."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class ResultadoAnalise:
    """Resultado da análise de um currículo contra uma vaga.

    Attributes:
        score: Pontuação de 0 a 100 indicando adequação à vaga
        justificativa: Explicação detalhada do score
        pontos_fortes: Lista de pontos fortes do candidato
        gaps: Lista de lacunas ou pontos de melhoria
        curriculo_id: ID do currículo analisado
        vaga_id: ID da vaga
        data_analise: Data e hora da análise
        tokens_usados: Número de tokens consumidos na análise
    """

    score: int
    justificativa: str
    pontos_fortes: list[str]
    gaps: list[str]
    curriculo_id: int
    vaga_id: int
    data_analise: datetime
    tokens_usados: int

    def __post_init__(self):
        """Valida os dados após inicialização."""
        if not 0 <= self.score <= 100:
            raise ValueError(f"Score deve estar entre 0 e 100, recebido: {self.score}")

        if not self.justificativa:
            raise ValueError("Justificativa não pode estar vazia")

        if not isinstance(self.pontos_fortes, list):
            raise ValueError("pontos_fortes deve ser uma lista")

        if not isinstance(self.gaps, list):
            raise ValueError("gaps deve ser uma lista")


@dataclass
class PromptAnalise:
    """Estrutura do prompt para análise de currículo.

    Attributes:
        sistema: Mensagem de sistema definindo o papel do LLM
        usuario: Mensagem do usuário com vaga e currículo
        formato_resposta: Formato esperado da resposta
    """

    sistema: str
    usuario: str
    formato_resposta: str

    def to_messages(self) -> list[dict[str, str]]:
        """Converte para formato de mensagens da OpenAI.

        Returns:
            Lista de mensagens no formato [{"role": "...", "content": "..."}]
        """
        return [
            {"role": "system", "content": self.sistema},
            {"role": "user", "content": self.usuario},
        ]
