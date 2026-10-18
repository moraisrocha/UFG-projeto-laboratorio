persona: como um experiente engenheiro de testes em testes funcionais, testes em API REST e testes integrados

contexto: Construir cenários de testes focados em falhas de autenticação e autorização baseadas em tokens (por exemplo, JWT). Cobrir todos os tipos de falha possíveis relacionadas ao token: assinatura incorreta, expiração (mesmo por poucos segundos), ausência de claims obrigatórias, token emitido para outro público (audience), algoritmo inválido, token manipulado, token revogado, cabeçalho ausente ou mal formado.

exemplo:

1. Token com Assinatura Incorreta

Objetivo: Validar que o sistema rejeita tokens cujo conteúdo foi alterado ou cuja assinatura não corresponde à chave esperada.
• Caso de Teste 1.1: Rejeição por assinatura inválida
	• Pré-condição: Usuário válido e token originalmente emitido; manter chave pública/segredo correto no servidor.
	• Ação: Enviar uma requisição GET autenticada para /api/v1/products/99 usando um JWT válido cujo payload seja idêntico, mas cuja assinatura (parte final) foi alterada ou regenerada com uma chave diferente.
	• Validações esperadas:
		• O código de status HTTP deve ser 401 (Unauthorized).
		• A mensagem de erro deve indicar "invalid signature" ou texto equivalente que não vaze segredos do servidor.

2. Token Expirado por Poucos Segundos

Objetivo: Verificar comportamento do servidor diante de tokens com exp (expiration) muito próximo do tempo atual (por exemplo, expirado há 1-10 segundos).
• Caso de Teste 2.1: Token expirado por alguns segundos
	• Pré-condição: Gerar um token JWT com claim "exp" igual a agora - 5 segundos.
	• Ação: Enviar uma requisição GET para /api/v1/products/99 com esse token no cabeçalho Authorization.
	• Validações esperadas:
		• O código de status HTTP deve ser 401 (Unauthorized).
		• A mensagem de erro deve indicar que o token expirou (por exemplo, "token expired").
		• Testar tolerância de relógio (clock skew) do servidor: se a especificação do servidor admite X segundos de skew, validar comportamento tanto dentro quanto fora da janela.

3. Token sem Claims Obrigatórias

Objetivo: Garantir que tokens que não apresentem claims essenciais (sub, exp, iat, aud quando exigido) sejam rejeitados.
• Caso de Teste 3.1: Token sem claim "sub"
	• Pré-condição: Gerar um JWT sem o claim "sub" (identificador do usuário) mas com exp/iat válidos.
	• Ação: Enviar uma requisição autenticada para /api/v1/products/99.
	• Validações esperadas:
		• O código de status HTTP deve ser 400 (Bad Request) ou 401 (Unauthorized) conforme a API.
		• A resposta deve indicar ausência da claim obrigatória.
• Caso de Teste 3.2: Token sem claim "exp"
	• Pré-condição: Gerar um JWT sem claim "exp".
	• Ação: Requisição autenticada à API.
	• Validações esperadas:
		• Rejeição com 400/401 devido à ausência de exp (ou comportamento aceito se a política permitir tokens sem exp — documentar). 

4. Token Emitido para Outro Público (Audience)

Objetivo: Validar que tokens emitidos para um aud (audience) diferente do esperado sejam rejeitados.
• Caso de Teste 4.1: aud diferente
	• Pré-condição: Gerar um JWT com claim "aud" igual a "other-service" enquanto a API espera "my-api".
	• Ação: Enviar GET /api/v1/products/99 com esse token.
	• Validações esperadas:
		• O código de status HTTP deve ser 401 (Unauthorized).
		• A resposta deve indicar "invalid audience" ou mensagem equivalente.

5. Token com Algoritmo Inválido / "alg" Manipulado

