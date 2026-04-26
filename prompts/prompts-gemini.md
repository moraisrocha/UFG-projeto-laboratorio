# Índice
1. [Capitulo 1 - Prompts para Gemini](#capitulo-1---prompts-para-gemini)
2. [Capitulo 2 - Prompts para Gemini/Copilot](#capítulo-2---prompts-para-gemini-copilot)
3. [Capitulo 3 - Prompts para Gemini/Copilot](#capítulo-3---prompts-para-gemini-copilot)
4. [Capitulo 4 - Prompts para Gemini/Copilot](#capítulo-4---prompts-para-gemini-copilot)
5. [Capitulo 5 - Prompts para Gemini/Copilot](#capítulo-5---prompts-para-gemini-copilot)
6. [Prompt Commit](#prompt-commit)

# Capitulo 1 - Prompts para Gemini

## Prompt 1 - .gitignore
``` text
Contexto: Estou iniciando uma chatbot de perguntas e respostas Python em um repositorio de produto.
Objetivo: Gere um arquivo .gitignore para Python, ambiente virtual, cache de testes e configuracoes 
locais do editor.
Estilo: Organize por secoes com comentarios.
Resposta: Forneca apenas o conteudo do arquivo .gitignore. 
```
## Prompt 2 - README inicial
``` text
Contexto: MVP de chatbot para perguntas e respostas em Python com retorno dos requisitos funcionais 
assistida por IA.
Objetivo: Escrever um README inicial com objetivo, stack, como rodar localmente e roadmap de releases.
Estilo: Markdown simples, direto e profissional.
Resposta: Forneca o README completo
```
## Prompt 3 - Endpoint de healthcheck
``` text
Contexto: Projeto em Python 3.11 com FastAPI.
Objetivo: Criar app/main-py com uma instancia FastAPI e endpoint GET /health retornando status ok e timestamp.
Estilo: Tipagem e codigo limpo.
Resposta: Forneca apenas o codigo de app/main-py.
```
## Prompt 4 - Revisao critica
``` text
Analise o codigo gerado para app/main.py e responda:
1) Quais riscos tecnicos existem?
2) O que pode quebrar em producao?
3) Quais testes minimos devo criar agora?
4) Resposta curta em checklist.
```
### Prompt 4.1 - Resultado revisao critica
``` text
Texto : realize as correcoes nos arquivos main.py e READEME
```
## Prompt 5 - Mensagem de commit
``` text
Contexto: Adicionei estrutura inicial, README, .gitignore e endpoint /health.
Objetivo: Gerar uma mensagem de commit no padrao Conventional Commits.
Resposta: Apenas uma linha de commit.
```
### Prompt 5.1 - Realizar o commmit
``` text
Texto : realize o commit com a mensagem gerada feat: setup initial project structure with health check endpoint and documentation
```
**o gemini nao tem acesso direto para fazer o commit por este motivo informou o codigo**
``` text
git add . && git commit -m "feat: setup initial project structure with health check endpoint and documentation"
```
# Capitulo 2 - Prompts para Gemini/Copilot

## Prompt 1 - Escopo MVP
``` text
Contexto: MVP de um chatbot de perguntas e respostas para elaborar a estimativa de um projeto de engenharia de dados.
Objetivo: Gerar documento de escopo com objetivo, requisitos funcionais, nao funcionais e fora de escopo.
Estilo: Linguagem tecnica, direta, em Markdown.
Resposta: Forneca o conteudo completo de docs/escopo-mvp.md
```
## Prompt 2 - Backlog por releases
``` text
Contexto: O produto sera entregue em 3 releases: core, qualidade e entrega final.
Objetivo: Criar backlog minimo com IDs RF/RT e criterios de aceite.
Estilo: Checklist Markdown.
Resposta: Conteudo de docs/backlog.md.
```
## Prompt 3 - Arquitetura Mermaid
``` text
Contexto: FastAPI com camadas API, Service, Repository e componente PriorityAdvisor.
Objetivo: Gerar diagrama Mermaid de componentes e fluxo de dados.
Estilo: Simples, legivel e versionavel.
Resposta: Apenas bloco Mermaid e criar o arquivo denominado arquitetura-componentes.mmd no diretorio docs.
```
## Prompt 4 - Conventional Commits
``` text
Contexto: Adicionei docs/escopo-mvp-md, docs/arquitetura-componentes.mmd e docs/backlog.md.
Objetivo: Sugerir 3 mensagens de commit no padrao Conventional Commits.
Resposta: Crie 1 linha de commit diferente para cada adicao e informe o comando para realizar o commit.
```
# Capitulo 3 - Prompts para Gemini/Copilot

## Prompt 1 - Modelo Pydantic

``` text
Contexto: Chatbot de perguntas e respostas para extrair definições técnicas, volumetria e complexidade, gerando um resumo estruturado que servirá de base para a estimativa de esforço e custos.
Objetivo: Gerar modelos InterfaceChat, DiscoveryRoadmap e Summary com tipagem e validacoes.
Estilo: Pydantic v2, codigo limpo e docstrings curtas.
Resposta: Gerar apenas codigo no arquivo denominado chatbot-engdados.py no diretorio app/models/.
```

## Prompt 2 - Repositorio Inicial
``` text
Contexto: Preciso de persistencia inicial enxuta para viabilizar a primeira release.
Objetivo: Criar ChatRepository em memoria com create e InterfaceChat.
Estilo: Python tipado, sem dependencias externas.
Resposta: Codigo completo de app/repositories/chatbot-engdados_repository-py.
```

## Prompt 3 - PriorityAdvisor com fallback
``` text
Contexto: Quero rodar sem custo de API quando nao houver chave.
Objetivo: Implementar PriorityAdvisor com heuristica local e chamada opcional a LLM quando  OPENAI_API_KEY existir.
Estilo: Falha segura, timeout e fallback obrigatorio.
Resposta: Gerar apenas codigo no arquivo denominado priority_advisor.py no diretorio app/services/
```

## Prompt 4 - Rotas CRUD
``` text
Contexto: ChatBot com ChatService pronto.
Objetivo: Criar rotas GET/PUT para perguntas com status HTTP corretos e tratamento de 404.
Estilo: Router separado em app/api/chatbot_routes.py•
Resposta: Gerar apenas codigo no arquivo denominado chatbot_routes.py no diretorio app/api/
```
**a gemini sugeriu algumas opcoes que confirmei, sendo elas**
``` text
1.  Create the ChatService class to integrate ChatRepository and PriorityAdvisor logic."**
2.  Implement a POST route in chatbot_routes.py to allow creating a new chat session message before analysis.
``` 
# Capitulo 4 - Prompts para Gemini/Copilot

## Prompt 1 - Testes do service
```text
Contexto: Tenho ChatService com criacao de mensagens e persistencia em memoria.
Objetivo: Gerar suite Pytest cobrindo a criacao de perguntas e respostas.
Estilo: Testes claros, nomes descritivos e fixtures simples.
Resposta: Codigo completo de tests/test_chatbot_service.py
```

## Prompt 2 - Testes do PriorityAdvisor
```text
Contexto: PriorityAdvisor possui heuristica local e fallback quando chamada externa falha.
Objetivo: Gerar testes para os tres niveis de prioridade e para fallback.
Estilo: Usar monkeypatch quando necessario.
Resposta: Gerar apenas o codigo no arquivo denominado test_priority_advisor.py no diretorio app/tests/ 
```

## Prompt 3 - Testes de API
```text
Contexto: Chatbot FastAPI
Objetivo: Criar testes de rota com TestClient para status 201, 200 e 404.
Estilo: Isolar dependencia de repositorio para evitar estado global entre testes.
Resposta: Gerar apenas o codigo no arquivo denominado test_task_routes.py no diretorio app/tests/
```

## Prompt 4 - Refatoracao DRY/SRP
```text
Analise os arquivos app/services/chat_service.py e app/models/chatbot_engdados_repository.py
Objetivo: Sugerir refatoracao com foco em DRY e SRP sem mudar comportamento externo.
Resposta: 1) lista de mudancas propostas 2) patch sugerido por arquivo.
```

## Prompt 5 - README final tecnico
```text
Contexto: MVP de micro-API de tarefas com prioridade assistida por IA.
Objetivo: Gerar README completo com instalacao, execucao, testes, arquitetura, uso da IA,limitacoes e proximos passos.
Estilo: Markdown profissional e objetivo.
Resposta: README inteiro
```

## Prompt 6 - Revisao final de qualidade
```text
Com base no codigo e nos testes atuais, gere um checklist com:
- Riscos tecnicos restantes
- Gaps de cobertura de teste
- Melhorias prioritarias para a proxima release
Resposta em bullets curtos.
```

# Capitulo 5 - Prompts para Gemini/Copilot

**antes de dar sequencia, solicitaremos a gemini para visualizarmos o chatbot funcionando**

# Prompt - 1 Pedido para visualizar funcionamento
```text
Contexto: Mostrar o funcionamento do chatbot
Objetivo: Demonstrar com alguns casos as perguntas e respostas sendo realizadas por uma pessoa
Resposta: Descreva passo a passo das ações necessárias para demonstrar os casos e também descreva o resultado dos casos
```

# Prompt Commit
```text
Contexto: Realizar commit em camadas separadas
Objetivo: Realizar o commit no padrao conventional separado por camadas das alteracoes em diff, com os devidos comentarios refletindo as ultimas alteracoes. Incluir o arquivo de prompts-gemini.md no commit informando que novos prompts foram incluidos ou alterados
Resposta: Criar um único comando para aplicar os commits separados por camadas
```