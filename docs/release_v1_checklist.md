# Checklist de Release v1.0.0 - MVP

## ✅ Validação Técnica
- [ ] **Suíte de Testes:** Executar `make test` e garantir 100% de aprovação.
- [ ] **Qualidade de Código:** Executar `make lint` para garantir conformidade com o padrão Black.
- [ ] **Dependências:** Verificar se o `requirements.txt` contém todas as versões necessárias sem conflitos.
- [ ] **Variáveis de Ambiente:** Validar se o `.env.example` está sincronizado com as necessidades do `PriorityAdvisor`.
- [ ] **Health Check:** Rodar a aplicação localmente e validar o endpoint `/health`.
- [ ] **Segurança:** Garantir que o `.env` e pastas de cache (`__pycache__`, `.pytest_cache`) estão no `.gitignore`.

## 📝 Documentação
- [ ] **README.md:** Revisar se as instruções de instalação via `Makefile` estão claras.
- [ ] **Histórico de Prompts:** Garantir que o `prompts-gemini.md` está atualizado com as últimas interações.
- [ ] **Backlog:** Marcar como concluídos os itens da "Release 1: Core" no arquivo `docs/backlog.md`.
- [ ] **Licença:** (Opcional) Adicionar um arquivo LICENSE se o projeto for open-source.

## 🚀 Procedimento de Publicação (Git/GitHub)

1. **Consolidação do Código:**
   ```bash
   git checkout main
   git pull origin main
   ```

2. **Criação da Tag de Versão:**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0 - MVP Functional Core"
   ```

3. **Push de Código e Tags:**
   ```bash
   git push origin main
   git push origin v1.0.0
   ```

4. **GitHub Release:**
   - Ir para a aba "Releases" no repositório.
   - Selecionar a tag `v1.0.0` e gerar as "Release Notes" automáticas.

---

## 💡 Sugestão de Conteúdo para a Release

**Título da Release:** `v1.0.0 - MVP: Core de Descoberta e Análise Técnica`

**Descrição Sugerida:**
```markdown
## O que há de novo? 🚀
Esta é a primeira versão estável do Data Engineering Discovery Chatbot! O foco desta release é fornecer a base funcional para a coleta de requisitos e estimativa técnica.

- **Interactive Discovery:** Fluxo de chat para coleta de fontes, volumes e destinos.
- **PriorityAdvisor:** Motor de análise inteligente com fallback automático para heurística local (custo zero).
- **Robustez:** Suíte completa de testes unitários e de integração com cobertura das regras de negócio.
- **Developer Experience:** Makefile para automação de setup e ambiente configurado via Pydantic v2.
```