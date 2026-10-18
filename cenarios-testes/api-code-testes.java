import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static io.restassured.RestAssured.*;
import static org.hamcrest.Matchers.*;

class ApiIntegrationTests {

    private static final String BASE_URL = "http://localhost:8080/api/v1";
    private static final String AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.example.token.valid";

    @BeforeAll
    static void setup() {
        RestAssured.baseURI = BASE_URL;
        RestAssured.enableLoggingOfRequestAndResponseIfValidationFails();
    }

    @Test
    @DisplayName("TC-USER-01 - Criação com sucesso")
    void criarUsuarioComSucesso() {
        String payload = "{"
                + "\"email\": \"rogeriorocha@provedor.br\","
                + "\"password\": \"rogeriomrocha\","
                + "\"name\": \"Rogerio Rocha\","
                + "\"phone\": \"+55 123 456 78 90\","
                + "\"address\": \"Logradouro 48\""
                + "}";

        given()
            .contentType(ContentType.JSON)
            .body(payload)
        .when()
            .post("/users")
        .then()
            .statusCode(201)
            .body("id", notNullValue())
            .body("email", equalTo("rogeriorocha@provedor.br"))
            .body("name", equalTo("Rogerio Rocha"))
            .body("password", nullValue());
    }

    @Test
    @DisplayName("TC-USER-02 - Bloqueio por e-mail duplicado")
    void bloquearEmailDuplicado() {
        String payload = "{"
                + "\"email\": \"rogeriorocha@provedor.br\","
                + "\"password\": \"rogeriomrocha\","
                + "\"name\": \"Rogerio Rocha\","
                + "\"phone\": \"+55 123 456 78 90\","
                + "\"address\": \"Logradouro 48\""
                + "}";

        Response response = given()
            .contentType(ContentType.JSON)
            .body(payload)
        .when()
            .post("/users");

        response.then()
            .statusCode(400)
            .body("message", containsString("e-mail"))
            .body("message", containsString("em uso"));
    }

    @Test
    @DisplayName("TC-USER-03 - E-mail inválido")
    void rejeitarEmailInvalido() {
        String payload = "{"
                + "\"email\": \"email-invalido\","
                + "\"password\": \"rogeriomrocha\","
                + "\"name\": \"Rogerio Rocha\","
                + "\"phone\": \"+55 123 456 78 90\","
                + "\"address\": \"Logradouro 48\""
                + "}";

        given()
            .contentType(ContentType.JSON)
            .body(payload)
        .when()
            .post("/users")
        .then()
            .statusCode(400)
            .body("message", containsString("email"));
    }

    @Test
    @DisplayName("TC-USER-04 - Senha fraca")
    void rejeitarSenhaFraca() {
        String payload = "{"
                + "\"email\": \"rogerio.senha.fraca@provedor.br\","
                + "\"password\": \"123\","
                + "\"name\": \"Rogerio Rocha\","
                + "\"phone\": \"+55 123 456 78 90\","
                + "\"address\": \"Logradouro 48\""
                + "}";

        given()
            .contentType(ContentType.JSON)
            .body(payload)
        .when()
            .post("/users")
        .then()
            .statusCode(400)
            .body("message", anyOf(containsString("senha"), containsString("password")))
            .body("errors.password", notNullValue());
    }

    @Test
    @DisplayName("TC-USER-05 - Campos obrigatórios ausentes")
    void rejeitarCamposObrigatoriosAusentes() {
        String payload = "{"
                + "\"email\": \"rogerio@provedor.br\","
                + "\"password\": \"rogeriomrocha\""
                + "}";

        given()
            .contentType(ContentType.JSON)
            .body(payload)
        .when()
            .post("/users")
        .then()
            .statusCode(400)
            .body("message", containsString("validation"))
            .body("errors", notNullValue());
    }

    @Test
    @DisplayName("TC-PRODUCT-01 - Busca de produto com sucesso")
    void buscarProdutoComSucesso() {
        given()
            .header("Authorization", "Bearer " + AUTH_TOKEN)
            .accept(ContentType.JSON)
        .when()
            .get("/products/99")
        .then()
            .statusCode(200)
            .body("id", equalTo(99))
            .body("nome", notNullValue())
            .body("preco", notNullValue());
    }

    @Test
    @DisplayName("TC-PRODUCT-02 - Busca sem autenticação")
    void buscarProdutoSemAutenticacao() {
        given()
            .accept(ContentType.JSON)
        .when()
            .get("/products/99")
        .then()
            .statusCode(401)
            .body("message", anyOf(containsString("token"), containsString("unauthorized")));
    }

    @Test
    @DisplayName("TC-PRODUCT-03 - Token inválido")
    void buscarProdutoComTokenInvalido() {
        given()
            .header("Authorization", "Bearer token.invalido")
            .accept(ContentType.JSON)
        .when()
            .get("/products/99")
        .then()
            .statusCode(401)
            .body("message", anyOf(containsString("token"), containsString("invalid"), containsString("assinado")));
    }

    @Test
    @DisplayName("TC-PRODUCT-04 - Produto não localizado")
    void buscarProdutoNaoExistente() {
        given()
            .header("Authorization", "Bearer " + AUTH_TOKEN)
            .accept(ContentType.JSON)
        .when()
            .get("/products/999999")
        .then()
            .statusCode(404)
            .body("message", containsString("produto"))
            .body("message", containsString("não encontrado"));
    }

    @Test
    @DisplayName("TC-PRODUCT-05 - Parâmetro de rota inválido")
    void buscarProdutoComIdInvalido() {
        given()
            .header("Authorization", "Bearer " + AUTH_TOKEN)
            .accept(ContentType.JSON)
        .when()
            .get("/products/abc")
        .then()
            .statusCode(400)
            .body("message", anyOf(containsString("invalid"), containsString("valor"), containsString("id")));
    }
}
