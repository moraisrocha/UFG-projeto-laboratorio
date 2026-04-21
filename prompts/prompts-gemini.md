# Capitulo 01 - Prompts para Gemini

## Prompt 1 - .gitignore

Contexto: Estou iniciando uma chatbot de perguntas e respostas Python em um repositorio de produto.
Objetivo: Gere um arquivo .gitignore para Python, ambiente virtual, cache de testes e configuracoes 
locais do editor.
Estilo: Organize por secoes com comentarios.
Resposta: Forneca apenas o conteudo do arquivo .gitignore. 

## Prompt 2 - README inicial

Contexto: MVP de chatbot para perguntas e respostas em Python com retorno dos requisitos funcionais 
assistida por IA.
Objetivo: Escrever um README inicial com objetivo, stack, como rodar localmente e roadmap de releases.
Estilo: Markdown simples, direto e profissional.
Resposta: Forneca o README completo

## Prompt 3 - Endpoint de healthcheck
Contexto: Projeto em Python 3.11 com FastAPI.
Objetivo: Criar app/main-py com uma instancia FastAPI e endpoint GET /health retornando status ok e timestamp.
Estilo: Tipagem e codigo limpo.
Resposta: Forneca apenas o codigo de app/main-py.

## Prompt 4 - Revisao critica
Analise o codigo gerado para app/main.py e responda:
1) Quais riscos tecnicos existem?
2) O que pode quebrar em producao?
3) Quais testes minimos devo criar agora?
4) Resposta curta em checklist.

### Prompt 4.1 - Resultado revisao critica
Texto : realize as correcoes nos arquivos main.py e READEME

## Prompt 5 - Mensagem de commit
Contexto: Adicionei estrutura inicial, README, .gitignore e endpoint /health.
Objetivo: Gerar uma mensagem de commit no padrao Conventional Commits.
Resposta: Apenas uma linha de commit.

### Prompt 5.1 - Realizar o commmit
Texto : realize o commit com a mensagem gerada feat: setup initial project structure with health check endpoint and documentation

*o gemini nao tem acesso direto para fazer o commit por este motivo informou o codigo*

<git add .>
<git commit -m "feat: setup initial project structure with health check endpoint and documentation">
