# Checklist de Release v1.0.1 - Estabilização e Automação

## ✅ Validação Técnica
- [ ] **Suíte de Testes:** Executar `make test` e garantir 100% de aprovação (valida a correção de imports e payloads).
- [ ] **Pydantic v2 Compliance:** Verificar se `min_length` foi utilizado em substituição ao `min_items` em `app/models/chatbot_engdados.py`.
- [ ] **Resolução de Módulos:** Confirmar presença dos arquivos `__init__.py` e `pytest.ini` para evitar `ModuleNotFoundError`.
- [ ] **Gerenciamento de Dependências:** Validar se `pytest-asyncio` está presente no `requirements.txt`.
- [ ] **Injeção de Dependência:** Validar o funcionamento do `lifespan` e `app.state` no `app/main.py`.
- [ ] **Qualidade de Código:** Executar `make lint` para garantir padronização com Black.

## 📝 Documentação
- [ ] **README.md:** Revisar se as seções de "Estrutura de Pastas" e "Automação com Makefile" estão corretas.
- [ ] **Histórico de Prompts:** Garantir que o `prompts/prompts-gemini.md` contém os registros das refatorações e correções de testes.
- [ ] **Exemplo de Ambiente:** Validar se o `.env.example` reflete a chave `OPENAI_API_KEY`.

## 🚀 Procedimento de Publicação (Git/GitHub)

1. **Consolidação das Correções:**
   ```bash
   git add .
   git commit -m "chore: prepare release v1.0.1 with technical fixes and improved DX"
   ```

2. **Criação da Tag de Versão:**
   ```bash
   git tag -a v1.0.1 -m "Release version 1.0.1 - Technical Fixes, Pydantic v2 and Makefile"
   ```

3. **Push de Código e Tags:**
   ```bash
   git push origin main
   git push origin v1.0.1
   ```

4. **GitHub Release:**
   - Acessar a aba "Releases" no GitHub.
   - Criar nova release a partir da tag `v1.0.1`.

---

## 💡 Sugestão de Conteúdo para a Release

**Título da Release:** `v1.0.1 - Estabilização Técnica e Automação`

**Descrição Sugerida:**
- **Fix:** Correção de caminhos de importação absolutos para `ChatRepository`.
- **Refactor:** Migração do ciclo de vida da aplicação para `lifespan` (FastAPI) e uso de `app.state` para singletons.
- **Feat:** Adição de `Makefile` para padronização de comandos (`install`, `run`, `test`).
- **Chore:** Compatibilidade total com Pydantic v2 e configuração de ambiente de testes com `pytest.ini`.
- **Docs:** README atualizado com guia de onboarding técnico e estrutura de diretórios.