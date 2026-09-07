import os
import sys
import time
import textwrap
import warnings
import logging

# Configuração de encoding UTF-8 para o terminal Windows e silenciamento de warnings
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

warnings.filterwarnings("ignore")
logging.getLogger("google.genai").setLevel(logging.ERROR)

from enum import Enum
from typing import List
from google import genai
from google.genai import types
from google.genai.errors import ServerError, ClientError
from pydantic import BaseModel, Field



def carregar_env():
    """Carrega variáveis do arquivo .env automaticamente sem depender de bibliotecas externas."""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip("'\""))

carregar_env()


# ==========================================
# 1. ESTILOS E PERSPECTIVAS FILOSÓFICAS
# ==========================================

class PerspectivaEtica(str, Enum):
    UTILITARISTA = "Utilitarismo (maximizar bem-estar coletivo e reduzir danos)"
    DEONTOLOGICA = "Deontologia Kantiana (agir por princípios morais universais inegociáveis)"
    ETICA_VIRTUDES = "Ética das Virtudes (caráter moral, prudência, justiça e coragem)"
    PRAGMATICA = "Pragmatismo ético (consequências práticas e viabilidade contextual)"
    MULTI_PERSPECTIVA = "Multi-perspectiva (confronto equilibrado entre as principais correntes)"

class TomResposta(str, Enum):
    ACADEMICO = "Rigoroso, neutro, conceitual e formal"
    SOCRATICO = "Questionador, provocativo, expondo contradições com perguntas reflexivas"
    PRAGMATICO = "Direto ao ponto, orientado à tomada de decisão prática"
    EMPATICO = "Sensível ao impacto humano e aos sentimentos envolvidos"


# ==========================================
# 2. SCHEMA ESTRUTURADO (PYDANTIC)
# ==========================================

class AnalisePerspectiva(BaseModel):
    corrente: str = Field(description="Nome da corrente ética analisada")
    argumento_favor: str = Field(description="Argumento a favor sob esta ótica")
    argumento_contra: str = Field(description="Argumento contrário sob esta ótica")

class RelatorioEtico(BaseModel):
    resumo_dilema: str = Field(description="Síntese do cerne ético do problema")
    analises: List[AnalisePerspectiva] = Field(description="Análise por perspectiva ética")
    conflito_central: str = Field(description="Tensão moral fundamental no dilema")
    recomendacao_final: str = Field(description="Recomendação ou conclusão ética ponderada")
    perguntas_para_reflexao: List[str] = Field(description="Perguntas críticas para reflexão")


# ==========================================
# 3. ANALISADOR COM GOOGLE GEMINI
# ==========================================

