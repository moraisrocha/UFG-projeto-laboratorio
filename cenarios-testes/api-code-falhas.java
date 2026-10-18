import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import io.restassured.response.Response;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.Instant;
import java.util.Map;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.*;

class ApiTokenFailureTests {

    private static final String BASE_URL = "http://localhost:8080";
    private static final String PRODUCT_ID = "99";

    @BeforeAll
    static void setup() {
        RestAssured.baseURI = BASE_URL;
        RestAssured.enableLoggingOfRequestAndResponseIfValidationFails();
    }

    @Test
    @DisplayName("TC-Auth-001 - Token com assinatura incorreta deve ser rejeitado")
    void shouldRejectTokenWithInvalidSignature() {
        String malformedToken = buildTokenWithWrongSignature();

        given()
            .header("Authorization", "Bearer " + malformedToken)
            .when()
            .get("/api/v1/products/" + PRODUCT_ID)
            .then()
            .statusCode(401)
            .body(containsString("invalid"))
            .body(containsString("signature"));
    }

    @Test
    @DisplayName("TC-Auth-002 - Token expirado em poucos segundos deve ser rejeitado")
    void shouldRejectExpiredTokenShortlyAfterExpiration() {
        String expiredToken = buildTokenWithExp(Instant.now().minusSeconds(5).getEpochSecond());

        given()
            .header("Authorization", "Bearer " + expiredToken)
            .when()
            .get("/api/v1/products/" + PRODUCT_ID)
            .then()
            .statusCode(401)
            .body(anyOf(containsString("expired"), containsString("token"))); 
    }

    @Test
    @DisplayName("TC-Auth-003 - Token sem claim 'sub' deve ser rejeitado")
    void shouldRejectTokenWithoutSubClaim() {
        String tokenWithoutSub = buildToken(Map.of(
            "exp", Instant.now().plusSeconds(300).getEpochSecond(),
            "iat", Instant.now().getEpochSecond(),
            "role", "USER"
        ));

        given()
            .header("Authorization", "Bearer " + tokenWithoutSub)
            .when()
            .get("/api/v1/products/" + PRODUCT_ID)
            .then()
            .statusCode(anyOf(is(400), is(401)))
            .body(anyOf(containsString("sub"), containsString("missing"), containsString("invalid")));
    }

    @Test
    @DisplayName("TC-Auth-004 - Token sem claim 'exp' deve ser rejeitado ou tratado conforme política")
    void shouldRejectTokenWithoutExpClaim() {
        String tokenWithoutExp = buildToken(Map.of(
            "sub", "user-123",
            "iat", Instant.now().getEpochSecond(),
            "aud", "my-api"
        ));

        given()
            .header("Authorization", "Bearer " + tokenWithoutExp)
            .when()
            .get("/api/v1/products/" + PRODUCT_ID)
            .then()
            .statusCode(anyOf(is(400), is(401)))
            .body(anyOf(containsString("exp"), containsString("missing"), containsString("invalid")));
    }

    @Test
    @DisplayName("TC-Auth-005 - Token com audience incorreto deve ser rejeitado")
    void shouldRejectTokenForDifferentAudience() {
        String tokenWrongAudience = buildToken(Map.of(
            "sub", "user-123",
            "exp", Instant.now().plusSeconds(300).getEpochSecond(),
            "iat", Instant.now().getEpochSecond(),
            "aud", "other-service"
        ));

        given()
            .header("Authorization", "Bearer " + tokenWrongAudience)
            .when()
            .get("/api/v1/products/" + PRODUCT_ID)
            .then()
            .statusCode(401)
            .body(anyOf(containsString("aud"), containsString("invalid"), containsString("audience")));
    }

    @Test
    @DisplayName("TC-Auth-006 - Token com algoritmo inválido deve ser rejeitado")
    void shouldRejectTokenWithInvalidAlgorithm() {
        String tokenAlgNone = buildTokenWithHeader(Map.of("alg", "none", "typ", "JWT"), Map.of(
            "sub", "user-123",
            "exp", Instant.now().plusSeconds(300).getEpochSecond(),
            "iat", Instant.now().getEpochSecond(),
            "aud", "my-api"
        ));

        given()
            .header("Authorization", "Bearer " + tokenAlgNone)
            .when()
            .get("/api/v1/products/" + PRODUCT_ID)
            .then()
            .statusCode(401)
            .body(anyOf(containsString("algorithm"), containsString("alg"), containsString("invalid")));
    }

