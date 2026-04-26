# Roteiro de Demonstração Técnica - MVP Chatbot (5 Minutos)

## ⏱️ Minuto 1: Setup e Infraestrutura
**Objetivo:** Mostrar prontidão para execução e integridade da API.
- **Ação:** Iniciar o servidor e validar health check.
- **Comandos:**
```bash
make run
# Em outro terminal:
curl -X GET http://localhost:8000/health
```
- **Fala:** "A API está operando em FastAPI com gerenciamento de ciclo de vida (lifespan) para injeção de dependências como o repositório e o motor de IA."

## ⏱️ Minutos 2-3: Fluxo de Descoberta e Persistência
**Objetivo:** Demonstrar a coleta de requisitos e o gerenciamento de estado.
- **Ação:** Criar uma mensagem de chat e recuperar o histórico.
- **Comandos:**
```bash
# Criar mensagem
curl -X POST http://localhost:8000/chatbot/ \
     -H "Content-Type: application/json" \
     -d '{"session_id": "demo123", "user_message": "Preciso processar 500GB/dia de logs."}'

# Recuperar histórico
curl -X GET http://localhost:8000/chatbot/demo123
```
- **Fala:** "Utilizamos Pydantic v2 para validação rigorosa de contratos. A persistência atual é em memória via padrão Repository, pronta para migração para base documental."

## ⏱️ Minutos 4: Inteligência e Resiliência (Fallback)
**Objetivo:** Mostrar o `PriorityAdvisor` em ação e a lógica de falha segura.
- **Ação:** Acionar análise técnica com volumetria que dispare heurística ou IA.
- **Comandos:**
```bash
curl -X PUT http://localhost:8000/chatbot/demo123/analyze \
     -H "Content-Type: application/json" \
     -d '{
       "target_destination": "BigQuery",
       "data_sources": ["CloudWatch"],
       "daily_volume_gb": 600,
       "is_real_time": true,
       "transformation_steps": ["Deduplicação"]
     }'
```
- **Fala:** "O PriorityAdvisor tenta processar via GPT-3.5. Caso a chave falhe ou ocorra timeout (15s), nossa Heurística Local assume o cálculo de complexidade e sugestão de stack."

## ⏱️ Minuto 5: Qualidade e Encerramento
**Objetivo:** Provar a confiabilidade do código.
- **Ação:** Rodar a suíte de testes.
- **Comando:**
```bash
make test
```
- **Fala:** "Fechamos com 100% de cobertura nos serviços e rotas, garantindo que refatorações futuras sejam seguras."