class AnalisadorEticoGemini:
    MODELOS_DISPONIVEIS = ["gemini-3.7-flash", "gemini-3.5-flash", "gemini-3.8-flash"]

    def __init__(self, model: str = "gemini-3.7-flash", api_key: str | None = None):
        key = api_key or os.getenv("GEMINI_API_KEY")
        if key:
            self.client = genai.Client(api_key=key)
        else:
            self.client = genai.Client()
        self.model = model

    def _gerar_system_prompt(self, perspectiva: PerspectivaEtica, tom: TomResposta) -> str:
        return f"""Você é um especialista em filosofia moral e ética aplicada.
Sua missão é dissecar e analisar dilemas éticos complexos.

Diretrizes:
- Perspectiva Filosófica Principal: {perspectiva.value}
- Tom da Linguagem: {tom.value}
- Não dê respostas superficiais; aponte os trade-offs reais e conflitos de valores fundamentais.
"""

    def _chamar_com_resiliencia(self, callback_geracao):
        """Tenta executar a requisição e, em caso de erro 503 ou 429, realiza retentativas e fallback de modelos."""
        modelos_para_tentar = [self.model] + [m for m in self.MODELOS_DISPONIVEIS if m != self.model]
        ultimo_erro = None

        for modelo in modelos_para_tentar:
            for tentativa in range(3):
                try:
                    return callback_geracao(modelo)
                except (ServerError, ClientError) as e:
                    ultimo_erro = e
                    msg_erro = str(e)
                    
                    # Erro 503 (sobrecarga) ou 429 (limite de requisições por minuto no tier gratuito)
                    if "503" in msg_erro or "429" in msg_erro or getattr(e, 'code', None) in (429, 503):
                        tempo_espera = (tentativa + 1) * 3
                        tipo_erro = "limite temporário (429)" if ("429" in msg_erro or getattr(e, 'code', None) == 429) else "alta demanda (503)"
                        print(f"[AVISO] Modelo {modelo} com {tipo_erro}. Nova tentativa em {tempo_espera}s...")
                        time.sleep(tempo_espera)
                        continue
                    raise e
        raise ultimo_erro

    def analisar_estruturado(
        self,
        dilema: str,
        perspectiva: PerspectivaEtica = PerspectivaEtica.MULTI_PERSPECTIVA,
        tom: TomResposta = TomResposta.ACADEMICO
    ) -> RelatorioEtico:
        """Retorna a resposta como objeto Python fortemente tipado (JSON Schema garantido)."""
        system_instruction = self._gerar_system_prompt(perspectiva, tom)

        def _executar(modelo):
            response = self.client.models.generate_content(
                model=modelo,
                contents=f"Dilema ético para análise:\n{dilema}",
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=RelatorioEtico,
                    temperature=0.3
                )
            )
            return RelatorioEtico.model_validate_json(response.text)

        return self._chamar_com_resiliencia(_executar)

    def analisar_texto_livre(
        self,
        dilema: str,
        perspectiva: PerspectivaEtica = PerspectivaEtica.MULTI_PERSPECTIVA,
        tom: TomResposta = TomResposta.SOCRATICO,
        formato: str = "Markdown estruturado com seções e pontos-chave."
    ) -> str:
        """Retorna texto em formato livre (Markdown, ensaio, diálogo socrático, etc)."""
        system_instruction = self._gerar_system_prompt(perspectiva, tom)

        def _executar(modelo):
            prompt = f"Dilema ético:\n{dilema}\n\nInstruções de formato de saída:\n{formato}"
            response = self.client.models.generate_content(
                model=modelo,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.6
                )
            )
            return response.text

        return self._chamar_com_resiliencia(_executar)


def formatar_paragrafo(texto: str, largura: int = 80, prefixo: str = "", indent_subsequente: str = "") -> str:
    """Formata o texto em parágrafos respeitando uma largura máxima de linha."""
    linhas = texto.strip().split("\n")
    resultado = []
    for linha in linhas:
        if linha.strip():
            resultado.append(
                textwrap.fill(
                    linha,
                    width=largura,
                    initial_indent=prefixo,
                    subsequent_indent=indent_subsequente if indent_subsequente else prefixo
                )
            )
        else:
            resultado.append("")
    return "\n".join(resultado)


# ==========================================
# 4. TESTE PRÁTICO
# ==========================================

if __name__ == "__main__":
    analisador = AnalisadorEticoGemini(model="gemini-3.5-flash")

    dilema = (
        "Um carro autônomo enfrenta uma falha crítica de freios em alta velocidade. "
        "À sua frente há uma faixa de pedestres com uma família de 4 pessoas. "
        "A única alternativa é desviar abruptamente contra um poste, o que certamente "
        "matará o passageiro único do veículo."
    )

    print("=" * 60)
    print("1. RESPOSTA ESTRUTURADA (JSON / PYDANTIC)")
    print("=" * 60 + "\n")

    relatorio = analisador.analisar_estruturado(
        dilema=dilema,
        perspectiva=PerspectivaEtica.UTILITARISTA,
        tom=TomResposta.PRAGMATICO
    )

    print(formatar_paragrafo(f"Resumo: {relatorio.resumo_dilema}", largura=80))
    print()
    print(formatar_paragrafo(f"Conflito Central: {relatorio.conflito_central}", largura=80))
    print()
    print(formatar_paragrafo(f"Recomendação: {relatorio.recomendacao_final}", largura=80))
    print()
    print("Perguntas para Reflexão:")
    for p in relatorio.perguntas_para_reflexao:
        print(formatar_paragrafo(f"• {p}", largura=80, prefixo="  ", indent_subsequente="    "))

    print("\n" + "=" * 60)
    print("2. RESPOSTA EM TEXTO LIVRE (DEBATE SOCRÁTICO)")
    print("=" * 60 + "\n")

    texto = analisador.analisar_texto_livre(
        dilema=dilema,
        perspectiva=PerspectivaEtica.DEONTOLOGICA,
        tom=TomResposta.SOCRATICO,
        formato="Diálogo curto em forma de perguntas instigantes."
    )
    print(formatar_paragrafo(texto, largura=80))
    print()