persona: como um experiente engenheiro de testes em testes funcionais, testes em API REST e testes integrados 

contexto: Realizar a construção de testes de integração, com foco em testes de API e comunicação entre componentes. Seguir exatamente o padrão e a estrutura descritos nos exemplos abaixo (com cenários de sucesso e de erro). Considerar o cenário de integração do projeto conforme descrito no arquivo README.md.

exemplo:

1. Endpoint de Criação (POST /users)

Objetivo: Validar a criação de um novo usuário garantindo que o e-mail seja exclusivo no sistema.
• Caso de Teste 1.1: Criação com sucesso
	• Pré-condição: Banco de dados ativo e sem o e-mail "joao.silva@email.com" cadastrado.
	• Ação: Enviar uma requisição POST para /api/v1/users contendo nome, e-mail válido e senha forte no corpo da mensagem.
	• Validações esperadas:
		• O código de status HTTP deve ser 201 (Created).
		• O corpo da resposta deve conter um ID gerado pelo sistema.
		• Os dados retornados (nome e e-mail) devem bater com o que foi enviado.
		• Por segurança, o campo de senha não deve ser retornado na resposta.
• Caso de Teste 1.2: Bloqueio de e-mail duplicado
	• Pré-condição: O e-mail "joao.silva@email.com" já deve existir previamente cadastrado na base de dados.
	• Ação: Enviar uma requisição POST para /api/v1/users tentando cadastrar um novo usuário com o mesmo e-mail.
	• Validações esperadas:
		• O código de status HTTP deve ser 400 (Bad Request).
		• O corpo da resposta deve trazer uma mensagem clara informando que o e-mail já está em uso.

2. Endpoint de Busca (GET /products/:id)

Objetivo: Validar a busca de um produto específico exigindo autenticação do usuário.
• Caso de Teste 2.1: Busca realizada com sucesso
	• Pré-condição: Deve existir um produto com ID 99 registrado no catálogo do sistema.
	• Ação: Enviar uma requisição GET para /api/v1/products/99 incluindo um token de autenticação válido no cabeçalho (Header "Authorization").
	• Validações esperadas:
		• O código de status HTTP deve ser 200 (OK).
		• O corpo da resposta deve conter os campos estruturados de ID, nome e preço do produto correspondente.
• Caso de Teste 2.2: Tentativa sem autenticação
	• Pré-condição: Nenhuma.
	• Ação: Enviar uma requisição GET para /api/v1/products/99 sem preencher o cabeçalho de autenticação.
	• Validações esperadas:
		• O código de status HTTP deve ser 401 (Unauthorized).
		• A mensagem de erro deve alertar que o token não foi fornecido.
• Caso de Teste 2.3: Produto não localizado
	• Pré-condição: Garantir que o ID 999999 não esteja cadastrado no catálogo.
	• Ação: Enviar uma requisição GET para /api/v1/products/999999 com o cabeçalho de autenticação válido.
	• Validações esperadas:
		• O código de status HTTP deve ser 404 (Not Found).
		• A resposta deve indicar que o produto não foi encontrado.

ação: 
1. cenários de testes válidos usando a documentação OpenAPI (Swagger) delimitada por ##### para prover informação sobre a especificação da aplicação.
2. Os testes deverão ser criados para cobrir a especificação e todas as respostas possíveis.  
3. Utilise os seguintes dados para registrar o usuário: {"email": "rogeriorocha@provedor.br", "password": "rogeriomrocha",
"name"
: "Rogerio Rocha"
, "phone"
:"+55 123 456 78 90"
"address": "Logradouro 48"}
4. cenários de testes inválidos

formato: saída em JSON estruturado, adequado para automação com REST

