"""Otimizador de prompts para reduzir consumo de tokens."""

import re
from typing import Any

import tiktoken

from app.config import Settings, get_settings
from app.processors.exceptions import TokenLimitExceededError


class OtimizadorPrompt:
    """Otimiza prompts para minimizar o consumo de tokens.

    Fornece métodos para contar, truncar e otimizar textos antes de
    enviar para a API do LLM, reduzindo custos e respeitando limites.

    Attributes:
        settings: Configurações da aplicação
        encoding: Encoder tiktoken para o modelo configurado
    """

    def __init__(self, settings: Settings | None = None):
        """Inicializa o otimizador de prompts.

        Args:
            settings: Configurações da aplicação. Se None, usa get_settings()
        """
        self.settings = settings or get_settings()
        
        # Usa encoding cl100k_base que funciona com GPT-4 e GPT-4o
        # Este é o encoding padrão para modelos GPT-4
        try:
            self.encoding = tiktoken.encoding_for_model(self.settings.openai_model)
        except KeyError:
            # Se o modelo não for reconhecido, usa o encoding padrão do GPT-4
            self.encoding = tiktoken.get_encoding("cl100k_base")

    def contar_tokens(self, texto: str) -> int:
        """Conta o número de tokens em um texto.

        Args:
            texto: Texto para contar tokens

        Returns:
            Número de tokens no texto
        """
        return len(self.encoding.encode(texto))

    def contar_tokens_mensagens(self, mensagens: list[dict[str, str]]) -> int:
        """Conta tokens em uma lista de mensagens do formato OpenAI.

        Args:
            mensagens: Lista de mensagens no formato [{"role": "...", "content": "..."}]

        Returns:
            Número total de tokens nas mensagens
        """
        total = 0
        for mensagem in mensagens:
            # Conta tokens do role e content
            total += self.contar_tokens(mensagem.get("role", ""))
            total += self.contar_tokens(mensagem.get("content", ""))
            # Adiciona overhead por mensagem (formato do chat)
            total += 4  # Overhead aproximado por mensagem

        total += 2  # Overhead da resposta
        return total

    def truncar_texto(
        self, texto: str, max_tokens: int, preservar_inicio: bool = True
    ) -> str:
        """Trunca texto para caber no limite de tokens.

        Args:
            texto: Texto a ser truncado
            max_tokens: Número máximo de tokens permitido
            preservar_inicio: Se True, preserva o início do texto.
                            Se False, preserva o final.

        Returns:
            Texto truncado
        """
        tokens = self.encoding.encode(texto)

        if len(tokens) <= max_tokens:
            return texto

        if preservar_inicio:
            tokens_truncados = tokens[:max_tokens]
        else:
            tokens_truncados = tokens[-max_tokens:]

        return self.encoding.decode(tokens_truncados)

    def remover_espacos_extras(self, texto: str) -> str:
        """Remove espaços em branco extras do texto.

        Args:
            texto: Texto a ser otimizado

        Returns:
            Texto sem espaços extras
        """
        # Remove múltiplos espaços
        texto = re.sub(r" +", " ", texto)
        # Remove múltiplas quebras de linha
        texto = re.sub(r"\n\n+", "\n\n", texto)
        # Remove espaços no início e fim de linhas
        texto = "\n".join(linha.strip() for linha in texto.split("\n"))
        return texto.strip()

    def comprimir_curriculo(self, texto_curriculo: str, max_tokens: int) -> str:
        """Comprime texto de currículo mantendo informações essenciais.

        Remove redundâncias e informações menos relevantes, priorizando:
        - Experiências profissionais
        - Formação acadêmica
        - Habilidades técnicas

        Args:
            texto_curriculo: Texto completo do currículo
            max_tokens: Número máximo de tokens permitido

        Returns:
            Texto do currículo otimizado
        """
        # Remove espaços extras primeiro
        texto = self.remover_espacos_extras(texto_curriculo)

        # Se já está dentro do limite, retorna
        if self.contar_tokens(texto) <= max_tokens:
            return texto

        # Estratégia: preservar seções importantes
        # Divide em parágrafos e prioriza os primeiros (geralmente mais importantes)
        paragrafos = texto.split("\n\n")

        texto_otimizado = ""
        tokens_usados = 0

        for paragrafo in paragrafos:
            tokens_paragrafo = self.contar_tokens(paragrafo)

            if tokens_usados + tokens_paragrafo <= max_tokens:
                texto_otimizado += paragrafo + "\n\n"
                tokens_usados += tokens_paragrafo
            else:
                # Tenta adicionar parte do parágrafo
                tokens_restantes = max_tokens - tokens_usados
                if tokens_restantes > 50:  # Mínimo útil
                    texto_otimizado += self.truncar_texto(
                        paragrafo, tokens_restantes, preservar_inicio=True
                    )
                break

        return texto_otimizado.strip()

    def comprimir_vaga(self, texto_vaga: str, max_tokens: int) -> str:
        """Comprime descrição de vaga mantendo requisitos essenciais.

        Args:
            texto_vaga: Texto completo da vaga
            max_tokens: Número máximo de tokens permitido

        Returns:
            Texto da vaga otimizado
        """
        # Remove espaços extras
        texto = self.remover_espacos_extras(texto_vaga)

        # Se já está dentro do limite, retorna
        if self.contar_tokens(texto) <= max_tokens:
            return texto

        # Trunca preservando o início (requisitos geralmente vêm primeiro)
        return self.truncar_texto(texto, max_tokens, preservar_inicio=True)

    def otimizar_prompt_analise(
        self,
        texto_vaga: str,
        texto_curriculo: str,
        max_tokens_total: int | None = None,
    ) -> tuple[str, str]:
        """Otimiza textos de vaga e currículo para análise.

        Distribui tokens de forma balanceada entre vaga e currículo,
        garantindo que o prompt completo caiba no limite.

        Args:
            texto_vaga: Texto da descrição da vaga
            texto_curriculo: Texto do currículo
            max_tokens_total: Limite total de tokens. Se None, usa configuração.

        Returns:
            Tupla (vaga_otimizada, curriculo_otimizado)

        Raises:
            TokenLimitExceededError: Se não for possível otimizar dentro do limite
        """
        max_tokens = max_tokens_total or self.settings.openai_max_tokens

        # Reserva tokens para o prompt do sistema e resposta (~500 tokens)
        tokens_disponiveis = max_tokens - 500

        if tokens_disponiveis < 100:
            raise TokenLimitExceededError(
                "Limite de tokens muito baixo para análise",
                token_count=max_tokens,
                max_tokens=max_tokens,
            )

        # Distribui tokens: 30% para vaga, 70% para currículo
        tokens_vaga = int(tokens_disponiveis * 0.3)
        tokens_curriculo = int(tokens_disponiveis * 0.7)

        vaga_otimizada = self.comprimir_vaga(texto_vaga, tokens_vaga)
        curriculo_otimizado = self.comprimir_curriculo(
            texto_curriculo, tokens_curriculo
        )

        return vaga_otimizada, curriculo_otimizado

    def validar_limite(
        self, mensagens: list[dict[str, str]], max_tokens: int | None = None
    ) -> bool:
        """Valida se mensagens estão dentro do limite de tokens.

        Args:
            mensagens: Lista de mensagens no formato OpenAI
            max_tokens: Limite de tokens. Se None, usa configuração.

        Returns:
            True se está dentro do limite, False caso contrário
        """
        limite = max_tokens or self.settings.openai_max_tokens
        tokens_usados = self.contar_tokens_mensagens(mensagens)
        return tokens_usados <= limite

    def obter_estatisticas(self, texto: str) -> dict[str, Any]:
        """Obtém estatísticas sobre um texto.

        Args:
            texto: Texto para análise

        Returns:
            Dicionário com estatísticas (tokens, caracteres, palavras, linhas)
        """
        tokens = self.contar_tokens(texto)
        caracteres = len(texto)
        palavras = len(texto.split())
        linhas = len(texto.split("\n"))

        return {
            "tokens": tokens,
            "caracteres": caracteres,
            "palavras": palavras,
            "linhas": linhas,
            "razao_tokens_palavras": round(tokens / palavras, 2) if palavras > 0 else 0,
        }
