"""Análise de candidatos via OpenAI LLM."""

import json
import logging
from dataclasses import dataclass
from typing import List

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """Você é um especialista em recrutamento e seleção.
Analise o candidato em relação à vaga e retorne APENAS um JSON válido com:
{
  "score": <número de 0 a 100>,
  "justificativa": "<máximo 3 frases explicando o score>",
  "pontos_fortes": ["<ponto 1>", "<ponto 2>"],
  "gaps": ["<gap 1>", "<gap 2>"]
}

Critérios:
- Adequação técnica aos requisitos (40%)
- Experiência relevante (30%)
- Competências comportamentais (20%)
- Formação acadêmica (10%)"""


@dataclass
class AnaliseResultado:
    score: int
    justificativa: str
    pontos_fortes: List[str]
    gaps: List[str]
    tokens_usados: int


class LLMError(Exception):
    pass


class LLMIndisponivelError(LLMError):
    pass


class AnalisadorLLM:
    def __init__(self):
        from app.config import get_settings
        settings = get_settings()
        self.api_key = settings.openai_api_key
        self.model = settings.openai_model
        self.max_tokens = settings.openai_max_tokens

    def analisar(self, prompt_otimizado: str) -> AnaliseResultado:
        """Envia prompt ao LLM e retorna análise estruturada."""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)

            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt_otimizado},
                ],
                temperature=0.3,
                max_tokens=500,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            tokens_usados = response.usage.total_tokens
            resultado = json.loads(content)

            return AnaliseResultado(
                score=int(resultado["score"]),
                justificativa=resultado["justificativa"],
                pontos_fortes=resultado.get("pontos_fortes", []),
                gaps=resultado.get("gaps", []),
                tokens_usados=tokens_usados,
            )

        except json.JSONDecodeError as e:
            raise LLMError(f"Resposta do LLM não é JSON válido: {e}") from e
        except Exception as e:
            raise LLMIndisponivelError(f"Erro ao chamar LLM: {e}") from e
