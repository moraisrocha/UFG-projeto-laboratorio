import os
import asyncio
import json
from typing import Optional
from openai import AsyncOpenAI
from app.models.chatbot_engdados import DiscoveryRoadmap, Summary, ComplexityLevel

class PriorityAdvisor:
    """
    Serviço responsável por avaliar o roadmap técnico e gerar um resumo consolidado,
    priorizando o uso de LLM com fallback para heurística local.
    """

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = AsyncOpenAI(api_key=self.api_key) if self.api_key else None
        self.timeout = 15.0  # Timeout de segurança para chamadas externas

    async def analyze_project(self, roadmap: DiscoveryRoadmap) -> Summary:
        """
        Orquestra a análise do projeto utilizando LLM ou Heurística Local.
        """
        if self.client:
            try:
                # Tenta processamento via IA com timeout restrito
                return await asyncio.wait_for(self._call_llm(roadmap), timeout=self.timeout)
            except Exception:
                # Em caso de falha (timeout, rede, rate limit), utiliza fallback
                return self._get_local_heuristic(roadmap)
        
        # Caso não haja chave de API, utiliza heurística sem custo
        return self._get_local_heuristic(roadmap)

    def _get_local_heuristic(self, roadmap: DiscoveryRoadmap) -> Summary:
        """
        Calcula complexidade e sugestão técnica baseada em regras de negócio locais.
        """
        sources_count = len(roadmap.data_sources)
        volume = roadmap.daily_volume_gb

        # Lógica de decisão para complexidade
        if volume > 500 or roadmap.is_real_time or sources_count > 5:
            complexity = ComplexityLevel.HIGH
            stack = ["Apache Spark", "Apache Kafka", "Terraform", "Cloud Data Lakehouse"]
        elif volume > 50 or sources_count > 2:
            complexity = ComplexityLevel.MEDIUM
            stack = ["Airflow", "dbt", "PostgreSQL", "Cloud Functions"]
        else:
            complexity = ComplexityLevel.LOW
            stack = ["Python (Pandas/Polars)", "DuckDB", "GitHub Actions"]

        overview = (
            f"Projeto focado em {roadmap.target_destination} com processamento de "
            f"{volume}GB/dia a partir de {sources_count} fontes distintas."
        )

        markdown = (
            f"## Resumo do Projeto (Heurística Local)\n"
            f"- **Complexidade:** {complexity.value}\n"
            f"- **Fontes:** {', '.join(roadmap.data_sources)}\n"
            f"- **Tempo Real:** {'Sim' if roadmap.is_real_time else 'Não'}"
        )

        return Summary(
            project_title=f"Pipeline: {roadmap.target_destination}",
            technical_overview=overview,
            complexity=complexity,
            estimated_tech_stack=stack,
            structured_markdown=markdown
        )

    async def _call_llm(self, roadmap: DiscoveryRoadmap) -> Summary:
        """
        Realiza chamada ao modelo GPT para análise técnica avançada.
        """
        prompt = (
            "Aja como um Arquiteto de Dados Sênior. Analise os seguintes requisitos "
            f"e retorne um JSON estritamente no formato do modelo Summary: {roadmap.model_dump_json()}\n"
            "Considere volumetria, fontes e o destino final para definir a stack."
        )

        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("Resposta vazia da LLM")
            
        data = json.loads(content)
        
        # Garante que o nível de complexidade seja um valor válido do Enum
        if "complexity" in data:
            # Mapeia strings retornadas pela IA para o Enum ComplexityLevel
            for level in ComplexityLevel:
                if level.value.lower() in str(data["complexity"]).lower():
                    data["complexity"] = level
                    break
            if isinstance(data["complexity"], str):
                data["complexity"] = ComplexityLevel.MEDIUM

        return Summary(**data)