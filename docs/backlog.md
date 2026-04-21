# Backlog do Produto: MVP Chatbot de Estimativa

## Release 1: Core (Funcionalidade Base)
- [ ] **RF01 - Integração com LLM (Gemini/OpenAI)**
    - **Critério de Aceite:** O sistema deve enviar um prompt técnico e receber uma resposta coerente da IA.
    - **RT01:** Implementar `app/services/ai_service.py` isolando a lógica da SDK do provedor.
- [ ] **RF02 - Endpoint de Chat Assíncrono**
    - **Critério de Aceite:** O endpoint `/chat` deve aceitar mensagens de texto e retornar a resposta da IA sem bloquear a aplicação.
    - **RT02:** Utilizar `async/await` do FastAPI para chamadas de rede à API de IA.
- [ ] **RF03 - Prompt de Sistema (System Instructions)**
    - **Critério de Aceite:** O chatbot deve atuar estritamente como um especialista em engenharia de dados, focando em fontes, volumes e transformações.
    - **RT03:** Criar um gerenciador de templates de prompt em `app/core/prompts.py`.

## Release 2: Qualidade (Robustez e UX)
- [ ] **RT04 - Validação de Schemas e Contratos**
    - **Critério de Aceite:** Entradas inválidas (strings vazias ou formatos incorretos) devem retornar erro 422 estruturado.
    - **RT04:** Implementar modelos Pydantic em `app/schemas/chat.py` para entrada e saída.
- [ ] **RF04 - Tratamento de Erros e Timeouts**
    - **Critério de Aceite:** Se a API de IA falhar ou demorar mais de 30s, o usuário deve receber uma mensagem de erro amigável.
    - **RT05:** Implementar middleware de tratamento de exceções globais e políticas de timeout no cliente HTTP.
- [ ] **RT06 - Cobertura de Testes Automatizados**
    - **Critério de Aceite:** Endpoints de `/health` e `/chat` devem possuir testes de integração com sucesso e falha.
    - **RT06:** Configurar `pytest` e `httpx.AsyncClient` para testes de integração.

## Release 3: Entrega Final (Valor e Saída)
- [ ] **RF05 - Geração de Resumo Estruturado**
    - **Critério de Aceite:** O chatbot deve ser capaz de gerar um bloco Markdown final contendo: Fontes, Volume Estimado e Complexidade.
    - **RT07:** Implementar lógica de "Summarization" no serviço de IA após a coleta de dados básicos.
- [ ] **RF06 - Interface CLI de Alta Fidelidade**
    - **Critério de Aceite:** O usuário deve conseguir interagir com o bot via terminal com cores e tabelas formatadas.
    - **RT08:** Implementar comando `chat` utilizando `Typer` e `Rich` para formatação de saída no terminal.
- [ ] **RT09 - Containerização e Deploy Ready**
    - **Critério de Aceite:** O projeto deve rodar em qualquer ambiente via Docker sem configurações manuais além do `.env`.
    - **RT09:** Criar `Dockerfile` multi-stage otimizado para Python.

---
**Legenda:**
- **RF:** Requisito Funcional (O que o sistema faz).
- **RT:** Requisito Técnico (Como o sistema faz internamente).