# Documento de Escopo: MVP Chatbot para Estimativa de Projetos de Engenharia de Dados

## 1. Objetivo
Prover uma interface inteligente baseada em LLM para auxiliar engenheiros e arquitetos de dados na fase de descoberta (discovery). O chatbot deve interagir com o usuário para extrair definições técnicas, volumetria e complexidade, gerando um resumo estruturado que servirá de base para a estimativa de esforço e custos.

## 2. Requisitos Funcionais (RF)

- **RF01 - Interface de Chat (API):** O sistema deve expor endpoints via FastAPI para envio de prompts e recepção de respostas processadas por modelos de linguagem (OpenAI/Gemini).
- **RF02 - Roteiro de Descoberta:** O chatbot deve ser instruído (System Prompt) a coletar informações sobre:
  - Fontes de dados (Origem, formato, protocolo).
  - Volumetria (Ingestão diária, histórico total).
  - Transformações (Limpeza, enriquecimento, agregações).
  - Destino (Data Lake, Warehouse, Lakehouse).
- **RF03 - Geração de Resumo Estruturado:** Ao final da interação, o bot deve consolidar os pontos discutidos em um formato técnico (Markdown/JSON) para facilitar a estimativa manual.
- **RF04 - Verificação de Saúde (Health Check):** O sistema deve informar o status operacional e a validade das configurações de integração com provedores de IA.

## 3. Requisitos Não Funcionais (RNF)

- **RNF01 - Latência de Resposta:** O sistema deve lidar com chamadas assíncronas para evitar bloqueios de thread enquanto aguarda o retorno da LLM.
- **RNF02 - Segurança de Credenciais:** Nenhuma chave de API ou segredo de infraestrutura deve estar hardcoded no repositório, utilizando exclusivamente variáveis de ambiente.
- **RNF03 - Arquitetura Limpa:** Separação clara entre a camada de API (FastAPI) e a camada de integração com serviços de IA.
- **RNF04 - Padronização de Saída:** As respostas do chatbot devem seguir um tom técnico, direto e focado em engenharia de dados, evitando redundâncias.

## 4. Fora de Escopo

- **Cálculo Automático de Preços:** O MVP não realizará cálculos financeiros diretos (ex: custo em USD de instâncias Cloud), apenas consolidará os requisitos técnicos.
- **Persistência de Sessão:** Armazenamento de histórico de conversas em banco de dados para consultas futuras.
- **Interface Gráfica (Front-end):** Desenvolvimento de dashboards ou interfaces complexas (limitado a API e CLI neste estágio).
- **Autenticação e Autorização:** Controle de acesso de usuários e gestão de permissões (RBAC).

---
**Status:** Proposto (v0.1)  
**Data:** 21 de Abril de 2024  
**Responsável:** Rogério Morais Rocha