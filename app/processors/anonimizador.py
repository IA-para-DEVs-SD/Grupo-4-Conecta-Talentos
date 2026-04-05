"""Anonimização de dados sensíveis usando Microsoft Presidio (LGPD).

Substitui PII (nomes, CPF, e-mails, telefones, endereços) por placeholders
preservando informações profissionais relevantes para análise de currículos.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

# Placeholders usados na substituição
_PLACEHOLDERS: dict[str, str] = {
    "PERSON": "[NOME]",
    "EMAIL_ADDRESS": "[EMAIL]",
    "PHONE_NUMBER": "[TELEFONE]",
    "BR_CPF": "[CPF]",
    "LOCATION": "[ENDERECO]",
    "URL": "[URL]",
}


class AnonimizadorError(Exception):
    """Erro base do módulo de anonimização."""


class PresidioIndisponivelError(AnonimizadorError):
    """Presidio não está instalado ou não pôde ser inicializado."""


@dataclass
class ResultadoAnonimizacao:
    texto_anonimizado: str
    entidades_encontradas: list[str] = field(default_factory=list)
    total_substituicoes: int = 0
    sucesso: bool = True
    erro: str | None = None


def _criar_engine_presidio(linguagem: str):
    """Inicializa AnalyzerEngine e AnonymizerEngine do Presidio.

    Raises:
        PresidioIndisponivelError: Se presidio ou spacy não estiverem instalados.
    """
    try:
        from presidio_analyzer import AnalyzerEngine
        from presidio_analyzer.nlp_engine import NlpEngineProvider
        from presidio_anonymizer import AnonymizerEngine
        from presidio_anonymizer.entities import OperatorConfig
    except ImportError as e:
        raise PresidioIndisponivelError(
            "Microsoft Presidio não está instalado. "
            "Execute: pip install presidio-analyzer presidio-anonymizer"
        ) from e

    try:
        nlp_config = {
            "nlp_engine_name": "spacy",
            "models": [{"lang_code": linguagem, "model_name": "pt_core_news_lg"}],
        }
        provider = NlpEngineProvider(nlp_configuration=nlp_config)
        nlp_engine = provider.create_engine()
        analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=[linguagem])
    except Exception as e:
        raise PresidioIndisponivelError(
            f"Falha ao inicializar NLP engine para '{linguagem}'. "
            "Verifique se o modelo spaCy está instalado: "
            "python -m spacy download pt_core_news_lg"
        ) from e

    operators = {
        entity: OperatorConfig("replace", {"new_value": placeholder})
        for entity, placeholder in _PLACEHOLDERS.items()
    }
    anonymizer = AnonymizerEngine()
    return analyzer, anonymizer, operators


class Anonimizador:
    """Anonimiza dados pessoais sensíveis em textos de currículos.

    Usa Microsoft Presidio com modelo spaCy em português para detectar e
    substituir PII, preservando informações profissionais.

    Quando Presidio não está disponível, usa fallback via regex para garantir
    que CPF, e-mail e telefone sejam sempre anonimizados.

    Example:
        >>> anon = Anonimizador()
        >>> resultado = anon.anonimizar("João Silva, CPF 123.456.789-09, joao@email.com")
        >>> print(resultado.texto_anonimizado)
        [NOME], CPF [CPF], [EMAIL]
    """

    # Padrões regex de fallback
    _REGEX_CPF = re.compile(r"\d{3}[.\s]?\d{3}[.\s]?\d{3}[-\s]?\d{2}")
    _REGEX_EMAIL = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
    _REGEX_TELEFONE = re.compile(
        r"(?:\+55\s?)?(?:\(?\d{2}\)?\s?)?(?:9\s?)?\d{4}[-\s]?\d{4}"
    )
    _REGEX_CEP = re.compile(r"\d{5}-?\d{3}")

    def __init__(self, linguagem: str = "pt", usar_fallback_regex: bool = True):
        """
        Args:
            linguagem: Código de idioma para o Presidio (padrão: "pt").
            usar_fallback_regex: Se True, usa regex quando Presidio não está disponível.
        """
        self.linguagem = linguagem
        self.usar_fallback_regex = usar_fallback_regex
        self._analyzer = None
        self._anonymizer = None
        self._operators = None
        self._presidio_disponivel = False
        self._inicializar()

    def _inicializar(self) -> None:
        try:
            self._analyzer, self._anonymizer, self._operators = _criar_engine_presidio(
                self.linguagem
            )
            self._presidio_disponivel = True
            logger.info("Presidio inicializado com sucesso (linguagem: %s)", self.linguagem)
        except PresidioIndisponivelError as e:
            if self.usar_fallback_regex:
                logger.warning(
                    "Presidio indisponível, usando fallback regex. Motivo: %s", e
                )
            else:
                raise

    def anonimizar(self, texto: str) -> ResultadoAnonimizacao:
        """Anonimiza dados sensíveis no texto.

        Args:
            texto: Texto extraído do currículo.

        Returns:
            ResultadoAnonimizacao com texto substituído e metadados.
        """
        if not texto or not texto.strip():
            return ResultadoAnonimizacao(texto_anonimizado=texto)

        if self._presidio_disponivel:
            return self._anonimizar_presidio(texto)
        return self._anonimizar_regex(texto)

    def _anonimizar_presidio(self, texto: str) -> ResultadoAnonimizacao:
        try:
            entidades_alvo = list(_PLACEHOLDERS.keys())
            resultados = self._analyzer.analyze(
                text=texto,
                language=self.linguagem,
                entities=entidades_alvo,
            )

            if not resultados:
                return ResultadoAnonimizacao(
                    texto_anonimizado=texto,
                    entidades_encontradas=[],
                    total_substituicoes=0,
                )

            anonimizado = self._anonymizer.anonymize(
                text=texto,
                analyzer_results=resultados,
                operators=self._operators,
            )

            entidades = list({r.entity_type for r in resultados})
            return ResultadoAnonimizacao(
                texto_anonimizado=anonimizado.text,
                entidades_encontradas=entidades,
                total_substituicoes=len(resultados),
            )
        except Exception as e:
            logger.error("Erro no Presidio, usando fallback regex: %s", e)
            return self._anonimizar_regex(texto)

    def _anonimizar_regex(self, texto: str) -> ResultadoAnonimizacao:
        """Fallback: anonimização via expressões regulares."""
        resultado = texto
        substituicoes = 0
        entidades: list[str] = []

        for padrao, placeholder, tipo in [
            (self._REGEX_CPF, "[CPF]", "BR_CPF"),
            (self._REGEX_EMAIL, "[EMAIL]", "EMAIL_ADDRESS"),
            (self._REGEX_TELEFONE, "[TELEFONE]", "PHONE_NUMBER"),
            (self._REGEX_CEP, "[CEP]", "LOCATION"),
        ]:
            matches = padrao.findall(resultado)
            if matches:
                resultado = padrao.sub(placeholder, resultado)
                substituicoes += len(matches)
                entidades.append(tipo)

        return ResultadoAnonimizacao(
            texto_anonimizado=resultado,
            entidades_encontradas=entidades,
            total_substituicoes=substituicoes,
        )

    @property
    def modo(self) -> str:
        """Retorna o modo de operação: 'presidio' ou 'regex'."""
        return "presidio" if self._presidio_disponivel else "regex"
