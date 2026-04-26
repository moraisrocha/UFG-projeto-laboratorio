import os
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv

from app.api.chatbot_routes import router as chatbot_router
from app.services.priority_advisor import PriorityAdvisor
from app.models.chatbot_engdados_repository import ChatRepository

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação, inicializando dependências globais.
    """
    # Inicialização (Startup)
    app.state.repository = ChatRepository()
    app.state.advisor = PriorityAdvisor()
    yield
    # Limpeza (Shutdown) - Pode ser adicionada lógica aqui se necessário

app = FastAPI(title="Chatbot de Requisitos Funcionais", lifespan=lifespan)

app.include_router(chatbot_router)

@app.get("/")
async def root():
    """
    Rota raiz para boas-vindas e verificação de configuração básica.
    """
    return {
        "message": "Bem-vindo ao API do Chatbot de Requisitos Funcionais",
        "api_key_status": "Configurada" if os.getenv("OPENAI_API_KEY") else "Ausente"
    }

@app.get("/health")
async def health_check() -> dict[str, str]:
    """
    Endpoint de verificação de saúde que retorna o status e o timestamp UTC atual.
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)