# DilemaLLM ⚖️🤖

Analisador ético e filosófico de dilemas morais complexos utilizando modelos **Google Gemini** e estruturas de dados fortemente tipadas com **Pydantic**.

---

## 📌 Funcionalidades

- **Perspectivas Filosóficas:** Utilitarismo, Deontologia Kantiana, Ética das Virtudes, Pragmatismo e Multi-perspectiva.
- **Tons de Resposta:** Acadêmico, Socrático, Pragmático e Empático.
- **Saída Estruturada (JSON / Pydantic):** Resposta rigorosa e validada contendo resumo, análises por corrente (prós e contras), conflito central, recomendação e perguntas reflexivas.
- **Modo Texto Livre:** Geração de diálogos socráticos e ensaios reflexivos.

---

## 🚀 Instalação e Configuração

### 1. Clone o repositório
```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd DilemaLLM
```

### 2. Crie e ative um ambiente virtual (opcional, mas recomendado)
```bash
python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure a chave de API do Gemini
Crie um arquivo `.env` na raiz do projeto com base no arquivo `.env.example`:
```env
GEMINI_API_KEY=sua_chave_aqui
```

> Obtenha sua chave gratuitamente em [Google AI Studio](https://aistudio.google.com/app/apikey).

---

## 💻 Executando o Projeto

```bash
python main.py
```
