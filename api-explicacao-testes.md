# Explicação dos testes de integração da API

## Objetivo

Este conjunto de cenários foi planejado para validar a integração entre clientes e API REST, cobrindo os fluxos principais de criação de usuários e consulta de produtos, além dos casos de erro esperados pela especificação.

## Especificação de referência

A API segue um modelo de contrato Swagger/OpenAPI com os seguintes endpoints principais:

- `POST /api/v1/users`
  - Cria um novo usuário.
  - Espera `201 Created` em caso de sucesso.
  - Espera `400 Bad Request` para dados inválidos ou duplicidade.

- `GET /api/v1/products/{id}`
  - Busca um produto por identificador.
  - Requer autenticação via `Authorization: Bearer <token>`.
  - Espera `200 OK` em sucesso.
  - Espera `401 Unauthorized` se não houver token ou se ele for inválido.
  - Espera `404 Not Found` quando o produto não existir.

## Dados utilizados

Para o cadastro do usuário, foi utilizado o payload definido na instrução:

```json
{
  "email": "rogeriorocha@provedor.br",
  "password": "rogeriomrocha",
  "name": "Rogerio Rocha",
  "phone": "+55 123 456 78 90",
  "address": "Logradouro 48"
}
```

Esse payload é usado como cenário base para validação de criação com sucesso, duplicidade e validações de regra de negócio.

## Cobertura de cenários

### 1. Usuários

Os testes cobrem:

- criação com sucesso;
- bloqueio de e-mail duplicado;
- rejeição de e-mail inválido;
- rejeição de senha fraca;
- rejeição de campos obrigatórios ausentes.

Esses casos validam tanto o caminho feliz quanto as principais falhas de entrada e regras de integridade.

### 2. Produtos

Os testes cobrem:

- busca bem-sucedida com token válido;
- acesso sem autenticação;
- acesso com token inválido;
- produto inexistente;
- parâmetro de rota inválido.

Essa combinação garante que a API respeite autenticação, validação de rota e resposta correta para recursos ausentes.

## Estrutura do JSON de cenários

O arquivo `api-cenarios-testes.json` foi modelado para automação REST, com:

- base URL da API;
- bloco Swagger/OpenAPI em formato delimitado por `#####`;
- dados estáticos de teste;
- lista de cenários com:
  - identificador;
  - tipo (`valid` ou `invalid`);
  - método HTTP;
  - endpoint;
  - pré-condições;
  - payload de entrada;
  - status esperado;
  - validações automáticas.

## Estrutura do código Java

O arquivo `api-code-testes.java` foi implementado em Java usando `JUnit 5` e `RestAssured`, sendo adequado para execução em pipelines de CI/CD ou em testes de integração automatizados.

Principais elementos:

- `@BeforeAll` para configuração da base URI;
- `@Test` para cada cenário;
- `given().when().then()` para executar as requisições;
- verificações com `statusCode`, `body(...)` e `containsString(...)`.

## Boas práticas aplicadas

- Separação clara entre cenário válido e inválido.
- Uso de payloads realistas para o domínio da aplicação.
- Verificações para campos sensíveis como senha não retornada na criação do usuário.
- Cobertura de falhas de autenticação e de dados inválidos.
- Estrutura pronta para expansão com novos endpoints.

## Conclusão

A suíte produzida atende ao objetivo de validar a especificação e todas as respostas possíveis da API, respeitando o padrão descrito no arquivo de instrução e mantendo uma organização adequada para automação e documentação.
