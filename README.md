# Data Engineering Discovery Chatbot (MVP)

Este projeto é uma micro-API desenvolvida com FastAPI para auxiliar engenheiros e arquitetos de dados na fase de descoberta de requisitos. O sistema utiliza Inteligência Artificial (OpenAI GPT) para analisar roadmaps técnicos, volumetria e complexidade, sugerindo stacks tecnológicas apropriadas.

## 🚀 Funcionalidades

- **Discovery Interativo:** Registro de mensagens e interações para coleta de requisitos de dados.
- **Análise de Prioridade (AI):** Avaliação automática de complexidade e sugestão de stack técnica.
- **Falha Segura (Fallback):** Sistema de heurística local que assume o processamento caso a chave da API não exista ou o serviço de LLM esteja indisponível.
- **Arquitetura Limpa:** Separação clara entre camadas de API, Serviços, Modelos e Repositórios.

## 📋 Pré-requisitos

- Python 3.11 ou superior
- Make (opcional, para automação)
- Git

## 🏗️ Arquitetura

A aplicação segue o padrão de camadas para garantir testabilidade e manutenção:

- **API (FastAPI):** Define os endpoints e gerencia a injeção de dependência via `app.state`.
- **Services:** Contém a lógica de negócio (`ChatService`) e o motor de decisão técnica (`PriorityAdvisor`).
- **Models:** Define as estruturas de dados usando Pydantic v2.
- **Repository:** Gerencia a persistência (atualmente em memória para o MVP).

### Estrutura de Pastas
```text
.
├── app/
│   ├── api/          # Rotas e Injeção de Dependência
│   ├── models/       # Modelos Pydantic e Enums
│   ├── services/     # Lógica de Negócio e PriorityAdvisor
│   └── tests/        # Suíte de testes (Unitários e Integração)
├── docs/             # Documentação de escopo e arquitetura
├── prompts/          # Histórico de engenharia de prompts
├── Makefile          # Automação de tarefas
└── main.py           # Ponto de entrada da aplicação
```

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.11+
- **Framework Web:** FastAPI
- **Modelos de Linguagem:** OpenAI GPT-3.5 Turbo (via biblioteca `openai`)
- **Validação de Dados:** Pydantic v2
- **Servidor ASGI:** Uvicorn
- **Testes:** Pytest

## 📥 Instalação e Configuração

**Via Makefile (Recomendado):**
```bash
make install
cp .env.example .env
```

**Manualmente:**

1. **Clone e entre no diretório:** `git clone <url> && cd LABORATORIO-PROJETO`
2. **Venv:** `python3 -m venv .venv && source .venv/bin/activate`
3. **Deps:** `pip install -r requirements.txt`
4. **Env:** `cp .env.example .env` (e preencha sua chave OpenAI)

## ⚙️ Execução

Para iniciar o servidor de desenvolvimento:

```bash
make run
```
A API estará disponível em `http://localhost:8000`. Você pode acessar a documentação interativa (Swagger UI) em `http://localhost:8000/docs`.

## 🛠️ Automação com Makefile

Para simplificar o fluxo de desenvolvimento, o projeto inclui um `Makefile` com comandos pré-configurados:

| Comando | Descrição |
| :--- | :--- |
| `make install` | Instala as dependências listadas no arquivo `requirements.txt`. |
| `make run` | Inicia o servidor de desenvolvimento FastAPI através do módulo `app.main`. |
| `make test` | Executa a suíte completa de testes unitários e de integração utilizando o `pytest`. |
| `make lint` | Realiza a formatação automática do código seguindo os padrões do `black`. |
| `make clean` | Remove arquivos temporários e caches de execução (`__pycache__`, `.pytest_cache`). |
| `make help` | Exibe a lista de comandos disponíveis e suas descrições. |

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