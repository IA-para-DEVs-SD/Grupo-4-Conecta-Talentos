"""Otimização de prompts para reduzir custo de tokens no LLM."""

import json
from dataclasses import dataclass
from typing import Dict, Any
from app.models.domain import Vaga


@dataclass
class PromptOtimizado:
    conteudo: str
    tokens_estimados: int


class OtimizadorPrompt:
    def __init__(self, model: str = "gpt-4o-mini", max_tokens: int = 2000):
        self.model = model
        self.max_tokens = max_tokens
        self._encoding = None

    def _get_encoding(self):
        if self._encoding is None:
            import tiktoken
            self._encoding = tiktoken.encoding_for_model(self.model)
        return self._encoding

    def contar_tokens(self, texto: str) -> int:
        return len(self._get_encoding().encode(texto))

    def otimizar(self, vaga: Vaga, texto_anonimizado: str) -> PromptOtimizado:
        vaga_dict = {
            "titulo": vaga.titulo,
            "requisitos": vaga.requisitos_tecnicos,
            "experiencia": vaga.experiencia_minima,
            "competencias": vaga.competencias_desejadas,
        }
        candidato = self._extrair_secoes(texto_anonimizado)
        payload: Dict[str, Any] = {"vaga": vaga_dict, "candidato": candidato}

        conteudo = json.dumps(payload, ensure_ascii=False)
        tokens = self.contar_tokens(conteudo)

        if tokens > self.max_tokens:
            conteudo = self._resumir(payload)
            tokens = self.contar_tokens(conteudo)

        return PromptOtimizado(conteudo=conteudo, tokens_estimados=tokens)

    def _extrair_secoes(self, texto: str) -> Dict[str, str]:
        secoes: Dict[str, str] = {"experiencia": "", "formacao": "", "habilidades": ""}
        t = texto.lower()

        keywords = {
            "experiencia": ["experiência", "experiencia"],
            "formacao": ["formação", "formacao", "educação"],
            "habilidades": ["habilidades", "competências"],
        }

        for secao, kws in keywords.items():
            for kw in kws:
                idx = t.find(kw)
                if idx != -1:
                    fim = t.find("\n\n", idx + 100)
                    fim = fim if fim != -1 else idx + 500
                    secoes[secao] = texto[idx:fim].strip()
                    break

        return secoes

    def _resumir(self, payload: Dict[str, Any]) -> str:
        candidato = payload["candidato"]
        for secao in ("experiencia", "formacao", "habilidades"):
            if len(candidato.get(secao, "")) > 200:
                candidato[secao] = candidato[secao][:200] + "..."
        return json.dumps(payload, ensure_ascii=False)
