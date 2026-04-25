import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.chatbot_engdados_repository import ChatRepository
from app.services.priority_advisor import PriorityAdvisor

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_isolated_state():
    """
    Garante o isolamento entre testes reinicializando o estado da aplicação.
    Isso evita que dados persistidos em um teste afetem o resultado de outro.
    """
    app.state.repository = ChatRepository()
    app.state.advisor = PriorityAdvisor()
    yield

def test_create_chat_message_success():
    """Valida a criação de uma mensagem (Status 201)."""
    payload = {
        "session_id": "session-test-1",
        "user_message": "Quais são as melhores práticas para ingestão de dados?",
        "bot_response": "O particionamento e o uso de formatos colunares são essenciais."
    }
    response = client.post("/chatbot/", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["session_id"] == "session-test-1"
    assert "user_message" in data

def test_get_chat_history_success():
    """Valida a recuperação do histórico de uma sessão existente (Status 200)."""
    session_id = "session-test-2"
    # Popula o repositório via API
    client.post("/chatbot/", json={
        "session_id": session_id,
        "user_message": "Olá",
        "bot_response": "Oi"
    })
    
    response = client.get(f"/chatbot/{session_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1

def test_get_chat_history_not_found():
    """Valida o erro 404 ao buscar uma sessão inexistente."""
    response = client.get("/chatbot/sessao-fantasma")
    assert response.status_code == 404
    assert "não encontrada" in response.json()["detail"]

def test_analyze_roadmap_success():
    """Valida o processamento da análise técnica (Status 200)."""
    session_id = "session-test-3"
    # Garante que a sessão exista para que o service aceite a análise
    client.post("/chatbot/", json={
        "session_id": session_id,
        "user_message": "Init",
        "bot_response": "Resp"
    })

    roadmap_payload = {
        "target_destination": "BigQuery",
        "data_sources": ["MySQL", "Salesforce"],
        "daily_volume_gb": 150.0,
        "is_real_time": False
    }
    response = client.put(f"/chatbot/{session_id}/analyze", json=roadmap_payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "technical_overview" in data
    assert "complexity" in data

def test_analyze_roadmap_not_found():
    """Valida o erro 404 ao tentar analisar um roadmap de sessão inexistente."""
    roadmap_payload = {"target_destination": "X", "data_sources": [], "daily_volume_gb": 0, "is_real_time": False}
    response = client.put("/chatbot/sessao-inexistente/analyze", json=roadmap_payload)
    assert response.status_code == 404