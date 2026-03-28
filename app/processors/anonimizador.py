"""Anonimização de dados sensíveis via Microsoft Presidio (LGPD)."""

import logging
from dataclasses import dataclass
from typing import Dict, List

logger = logging.getLogger(__name__)


@dataclass
class TextoAnonimizado:
    conteudo: str
    substituicoes: Dict[str, List[str]]
    sucesso: bool


class AnonimizacaoError(Exception):
    pass


class Anonimizador:
    """Remove dados pessoais do texto usando Presidio."""

    ENTITY_MAPPING = {
        "PERSON": "[NOME]",
        "EMAIL_ADDRESS": "[EMAIL]",
        "PHONE_NUMBER": "[TELEFONE]",
        "LOCATION": "[ENDEREÇO]",
        "BR_CPF": "[CPF]",
    }

    def __init__(self, language: str = "pt"):
        self.language = language
        self._analyzer = None
        self._anonymizer = None

    def _get_engines(self):
        """Lazy-load Presidio engines (evita import lento no startup)."""
        if self._analyzer is None:
            from presidio_analyzer import AnalyzerEngine
            from presidio_anonymizer import AnonymizerEngine
            self._analyzer = AnalyzerEngine()
            self._anonymizer = AnonymizerEngine()
        return self._analyzer, self._anonymizer

    def anonimizar(self, texto: str) -> TextoAnonimizado:
        """Remove dados sensíveis e retorna texto anonimizado."""
        try:
            from presidio_anonymizer.entities import OperatorConfig

            analyzer, anonymizer = self._get_engines()

            results = analyzer.analyze(
                text=texto,
                language=self.language,
                entities=list(self.ENTITY_MAPPING.keys()),
            )

            operators = {
                entity: OperatorConfig("replace", {"new_value": token})
                for entity, token in self.ENTITY_MAPPING.items()
            }

            anonymized = anonymizer.anonymize(
                text=texto, analyzer_results=results, operators=operators
            )

            substituicoes: Dict[str, List[str]] = {}
            for r in results:
                substituicoes.setdefault(r.entity_type, []).append(texto[r.start:r.end])

            return TextoAnonimizado(
                conteudo=anonymized.text,
                substituicoes=substituicoes,
                sucesso=True,
            )

        except Exception as e:
            raise AnonimizacaoError(f"Falha na anonimização: {e}") from e
