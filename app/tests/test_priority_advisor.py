import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.priority_advisor import PriorityAdvisor
from app.models.chatbot_engdados import DiscoveryRoadmap, ComplexityLevel

@pytest.fixture
def advisor():
    """Fixture que fornece uma instância limpa do PriorityAdvisor."""
    return PriorityAdvisor()

@pytest.mark.asyncio
async def test_heuristic_low_complexity(advisor):
    """Valida se requisitos leves resultam em complexidade baixa."""
    roadmap = DiscoveryRoadmap(
        target_destination="DuckDB",
        data_sources=["CSV Local"],
        daily_volume_gb=5,
        is_real_time=False
    )
    result = advisor._get_local_heuristic(roadmap)
    
    assert result.complexity == ComplexityLevel.LOW
    assert "DuckDB" in result.estimated_tech_stack
    assert "Python" in result.estimated_tech_stack[0]

@pytest.mark.asyncio
async def test_heuristic_medium_complexity(advisor):
    """Valida se volumes moderados resultam em complexidade média."""
    roadmap = DiscoveryRoadmap(
        target_destination="PostgreSQL",
        data_sources=["API Externa", "DB Legado", "S3"],
        daily_volume_gb=100,
        is_real_time=False
    )
    result = advisor._get_local_heuristic(roadmap)
    
    assert result.complexity == ComplexityLevel.MEDIUM
    assert "Airflow" in result.estimated_tech_stack
    assert "dbt" in result.estimated_tech_stack

@pytest.mark.asyncio
async def test_heuristic_high_complexity_by_volume(advisor):
    """Valida se volumes altos disparam complexidade alta."""
    roadmap = DiscoveryRoadmap(
        target_destination="Delta Lake",
        data_sources=["Logs"],
        daily_volume_gb=1000,
        is_real_time=False
    )
    result = advisor._get_local_heuristic(roadmap)
    
    assert result.complexity == ComplexityLevel.HIGH
    assert "Apache Spark" in result.estimated_tech_stack

@pytest.mark.asyncio
async def test_heuristic_high_complexity_by_real_time(advisor):
    """Valida se requisito de tempo real força complexidade alta."""
    roadmap = DiscoveryRoadmap(
        target_destination="Redis",
        data_sources=["Sensors"],
        daily_volume_gb=1,
        is_real_time=True
    )
    result = advisor._get_local_heuristic(roadmap)
    
    assert result.complexity == ComplexityLevel.HIGH
    assert "Apache Kafka" in result.estimated_tech_stack

@pytest.mark.asyncio
async def test_fallback_on_llm_exception(advisor):
    """Garante que a heurística local é usada se o cliente LLM falhar."""
    advisor.client = AsyncMock() # Simula que existe cliente configurado
    
    roadmap = DiscoveryRoadmap(
        target_destination="S3",
        data_sources=["Fonte"],
        daily_volume_gb=10,
        is_real_time=False
    )

    with patch.object(advisor, '_call_llm', side_effect=Exception("OpenAI Offline")):
        result = await advisor.analyze_project(roadmap)
        
        assert result.complexity == ComplexityLevel.LOW
        assert "Heurística Local" in result.structured_markdown

@pytest.mark.asyncio
async def test_fallback_on_timeout(advisor):
    """Valida o comportamento de fallback quando a API excede o timeout."""
    advisor.client = AsyncMock()
    advisor.timeout = 0.1  # Reduz timeout para o teste ser rápido

    async def slow_response(*args):
        await asyncio.sleep(0.5)
        return MagicMock()

    roadmap = DiscoveryRoadmap(
        target_destination="Cloud",
        data_sources=["Source"],
        daily_volume_gb=500,
        is_real_time=False
    )

    with patch.object(advisor, '_call_llm', side_effect=slow_response):
        result = await advisor.analyze_project(roadmap)
        # Como o volume é 500, a heurística deve classificar como MEDIUM ou HIGH
        assert result.complexity in [ComplexityLevel.MEDIUM, ComplexityLevel.HIGH]
        assert "Heurística Local" in result.structured_markdown