Objetivo: Garantir que tokens com header.alg alterado (por exemplo, "alg":"none" ou troca de algoritmo de RS256 para HS256) sejam rejeitados.
• Caso de Teste 5.1: alg = none
	• Pré-condição: Criar token JWT com header {"alg":"none"} e payload válido.
	• Ação: Enviar requisição autenticada com esse token.
	• Validações esperadas:
		• O servidor deve rejeitar o token com 401.

6. Token Manipulado/Corrompido

Objetivo: Validar comportamento ao receber tokens truncados, com base64 inválido, ou com partes faltando.
• Caso de Teste 6.1: Token truncado
	• Ação: Enviar Authorization: Bearer <token-truncado>
	• Validações esperadas: 400 (Bad Request) ou 401 (Unauthorized) com mensagem de token inválido.

7. Token de Usuário Revogado (logout / revogação por servidor)

Objetivo: Se a aplicação mantém lista de revogação (blacklist) ou versionamento de tokens, garantir que tokens revogados sejam rejeitados.
• Caso de Teste 7.1: Token revogado
	• Pré-condição: Emitir token válido; registrar revogação no servidor (ou simular revogação de sessão).
	• Ação: Enviar requisição autenticada com o token revogado.
	• Validações esperadas: 401 com mensagem de sessão/tokem inválido ou revogado.

8. Cabeçalho de Autenticação Ausente ou Mal Formado

Objetivo: Verificar respostas quando Authorization header não é enviado, ou forma incorreta (p.ex. "Bearer" faltando, ou com prefixo diferente).
• Caso de Teste 8.1: Sem cabeçalho Authorization
	• Ação: Enviar GET /api/v1/products/99 sem Authorization.
	• Validações esperadas: 401 e mensagem indicando que o token não foi fornecido.
• Caso de Teste 8.2: Cabeçalho mal formado
	• Ação: Enviar Authorization: Token abc.def.ghi
	• Validações esperadas: 401 e mensagem de token mal formado.

formato:
1. cenários de teste com saída em JSON estruturado, adequado para automação com REST
2. código de testes em JAVA (focando em JUnit + RestAssured ou similar)
3. explicações em formato markdown

ação:
1. Fornecer a especificação OpenAPI (Swagger) delimitada por ##### contendo ao menos os endpoints que exigem autenticação (por exemplo, GET /api/v1/products/{id}, POST /api/v1/orders) para que os testes cubram os comportamentos de falha nessas rotas.
2. Para cada cenário listado acima, criar cenários de testes inválidos e as variações relevantes (por exemplo, expirado por 5s, por 30s, assinado com chave diferente, aud diferente, sem claim sub/exp/aud).
3. Incluir payloads de exemplo e cabeçalhos (Authorization) com templates para gerar tokens inválidos (ex.: modificar assinatura, alterar "exp" para passado, remover campos). Não incluir chaves privadas reais — apenas instruções e exemplos de criação com bibliotecas de JWT.
4. Produzir os três artefatos finais (mesmo formato que o prompt original):
	- arquivo api-cenarios-falhas.json
	- arquivo api-code-falhas.java
	- arquivo api-explicacao-falhas.md

resposta esperada:
- Este arquivo: prompts/testes-integrados-falhas-possiveis.md (conteúdo que descreve os testes de falha).
- Quando solicitado posteriormente, gerar os arquivos de cenários JSON, código Java e explicações em Markdown usando a OpenAPI fornecida.

observações:
- Descrever claramente as mensagens de erro esperadas, mas sem expor segredos (chaves/algoritmos internos). Use mensagens genéricas padrão quando apropriado.
- Indicar se a API tem tolerância de clock skew e parametrizar os testes para validar limites (ex.: 0s, 5s, 30s).
- Para cada caso, indicar o status HTTP esperado (401, 400, 403, 404 quando aplicável) e o fragmento esperado na mensagem de erro.
- Incluir exemplos de comandos curl e trechos de código (pseudo) em Java para gerar tokens inválidos usando bibliotecas comuns (java-jwt, jjwt) — sem chaves reais.

