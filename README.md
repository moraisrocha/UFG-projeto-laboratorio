# Chatbot de Requisitos Funcionais (MVP)

Este projeto é um MVP de um chatbot inteligente desenvolvido em Python, focado em responder perguntas e auxiliar na definição de requisitos funcionais de software utilizando Inteligência Artificial.

## 🎯 Objetivo

Automatizar e qualificar o processo de levantamento de requisitos, permitindo que analistas e desenvolvedores interajam com uma IA para validar fluxos, identificar lacunas e gerar documentação funcional preliminar de forma ágil.

## 🛠 Stack Tecnológica

- **Linguagem:** Python 3.10+
- **Ambiente Virtual:** `venv`
- **IA/LLM:** OpenAI API (ou Gemini API)
- **Gerenciamento de Dependências:** `pip`
- **Controle de Versão:** Git

## 🚀 Como Rodar Localmente

Siga os passos abaixo para configurar o ambiente em sua máquina:

1. **Clonar o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd <nome-do-diretorio>
   ```

2. **Configurar o ambiente virtual:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # No Windows: .venv\Scripts\activate
   ```

3. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variáveis de ambiente:**
   Crie um arquivo `.env` na raiz do projeto e adicione sua chave de API:
   ```env
   API_KEY=seu_token_aqui
   ```

5. **Executar a aplicação:**
   ```bash
   uvicorn app.main:app --reload
   ```

## 🗺️ Roadmap de Releases

- **v0.1 (MVP):** API base com FastAPI, integração básica com LLM (Gemini/OpenAI) e endpoint de saúde.
- **v0.2:** Suporte para exportação de requisitos em formato Markdown e PDF.
- **v0.3:** Interface Web (Streamlit ou Flask) e persistência de histórico de conversas.
- **v1.0:** Integração direta com ferramentas de gestão (Jira/Azure DevOps).