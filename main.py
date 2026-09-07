import os
from enum import Enum
from typing import List
from google import genai
from google.genai import types
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
    def __init__(self, model: str = "gemini-3.5-flash", api_key: str | None = None):
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

    def analisar_estruturado(
        self,
        dilema: str,
        perspectiva: PerspectivaEtica = PerspectivaEtica.MULTI_PERSPECTIVA,
        tom: TomResposta = TomResposta.ACADEMICO
    ) -> RelatorioEtico:
        """Retorna a resposta como objeto Python fortemente tipado (JSON Schema garantido)."""
        system_instruction = self._gerar_system_prompt(perspectiva, tom)

        response = self.client.models.generate_content(
            model=self.model,
            contents=f"Dilema ético para análise:\n{dilema}",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=RelatorioEtico,
                temperature=0.3
            )
        )
        
        # Converte o JSON retornado pelo Gemini diretamente para o modelo Pydantic
        return RelatorioEtico.model_validate_json(response.text)

    def analisar_texto_livre(
        self,
        dilema: str,
        perspectiva: PerspectivaEtica = PerspectivaEtica.MULTI_PERSPECTIVA,
        tom: TomResposta = TomResposta.SOCRATICO,
        formato: str = "Markdown estruturado com seções e pontos-chave."
    ) -> str:
        """Retorna texto em formato livre (Markdown, ensaio, diálogo socrático, etc)."""
        system_instruction = self._gerar_system_prompt(perspectiva, tom)

        prompt = f"""Dilema ético:
{dilema}

Instruções de formato de saída:
{formato}
"""
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.6
            )
        )
        return response.text


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
    print("=" * 60)

    relatorio = analisador.analisar_estruturado(
        dilema=dilema,
        perspectiva=PerspectivaEtica.UTILITARISTA,
        tom=TomResposta.PRAGMATICO
    )

    print(f"Resumo: {relatorio.resumo_dilema}\n")
    print(f"Conflito Central: {relatorio.conflito_central}\n")
    print(f"Recomendação: {relatorio.recomendacao_final}\n")
    print("Perguntas para Reflexão:")
    for p in relatorio.perguntas_para_reflexao:
        print(f"  • {p}")

    print("\n" + "=" * 60)
    print("2. RESPOSTA EM TEXTO LIVRE (DEBATE SOCRÁTICO)")
    print("=" * 60)

    texto = analisador.analisar_texto_livre(
        dilema=dilema,
        perspectiva=PerspectivaEtica.DEONTOLOGICA,
        tom=TomResposta.SOCRATICO,
        formato="Diálogo curto em forma de perguntas instigantes."
    )
    print(texto)