"""Analisador de currículos usando LLM."""

import json
import re
from datetime import datetime

from app.config import Settings, get_settings
from app.models.analise import PromptAnalise, ResultadoAnalise
from app.processors.exceptions import LLMError, LLMRateLimitError
from app.processors.openai_client import OpenAIClient
from app.processors.otimizador_prompt import OtimizadorPrompt


class AnalisadorLLM:
    """Analisa currículos contra vagas usando LLM.

    Integra o cliente OpenAI e o otimizador de prompts para realizar
    análises estruturadas de adequação de candidatos a vagas.

    Attributes:
        settings: Configurações da aplicação
        openai_client: Cliente para chamadas à API OpenAI
        otimizador: Otimizador de prompts para reduzir tokens
    """

    def __init__(self, settings: Settings | None = None):
        """Inicializa o analisador LLM.

        Args:
            settings: Configurações da aplicação. Se None, usa get_settings()
        """
        self.settings = settings or get_settings()
        
        # Usa Groq diretamente (API gratuita)
        from app.processors.groq_client import GroqClient
        self.llm_client = GroqClient(settings=self.settings)
        self.otimizador = OtimizadorPrompt(settings=self.settings)
        
        print("✓ AnalisadorLLM: Usando Groq (Llama 3.1 70B)")

    def _construir_prompt(self, texto_vaga: str, texto_curriculo: str) -> PromptAnalise:
        """Constrói o prompt estruturado para análise.

        Args:
            texto_vaga: Descrição da vaga
            texto_curriculo: Texto do currículo

        Returns:
            PromptAnalise com mensagens estruturadas
        """
        # Otimiza textos para caber no limite
        vaga_otimizada, curriculo_otimizado = self.otimizador.otimizar_prompt_analise(
            texto_vaga, texto_curriculo
        )

        sistema = """Você é um especialista em recrutamento e seleção de talentos.
Sua tarefa é analisar currículos e avaliar a adequação de candidatos a vagas.

Você deve fornecer uma análise objetiva, justa e estruturada, considerando:
- Experiência profissional relevante
- Formação acadêmica
- Habilidades técnicas
- Soft skills demonstradas
- Alinhamento com os requisitos da vaga

Seja imparcial e baseie sua análise apenas nas informações fornecidas."""

        usuario = f"""Analise o seguinte currículo em relação à vaga descrita.

VAGA:
{vaga_otimizada}

CURRÍCULO:
{curriculo_otimizado}

Forneça sua análise no seguinte formato JSON:
{{
    "score": <número de 0 a 100>,
    "justificativa": "<explicação detalhada do score>",
    "pontos_fortes": ["<ponto 1>", "<ponto 2>", ...],
    "gaps": ["<gap 1>", "<gap 2>", ...]
}}

IMPORTANTE:
- O score deve ser um número inteiro de 0 a 100
- A justificativa deve explicar claramente o score atribuído
- Liste pelo menos 2 pontos fortes do candidato
- Liste pelo menos 2 gaps ou áreas de melhoria
- Seja específico e objetivo"""

        formato_resposta = "JSON com score, justificativa, pontos_fortes e gaps"

        return PromptAnalise(
            sistema=sistema, usuario=usuario, formato_resposta=formato_resposta
        )

    def _extrair_json_resposta(self, resposta: str) -> dict:
        """Extrai JSON da resposta do LLM.

        O LLM pode retornar o JSON com texto adicional ou formatação.
        Este método tenta extrair apenas o JSON válido.

        Args:
            resposta: Resposta completa do LLM

        Returns:
            Dicionário com os dados extraídos

        Raises:
            LLMError: Se não conseguir extrair JSON válido
        """
        # Tenta encontrar JSON na resposta
        # Procura por padrão {..."score":...}
        match = re.search(r"\{[^{}]*\"score\"[^{}]*\}", resposta, re.DOTALL)

        json_str = match.group(0) if match else resposta.strip()

        try:
            dados = json.loads(json_str)
            return dados
        except json.JSONDecodeError as e:
            raise LLMError(
                f"Não foi possível extrair JSON válido da resposta do LLM: {e}"
            ) from e

    def _validar_resposta(self, dados: dict) -> None:
        """Valida a estrutura da resposta do LLM.

        Args:
            dados: Dicionário com dados da resposta

        Raises:
            LLMError: Se a resposta não tiver a estrutura esperada
        """
        campos_obrigatorios = ["score", "justificativa", "pontos_fortes", "gaps"]

        for campo in campos_obrigatorios:
            if campo not in dados:
                raise LLMError(f"Campo obrigatório ausente na resposta: {campo}")

        # Valida tipos
        if not isinstance(dados["score"], int):
            raise LLMError(f"Score deve ser inteiro, recebido: {type(dados['score'])}")

        if not isinstance(dados["justificativa"], str):
            raise LLMError("Justificativa deve ser string")

        if not isinstance(dados["pontos_fortes"], list):
            raise LLMError("pontos_fortes deve ser lista")

        if not isinstance(dados["gaps"], list):
            raise LLMError("gaps deve ser lista")

        # Valida valores
        if not 0 <= dados["score"] <= 100:
            raise LLMError(f"Score fora do intervalo 0-100: {dados['score']}")

        if not dados["justificativa"].strip():
            raise LLMError("Justificativa não pode estar vazia")

    def analisar(
        self, texto_vaga: str, texto_curriculo: str, curriculo_id: int, vaga_id: int
    ) -> ResultadoAnalise:
        """Analisa um currículo contra uma vaga.

        Args:
            texto_vaga: Descrição completa da vaga
            texto_curriculo: Texto extraído do currículo
            curriculo_id: ID do currículo no banco de dados
            vaga_id: ID da vaga no banco de dados

        Returns:
            ResultadoAnalise com score, justificativa, pontos fortes e gaps

        Raises:
            LLMError: Se houver erro na análise ou resposta inválida
            TokenLimitExceededError: Se textos excederem limite de tokens
        """
        # Constrói prompt otimizado
        prompt = self._construir_prompt(texto_vaga, texto_curriculo)

        # Converte para mensagens OpenAI
        mensagens = prompt.to_messages()

        # Valida limite de tokens
        if not self.otimizador.validar_limite(mensagens):
            tokens_usados = self.otimizador.contar_tokens_mensagens(mensagens)
            raise LLMError(
                f"Prompt excede limite de tokens: {tokens_usados} > {self.settings.openai_max_tokens}"
            )

        # Chama LLM (Groq)
        resposta = self.llm_client.chat_completion(
            mensagens, temperature=0.3  # Temperatura baixa para respostas mais consistentes
        )

        # Extrai e valida JSON
        dados = self._extrair_json_resposta(resposta)
        self._validar_resposta(dados)

        # Conta tokens usados
        tokens_usados = self.otimizador.contar_tokens_mensagens(mensagens)
        tokens_usados += self.otimizador.contar_tokens(resposta)

        # Cria resultado
        return ResultadoAnalise(
            score=dados["score"],
            justificativa=dados["justificativa"],
            pontos_fortes=dados["pontos_fortes"],
            gaps=dados["gaps"],
            curriculo_id=curriculo_id,
            vaga_id=vaga_id,
            data_analise=datetime.now(),
            tokens_usados=tokens_usados,
        )

    async def analisar_async(
        self, texto_vaga: str, texto_curriculo: str, curriculo_id: int, vaga_id: int
    ) -> ResultadoAnalise:
        """Versão assíncrona da análise de currículo.

        Args:
            texto_vaga: Descrição completa da vaga
            texto_curriculo: Texto extraído do currículo
            curriculo_id: ID do currículo no banco de dados
            vaga_id: ID da vaga no banco de dados

        Returns:
            ResultadoAnalise com score, justificativa, pontos fortes e gaps

        Raises:
            LLMError: Se houver erro na análise ou resposta inválida
            TokenLimitExceededError: Se textos excederem limite de tokens
        """
        # Constrói prompt otimizado
        prompt = self._construir_prompt(texto_vaga, texto_curriculo)

        # Converte para mensagens OpenAI
        mensagens = prompt.to_messages()

        # Valida limite de tokens
        if not self.otimizador.validar_limite(mensagens):
            tokens_usados = self.otimizador.contar_tokens_mensagens(mensagens)
            raise LLMError(
                f"Prompt excede limite de tokens: {tokens_usados} > {self.settings.openai_max_tokens}"
            )

        # Chama LLM de forma assíncrona (Groq)
        resposta = await self.llm_client.async_chat_completion(
            mensagens, temperature=0.3
        )

        # Extrai e valida JSON
        dados = self._extrair_json_resposta(resposta)
        self._validar_resposta(dados)

        # Conta tokens usados
        tokens_usados = self.otimizador.contar_tokens_mensagens(mensagens)
        tokens_usados += self.otimizador.contar_tokens(resposta)

        # Cria resultado
        return ResultadoAnalise(
            score=dados["score"],
            justificativa=dados["justificativa"],
            pontos_fortes=dados["pontos_fortes"],
            gaps=dados["gaps"],
            curriculo_id=curriculo_id,
            vaga_id=vaga_id,
            data_analise=datetime.now(),
            tokens_usados=tokens_usados,
        )
