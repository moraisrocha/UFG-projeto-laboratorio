# Data Engineering Discovery Chatbot (MVP)

Este projeto é uma micro-API desenvolvida com FastAPI para auxiliar engenheiros e arquitetos de dados na fase de descoberta de requisitos. O sistema utiliza Inteligência Artificial (OpenAI GPT) para analisar roadmaps técnicos, volumetria e complexidade, sugerindo stacks tecnológicas apropriadas.

## 🚀 Funcionalidades

- **Discovery Interativo:** Registro de mensagens e interações para coleta de requisitos de dados.
- **Análise de Prioridade (AI):** Avaliação automática de complexidade e sugestão de stack técnica.
- **Falha Segura (Fallback):** Sistema de heurística local que assume o processamento caso a chave da API não exista ou o serviço de LLM esteja indisponível.
- **Arquitetura Limpa:** Separação clara entre camadas de API, Serviços, Modelos e Repositórios.

## 🏗️ Arquitetura

A aplicação segue o padrão de camadas para garantir testabilidade e manutenção:

- **API (FastAPI):** Define os endpoints e gerencia a injeção de dependência via `app.state`.
- **Services:** Contém a lógica de negócio (`ChatService`) e o motor de decisão técnica (`PriorityAdvisor`).
- **Models:** Define as estruturas de dados usando Pydantic v2.
- **Repository:** Gerencia a persistência (atualmente em memória para o MVP).

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.11+
- **Framework Web:** FastAPI
- **Modelos de Linguagem:** OpenAI GPT-3.5 Turbo (via biblioteca `openai`)
- **Validação de Dados:** Pydantic v2
- **Servidor ASGI:** Uvicorn
- **Testes:** Pytest

## 📥 Instalação e Configuração

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd LABORATORIO-PROJETO
   ```

2. **Crie e ative o ambiente virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` na raiz do projeto:
   ```env
   OPENAI_API_KEY=sua_chave_aqui  # Opcional: Se ausente, usará a heurística local
   ```

## ⚙️ Execução

Para iniciar o servidor de desenvolvimento:

```bash
python3 -m app.main
```
A API estará disponível em `http://localhost:8000`. Você pode acessar a documentação interativa (Swagger UI) em `http://localhost:8000/docs`.

## 🧪 Testes

A suíte de testes cobre a lógica de serviços, heurísticas de prioridade e endpoints da API.

```bash
pytest app/tests/
```

## 🤖 Uso da IA e Sistema de Prioridade

O componente `PriorityAdvisor` orquestra a inteligência da aplicação:

1. **Caminho Principal (LLM):** Se `OPENAI_API_KEY` estiver configurada, a API envia o roadmap para o GPT-3.5, que retorna uma análise técnica detalhada em formato JSON.
2. **Timeout & Fallback:** Se a chamada à IA demorar mais de 15 segundos ou falhar, o sistema aciona automaticamente a **Heurística Local**.
3. **Heurística Local (Custo Zero):** Uma lógica baseada em regras de negócio avalia o volume (GB/dia) e a quantidade de fontes para classificar a complexidade em *BAIXA*, *MÉDIA* ou *ALTA*.

## ⚠️ Limitações do MVP

- **Persistência Volátil:** Os dados são armazenados em memória. Se o servidor for reiniciado, o histórico das sessões será perdido.
- **Provedores de IA:** Atualmente otimizado para OpenAI (integração com Gemini mapeada no backlog).
- **Autenticação:** Não há controle de acesso de usuários nesta fase.

## 📈 Próximos Passos

- [ ] **Persistência em Banco de Dados:** Migrar do repositório em memória para MongoDB ou PostgreSQL.
- [ ] **Containerização:** Criar `Dockerfile` e `docker-compose.yml` para facilitar o deploy.
- [ ] **Suporte a Múltiplos Provedores:** Adicionar suporte ao Google Gemini via `google-generativeai`.
- [ ] **Interface CLI:** Desenvolver uma ferramenta de linha de comando usando `Typer` e `Rich` para interações rápidas.

---
**Projeto desenvolvido para o Laboratório de Projeto - Especialização UFG**
**Responsável:** Rogério Morais Rocha