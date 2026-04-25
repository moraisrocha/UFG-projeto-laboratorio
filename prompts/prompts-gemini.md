# Capitulo 01 - Prompts para Gemini

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

## Prompt 5 - Mensagem de commit
``` text
Contexto: Adicionei diferentes estruturas .
Objetivo: Gerar uma mensagem de commit no padrao Conventional Commits para cada adição.
Resposta: Gerar o comando com uma linha de commit para cada adição.
```