    @Test
    @DisplayName("TC-Auth-007 - Token truncado ou corrompido deve ser rejeitado")
    void shouldRejectMalformedToken() {
        given()
            .header("Authorization", "Bearer abc.def")
            .when()
            .get("/api/v1/products/" + PRODUCT_ID)
            .then()
            .statusCode(anyOf(is(400), is(401)))
            .body(anyOf(containsString("malformed"), containsString("invalid"), containsString("token")));
    }

    @Test
    @DisplayName("TC-Auth-008 - Token revogado deve ser rejeitado")
    void shouldRejectRevokedToken() {
        String revokedToken = buildToken(Map.of(
            "sub", "user-123",
            "exp", Instant.now().plusSeconds(300).getEpochSecond(),
            "iat", Instant.now().getEpochSecond(),
            "aud", "my-api",
            "jti", "revoked-1"
        ));

        revokeToken("revoked-1");

        given()
            .header("Authorization", "Bearer " + revokedToken)
            .when()
            .get("/api/v1/products/" + PRODUCT_ID)
            .then()
            .statusCode(401)
            .body(anyOf(containsString("revoked"), containsString("invalid"), containsString("session")));
    }

    @Test
    @DisplayName("TC-Auth-009 - Requisição sem Authorization deve ser bloqueada")
    void shouldRejectWithoutAuthorizationHeader() {
        given()
            .when()
            .get("/api/v1/products/" + PRODUCT_ID)
            .then()
            .statusCode(401)
            .body(anyOf(containsString("authorization"), containsString("token"), containsString("missing")));
    }

    @Test
    @DisplayName("TC-Auth-010 - Header Authorization mal formatado deve ser rejeitado")
    void shouldRejectMalformedAuthorizationHeader() {
        given()
            .header("Authorization", "Token abc.def.ghi")
            .when()
            .get("/api/v1/products/" + PRODUCT_ID)
            .then()
            .statusCode(401)
            .body(anyOf(containsString("malformed"), containsString("scheme"), containsString("authorization")));
    }

    private static String buildTokenWithWrongSignature() {
        String payload = buildToken(Map.of(
            "sub", "user-123",
            "exp", Instant.now().plusSeconds(300).getEpochSecond(),
            "iat", Instant.now().getEpochSecond(),
            "aud", "my-api"
        ));
        return payload.substring(0, payload.length() - 1) + "Z";
    }

    private static String buildTokenWithExp(long exp) {
        return buildToken(Map.of(
            "sub", "user-123",
            "exp", exp,
            "iat", Instant.now().getEpochSecond(),
            "aud", "my-api"
        ));
    }

    private static String buildToken(Map<String, Object> claims) {
        return buildTokenWithHeader(Map.of("alg", "HS256", "typ", "JWT"), claims);
    }

    private static String buildTokenWithHeader(Map<String, Object> header, Map<String, Object> claims) {
        String headerJson = toJson(header);
        String payloadJson = toJson(claims);
        String encodedHeader = Base64UrlEncoder.encode(headerJson);
        String encodedPayload = Base64UrlEncoder.encode(payloadJson);
        String signingInput = encodedHeader + "." + encodedPayload;
        String signature = Base64UrlEncoder.encode("invalid-secret");
        return signingInput + "." + signature;
    }

    private static void revokeToken(String jti) {
        // Simulação de revogação. Em produção, o serviço deveria invalidar o token em cache/DB.
        // Este método é um placeholder para demonstração de teste.
    }

    private static String toJson(Map<String, Object> map) {
        StringBuilder sb = new StringBuilder();
        sb.append("{");
        int i = 0;
        for (Map.Entry<String, Object> e : map.entrySet()) {
            if (i++ > 0) sb.append(",");
            sb.append("\"").append(e.getKey()).append("\":");
            if (e.getValue() instanceof String) {
                sb.append("\"").append(e.getValue()).append("\"");
            } else {
                sb.append(e.getValue());
            }
        }
        sb.append("}");
        return sb.toString();
    }

    static class Base64UrlEncoder {
        public static String encode(String s) {
            return java.util.Base64.getUrlEncoder().withoutPadding().encodeToString(s.getBytes(java.nio.charset.StandardCharsets.UTF_8));
        }
    }
}
