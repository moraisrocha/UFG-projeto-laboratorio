import os
from datetime import datetime, timezone
from fastapi import FastAPI
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = FastAPI(title="Chatbot de Requisitos Funcionais")

@app.get("/")
async def root():
    """
    Rota raiz para boas-vindas e verificação de configuração básica.
    """
    return {
        "message": "Bem-vindo ao API do Chatbot de Requisitos Funcionais",
        "api_key_status": "Configurada" if os.getenv("API_KEY") else "Ausente"
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