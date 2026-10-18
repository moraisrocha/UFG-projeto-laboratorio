# Testes de integração para falhas de autenticação JWT

## Visão geral

Este documento descreve cenários de integração para validar a robustez da autenticação via JWT em APIs REST. O foco principal é rejeitar corretamente tokens em condições de falha, sem expor segredos, sem permitir bypass e sem aceitar claims incompletas ou inconsistentes.

## Objetivo

Garantir que a API responda com segurança aos seguintes casos:

- token com assinatura incorreta
- token expirado em poucos segundos
- token sem claims obrigatórias
- token emitido para outro público (audience)
- token com algoritmo inválido
- token truncado/corrompido
- token revogado
- cabeçalho de autorização ausente
- cabeçalho de autorização mal formatado

## Critérios gerais de aceite

- Qualquer token inválido deve resultar em resposta HTTP de 401 Unauthorized, ou 400 Bad Request quando a API modela falha de payload/headers de forma explícita.
- respostas devem ser consistentes e não revelar detalhes internos de implementação.
- todos os testes devem validar `Authorization: Bearer <token>` quando aplicável.
- claims consideradas obrigatórias devem ser explicitadas pela política da aplicação (ex.: `sub`, `exp`, `iat`, `aud`).

## Casos de falha testados

### 1. Assinatura incorreta

Quando a assinatura do JWT é alterada, a API deve rejeitá-lo imediatamente.

Exemplo de comportamento esperado:

- status: `401 Unauthorized`
- corpo: mensagem contendo `invalid signature`, `signature`, ou equivalente.

### 2. Expiração em poucos segundos

Mesmo que o token tenha sido emitido recentemente, se `exp` já foi ultrapassado, o servidor deve rejeitá-lo.

Exemplos:

- `exp = now - 5s`
- `exp = now - 1s`
- `exp = now - 30s`

Comportamento esperado:

- status: `401 Unauthorized`
- corpo: `token expired`, `expired`, ou equivalente.

### 3. Claims obrigatórias ausentes

Claims como `sub` e `exp` são fundamentais para a segurança da autenticação. Tokens sem elas devem ser rejeitados.

Exemplos:

- ausência de `sub`
- ausência de `exp`
- ausência de `aud` quando o sistema exige audience

### 4. Audience incompatível

Se a API espera um público específico, um token emitido para outro audiência deve ser recusado.

Exemplo:

- API espera `aud=my-api`
- token foi emitido com `aud=other-service`

Comportamento esperado:

- status: `401 Unauthorized`
- corpo: `invalid audience` ou frase equivalente.

### 5. Algoritmo inválido

A API deve impedir uso de `alg=none` ou qualquer alteração de algoritmo que comprometa a verificação da assinatura.

### 6. Token truncado ou corrompido

Tokens sem estrutura JWT válida, com partes faltantes ou dados inválidos, devem ser rejeitados.

### 7. Token revogado

Se a aplicação mantém revogação de tokens, o servidor deve rejeitar um token previamente invalidado.

### 8. Cabeçalho ausente ou mal formatado

- ausência do header `Authorization`
- uso de prefixo inválido
- valor do cabeçalho vazio ou incompleto

Todos esses casos devem resultar em erro explícito e sem exceção de autenticação.

## Boas práticas de implementação

- preferir validação de assinatura antes de qualquer leitura de claims
- validar `exp`, `iat`, `nbf`, `aud`, `iss` quando aplicável
- tratar `clock skew` de forma documentada
- prevenir respostas que vazem detalhes internos da infraestrutura
- padronizar erros em corpo JSON, por exemplo:

```json
{
  "error": "unauthorized",
  "message": "Token expired"
}
```

## Recomendações para automação

Os testes devem ser parametrizados e executados em diferentes combinações:

- `exp = now + 300s`
- `exp = now - 5s`
- `exp = now - 30s`
- `aud = my-api`
- `aud = other-service`
- `sub` ausente
- `exp` ausente
- `alg = none`
- `Authorization` sem prefixo `Bearer`

## Conclusão

A validação de falhas de token é essencial para proteger a API contra bypass de autenticação, uso indevido de JWT e abuso de claims. A presença de testes automatizados para esses cenários reduz riscos de produção e garante comportamento previsível e seguro.

