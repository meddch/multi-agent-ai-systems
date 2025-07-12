#!/usr/bin/env python3
"""
Academic Research Assistant - Level 4 Multi-Agent System
Simple local development version
"""

import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.tools.arxiv import ArxivTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools
from agno.storage.sqlite import SqliteStorage
# Simplified imports - using tools instead of knowledge base for demo
# from agno.knowledge.arxiv import ArxivKnowledge
# from agno.knowledge.pdf import PdfKnowledge
# from agno.vectordb.lancedb import LanceDb

# Load environment variables
load_dotenv()

def create_research_assistant_team():
    """Create the research assistant team with 6 specialized agents"""
    
    # Create storage for team-level use only
    storage = SqliteStorage(table_name="research_sessions", db_file="research_assistant.db")
    
    # Paper Discovery Specialist
    paper_discoverer = Agent(
        name="Paper Discovery Specialist",
        role="Comprehensive research paper discovery across multiple academic sources",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[
            ArxivTools(),
            DuckDuckGoTools(cache_results=True),
            ReasoningTools(add_instructions=True)
        ],
        instructions=[
            "You are a research librarian with expertise in academic paper discovery.",
            "Search across ArXiv and web sources for relevant research papers.",
            "Prioritize high-impact journals and recent publications.",
            "Identify seminal papers and review articles in the field.",
            "Provide detailed paper metadata including citations and relevance scores."
        ],
        show_tool_calls=True,
        markdown=True
    )
    
    # Paper Analysis Expert
    paper_analyzer = Agent(
        name="Paper Analysis Expert",
        role="In-depth analysis of individual research papers",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[ReasoningTools(add_instructions=True)],
        instructions=[
            "You are an expert at analyzing academic papers for methodology, contributions, and quality.",
            "Evaluate research design, novelty, and significance of findings.",
            "Assess statistical methods, sample sizes, and validity of conclusions.",
            "Identify key contributions, limitations, and areas for future work.",
            "Provide structured analysis with quality scoring."
        ],
        show_tool_calls=True,
        markdown=True
    )
    
    # Bias Detection Specialist
    bias_detector = Agent(
        name="Bias Detection Specialist",
        role="Identification of bias and methodological issues in research",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[ReasoningTools(add_instructions=True)],
        instructions=[
            "You are an expert in research methodology and bias detection.",
            "Identify potential sources of bias: selection, confirmation, publication, funding.",
            "Evaluate methodological rigor and experimental design.",
            "Assess sample representativeness and statistical validity.",
            "Provide bias risk scores and mitigation recommendations."
        ],
        show_tool_calls=True,
        markdown=True
    )
    
    # Citation Network Analyst
    citation_analyst = Agent(
        name="Citation Network Analyst",
        role="Analysis of citation patterns, research impact, and collaboration networks",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[ReasoningTools(add_instructions=True)],
        instructions=[
            "You are an expert in scientometrics and citation analysis.",
            "Analyze citation patterns, research impact, and collaboration networks.",
            "Identify highly influential papers and researchers in the field.",
            "Track research trends and emerging topics.",
            "Provide insights on research community dynamics and knowledge flow."
        ],
        show_tool_calls=True,
        markdown=True
    )
    
    # Literature Synthesis Expert
    literature_synthesizer = Agent(
        name="Literature Synthesis Expert",
        role="Synthesis of research findings into comprehensive literature reviews",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[ReasoningTools(add_instructions=True)],
        instructions=[
            "You are an expert at synthesizing research literature into coherent narratives.",
            "Identify common themes, contradictions, and knowledge gaps.",
            "Track the evolution of research topics over time.",
            "Provide comprehensive literature reviews with clear structure.",
            "Suggest future research directions and priorities."
        ],
        show_tool_calls=True,
        markdown=True
    )
    
    # Research Process Coordinator
    research_coordinator = Agent(
        name="Research Process Coordinator",
        role="Orchestration of research activities and quality assurance",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[ReasoningTools(add_instructions=True)],
        instructions=[
            "You are a research director ensuring comprehensive and high-quality analysis.",
            "Coordinate between different research specialists.",
            "Ensure all aspects of literature review are covered systematically.",
            "Maintain academic standards and provide quality control.",
            "Synthesize findings into actionable research insights."
        ],
        show_tool_calls=True,
        markdown=True
    )
    
    # Create coordinated team
    team = Team(
        name="Academic Research Team",
        mode="coordinate",
        members=[paper_discoverer, paper_analyzer, bias_detector, citation_analyst, literature_synthesizer, research_coordinator],
        instructions=[
            "Work together systematically to conduct comprehensive literature reviews.",
            "Build upon each other's findings to create thorough research analysis.",
            "Maintain high academic standards and methodological rigor.",
            "Identify research gaps and provide actionable insights.",
            "Deliver publication-quality literature reviews."
        ],
        storage=storage,
        show_tool_calls=True,
        markdown=True,
        debug_mode=True
    )
    
    return team

def conduct_literature_review(research_topic, max_papers=15):
    """Conduct a comprehensive literature review"""
    
    team = create_research_assistant_team()
    
    query = f"""
    Conduct a comprehensive literature review on: {research_topic}
    
    Please provide:
    1. Systematic paper discovery and selection (up to {max_papers} papers)
    2. Individual paper analysis with quality assessment
    3. Bias detection and methodological evaluation
    4. Citation network analysis and research impact assessment
    5. Literature synthesis with thematic analysis
    6. Research gaps identification and future directions
    
    Ensure the review meets academic publication standards.
    """
    
    print("📚 Starting Academic Literature Review...")
    print("=" * 60)
    
    response = team.run(query)
    
    print("\n" + "=" * 60)
    print("🎯 Literature Review Complete!")
    
    return response

if __name__ == "__main__":
    # Example usage
    research_topic = "Multi-agent systems in artificial intelligence"
    max_papers = 10
    
    result = conduct_literature_review(research_topic, max_papers)
    print(result.content)