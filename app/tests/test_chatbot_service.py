import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.chat_service import ChatService
from app.models.chatbot_engdados import InterfaceChat, DiscoveryRoadmap, Summary, ComplexityLevel

@pytest.fixture
def mock_repository():
    """Fixture para mockar o repositório de dados."""
    return MagicMock()

@pytest.fixture
def mock_advisor():
    """Fixture para mockar o PriorityAdvisor (chamadas assíncronas)."""
    return AsyncMock()

@pytest.fixture
def chat_service(mock_repository, mock_advisor):
    """Instância do serviço injetando os mocks."""
    return ChatService(repository=mock_repository, advisor=mock_advisor)

@pytest.mark.asyncio
async def test_create_message_should_call_repository_and_return_entry(chat_service, mock_repository):
    """Garante que a mensagem é enviada ao repositório e retornada corretamente."""
    # Arrange
    chat_entry = InterfaceChat(
        session_id="session-123",
        user_message="Como estruturar um Data Lake?",
        bot_response="Você deve considerar o particionamento..."
    )
    mock_repository.create.return_value = chat_entry

    # Act
    result = await chat_service.create_message(chat_entry)

    # Assert
    mock_repository.create.assert_called_once_with(chat_entry)
    assert result == chat_entry
    assert result.session_id == "session-123"

@pytest.mark.asyncio
async def test_get_history_returns_list_when_session_exists(chat_service, mock_repository):
    """Verifica se o histórico é retornado corretamente para sessões existentes."""
    # Arrange
    session_id = "valid-session"
    expected_history = [
        InterfaceChat(session_id=session_id, user_message="Oi", bot_response="Olá")
    ]
    mock_repository.get_by_session_id.return_value = expected_history

    # Act
    history = await chat_service.get_history(session_id)

    # Assert
    assert history == expected_history
    mock_repository.get_by_session_id.assert_called_with(session_id)

@pytest.mark.asyncio
async def test_get_history_returns_none_when_session_not_found(chat_service, mock_repository):
    """Garante que sessões inexistentes retornem None (conforme contrato do serviço)."""
    # Arrange
    mock_repository.get_by_session_id.return_value = []
    mock_repository.exists.return_value = False # Simula que a sessão não existe

    # Act
    history = await chat_service.get_history("ghost-session")

    # Assert
    assert history is None

@pytest.mark.asyncio
async def test_process_analysis_returns_summary_for_existing_session(chat_service, mock_repository, mock_advisor):
    """Verifica se a análise é acionada apenas se a sessão for válida."""
    # Arrange
    session_id = "active-session"
    roadmap = DiscoveryRoadmap(
        target_destination="S3",
        data_sources=["ERP"],
        daily_volume_gb=10.0,
        is_real_time=False,
        transformation_steps=["Limpeza", "Normalização"] # Adicionado campo obrigatório
    )
    expected_summary = Summary(
        project_title="Análise Técnica",
        technical_overview="Resumo",
        complexity=ComplexityLevel.LOW,
        estimated_tech_stack=["Python"],
        structured_markdown="# MD"
    )
    
    mock_repository.exists.return_value = True # Simula que a sessão existe
    mock_advisor.analyze_project.return_value = expected_summary

    # Act
    result = await chat_service.process_analysis(session_id, roadmap)

    # Assert
    assert result == expected_summary
    mock_advisor.analyze_project.assert_called_once_with(roadmap)

@pytest.mark.asyncio
async def test_process_analysis_returns_none_when_session_missing(chat_service, mock_repository):
    """Garante que a análise falha silenciosamente se a sessão não existir."""
    # Arrange
    mock_repository.get_by_session_id.return_value = []
    mock_repository.exists.return_value = False # Simula que a sessão não existe
    roadmap = DiscoveryRoadmap( # Roadmap válido para passar na validação Pydantic
        target_destination="Lake",
        data_sources=["Logs"],
        daily_volume_gb=1.0,
        is_real_time=False,
        transformation_steps=["Agregação"]
    )

    # Act
    result = await chat_service.process_analysis("invalid-id", roadmap)

    # Assert
    assert result is None