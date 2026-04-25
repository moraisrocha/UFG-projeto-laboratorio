from typing import Dict, List, Optional
from app.models.chatbot_engdados import InterfaceChat

class ChatRepository:
    """
    Repositório em memória para persistência volátil de interações.
    Ideal para a fase de MVP e testes de integração.
    """
    def __init__(self) -> None:
        # Armazenamento indexado por session_id para recuperação rápida do histórico
        self._storage: Dict[str, List[InterfaceChat]] = {}

    def create(self, chat_entry: InterfaceChat) -> InterfaceChat:
        """
        Persiste uma nova interação no histórico da sessão correspondente.
        """
        session_id = chat_entry.session_id
        
        if session_id not in self._storage:
            self._storage[session_id] = []
            
        self._storage[session_id].append(chat_entry)
        return chat_entry

    def get_by_session_id(self, session_id: str) -> List[InterfaceChat]:
        """
        Recupera a lista completa de interações de uma sessão específica.
        """
        return self._storage.get(session_id, [])

    def delete_session(self, session_id: str) -> None:
        """Remove todos os dados de uma sessão específica."""
        self._storage.pop(session_id, None)