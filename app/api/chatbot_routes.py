from fastapi import APIRouter, HTTPException, status, Depends, Request
from typing import List
from app.models.chatbot_engdados import InterfaceChat, DiscoveryRoadmap, Summary
from app.services.chat_service import ChatService
from app.services.priority_advisor import PriorityAdvisor
from prompts.chatbot_engdados_repository import ChatRepository

# Provedores de Dependência Nativos

def get_repository(request: Request) -> ChatRepository:
    """
    Recupera o repositório singleton armazenado no estado da aplicação.
    """
    return request.app.state.repository

def get_advisor(request: Request) -> PriorityAdvisor:
    """
    Recupera o PriorityAdvisor do estado da aplicação.
    """
    return request.app.state.advisor

def get_chat_service(
    repo: ChatRepository = Depends(get_repository),
    advisor: PriorityAdvisor = Depends(get_advisor)
) -> ChatService:
    """
    Constrói o serviço de chat injetando suas dependências necessárias.
    """
    return ChatService(repository=repo, advisor=advisor)

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

@router.post(
    "/",
    response_model=InterfaceChat,
    status_code=status.HTTP_201_CREATED,
    summary="Enviar nova mensagem"
)
async def create_chat_message(chat_entry: InterfaceChat, service: ChatService = Depends(get_chat_service)):
    """
    Registra uma nova interação do usuário na sessão. 
    Utilizado para coletar requisitos durante o discovery antes da análise final.
    """
    return await service.create_message(chat_entry)

@router.get(
    "/{chat_id}",
    response_model=List[InterfaceChat],
    status_code=status.HTTP_200_OK,
    summary="Recuperar histórico do chat"
)
async def get_chat_history(chat_id: str, service: ChatService = Depends(get_chat_service)):
    """
    Retorna a lista de interações de uma sessão específica.
    Lança 404 caso a sessão não exista no repositório.
    """
    history = await service.get_history(chat_id)

    if history is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sessão de chat '{chat_id}' não encontrada."
        )
    
    return history

@router.put(
    "/{chat_id}/analyze",
    response_model=Summary,
    status_code=status.HTTP_200_OK,
    summary="Atualizar roadmap e gerar análise técnica"
)
async def analyze_roadmap(chat_id: str, roadmap: DiscoveryRoadmap, service: ChatService = Depends(get_chat_service)):
    """
    Recebe os dados consolidados do discovery e aciona o PriorityAdvisor.
    Retorna o Sumário técnico ou 404 se a sessão for inválida.
    """
    summary = await service.process_analysis(chat_id, roadmap)

    if summary is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Não foi possível processar a análise. Sessão '{chat_id}' não encontrada."
        )

    return summary