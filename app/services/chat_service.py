from typing import List, Optional
from app.models.chatbot_engdados import InterfaceChat, DiscoveryRoadmap, Summary
from app.services.priority_advisor import PriorityAdvisor
from prompts.chatbot_engdados_repository import ChatRepository

class ChatService:
    """
    Orquestrador que integra a persistência de mensagens (Repository) 
    com a lógica de análise técnica (PriorityAdvisor).
    """

    def __init__(self, repository: ChatRepository, advisor: PriorityAdvisor):
        self.repository = repository
        self.advisor = advisor

    async def create_message(self, chat_entry: InterfaceChat) -> InterfaceChat:
        """
        Persiste uma nova interação no histórico da sessão correspondente.
        """
        return self.repository.create(chat_entry)

    async def get_history(self, session_id: str) -> Optional[List[InterfaceChat]]:
        """
        Recupera o histórico de mensagens. Retorna None se a sessão não existir.
        """
        history = self.repository.get_by_session_id(session_id)
        if not history:
            return None
        return history

    async def process_analysis(self, session_id: str, roadmap: DiscoveryRoadmap) -> Optional[Summary]:
        """
        Executa a análise técnica e retorna o sumário. 
        Valida a existência da sessão no repositório antes de processar.
        """
        # Verifica se a sessão existe (requisito para atualização via PUT)
        existing_history = self.repository.get_by_session_id(session_id)
        if not existing_history:
            return None

        # Aciona o PriorityAdvisor para análise (LLM com fallback local)
        summary = await self.advisor.analyze_project(roadmap)
        
        # Opcional: Aqui poderíamos persistir o sumário no repositório como 
        # a última mensagem do sistema para a sessão.
        
        return summary