from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, ConfigDict

class ComplexityLevel(str, Enum):
    LOW = "Baixa"
    MEDIUM = "Média"
    HIGH = "Alta"

class InterfaceChat(BaseModel):
    """Representa uma interação individual na interface de chat."""
    model_config = ConfigDict(from_attributes=True)

    session_id: str = Field(..., description="Identificador único da sessão de chat")
    user_message: str = Field(..., min_length=1, description="Mensagem enviada pelo usuário")
    context_metadata: Optional[Dict] = Field(default_factory=dict, description="Metadados de contexto da conversa")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class DiscoveryRoadmap(BaseModel):
    """Mapeia os requisitos técnicos extraídos durante o discovery."""
    data_sources: List[str] = Field(
        ..., 
        min_items=1, 
        description="Lista de fontes de dados (ex: APIs, Bancos SQL, S3)"
    )
    daily_volume_gb: float = Field(
        ..., 
        gt=0, 
        description="Volume de dados estimado para processamento diário em GB"
    )
    transformation_steps: List[str] = Field(
        ..., 
        description="Lista de transformações necessárias (ex: limpeza, join, agregação)"
    )
    target_destination: str = Field(
        ..., 
        description="Destino final dos dados (ex: BigQuery, Data Lakehouse)"
    )
    is_real_time: bool = Field(
        default=False, 
        description="Indica se o pipeline exige processamento em tempo real"
    )

class Summary(BaseModel):
    """Estrutura consolidada para subsidiar a estimativa de esforço."""
    project_title: str = Field(..., description="Título sugerido para o projeto")
    technical_overview: str = Field(..., description="Resumo descritivo da arquitetura proposta")
    complexity: ComplexityLevel = Field(..., description="Nível de complexidade calculado")
    estimated_tech_stack: List[str] = Field(..., description="Ferramentas recomendadas (ex: Spark, Airflow)")
    structured_markdown: str = Field(..., description="Documentação formatada para o escopo final")
    generated_at: datetime = Field(default_factory=datetime.utcnow)