#!/usr/bin/env python3
"""
AGNO Collaborate Mode Demo - Enhanced Financial Intelligence
Demonstrates advanced team collaboration patterns per AGNO best practices
"""

import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools
from agno.storage.sqlite import SqliteStorage

load_dotenv()

def create_collaborative_investment_team():
    """
    AGNO Collaborate Mode Demo - Advanced team interaction pattern
    
    This demonstrates the collaborate mode where agents engage in deeper 
    reasoning and discussion, as specified in AGNO documentation.
    """
    
    storage = SqliteStorage(
        table_name="collaborative_investment_team",
        db_file="collaborative_investment.db"
    )
    
    # Senior Investment Analyst - Strategic thinking
    senior_analyst = Agent(
        name="Senior Investment Analyst",
        role="Lead strategic investment analysis and challenge assumptions",
        model=OpenAIChat(id="gpt-4o"),  # Using more powerful model for senior role
        tools=[
            YFinanceTools(
                stock_price=True,
                company_info=True,
                analyst_recommendations=True,
                stock_fundamentals=True
            ),
            ReasoningTools(add_instructions=True)
        ],
        instructions=[
            "You are a senior investment analyst with 15+ years experience.",
            "Lead strategic discussions and challenge team assumptions.",
            "Ask probing questions to ensure thorough analysis.",
            "Identify potential blind spots in investment recommendations.",
            "Synthesize team insights into strategic recommendations."
        ],
        show_tool_calls=True,
        markdown=True
    )
    
    # Market Research Specialist - Data-driven insights
    market_researcher = Agent(
        name="Market Research Specialist", 
        role="Provide comprehensive market research and competitive analysis",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[
            DuckDuckGoTools(cache_results=True),
            YFinanceTools(company_news=True),
            ReasoningTools(add_instructions=True)
        ],
        instructions=[
            "You are a market research expert specializing in competitive intelligence.",
            "Provide comprehensive market context and competitive positioning.",
            "Challenge investment theses with market reality checks.",
            "Engage in analytical discussions with team members.",
            "Question assumptions and provide alternative perspectives."
        ],
        show_tool_calls=True,
        markdown=True
    )
    
    # Risk Management Expert - Conservative perspective
    risk_expert = Agent(
        name="Risk Management Expert",
        role="Provide risk assessment and challenge aggressive assumptions",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[
            YFinanceTools(stock_fundamentals=True),
            ReasoningTools(add_instructions=True)
        ],
        instructions=[
            "You are a risk management expert focused on capital preservation.",
            "Challenge optimistic projections with realistic risk assessments.",
            "Engage in debates about risk-return trade-offs.",
            "Provide conservative counterpoints to aggressive strategies.",
            "Ensure team considers downside scenarios thoroughly."
        ],
        show_tool_calls=True,
        markdown=True
    )
    
    # Create team in collaborate mode for deeper interaction
    team = Team(
        name="Collaborative Investment Research Team",
        mode="collaborate",  # AGNO collaborate mode for deeper reasoning
        members=[senior_analyst, market_researcher, risk_expert],
        instructions=[
            "Engage in thorough analytical discussions about investment opportunities.",
            "Challenge each other's assumptions and provide alternative perspectives.",
            "Debate the merits and risks of each investment recommendation.",
            "Build consensus through collaborative reasoning and analysis.",
            "Ensure all viewpoints are considered before reaching conclusions.",
            "Use your expertise to enhance the team's collective intelligence."
        ],
        success_criteria=[
            "Comprehensive debate covering multiple perspectives",
            "Risk-return analysis from conservative and aggressive viewpoints", 
            "Consensus recommendations with clear rationale",
            "Identification of key assumptions and potential blind spots",
            "Final recommendations that balance opportunity with prudent risk management"
        ],
        storage=storage,
        show_tool_calls=True,
        markdown=True,
        debug_mode=True,
    )
    
    return team

def collaborative_investment_analysis(symbols, investment_amount=1000000):
    """
    Demonstrate collaborative analysis with debate and discussion
    """
    
    team = create_collaborative_investment_team()
    
    query = f"""
    Please conduct a collaborative investment analysis for:
    
    Portfolio: {', '.join(symbols)}
    Investment Amount: ${investment_amount:,.2f}
    
    I want you to engage in a thorough analytical discussion where:
    
    1. The Senior Analyst leads strategic evaluation
    2. The Market Researcher provides competitive intelligence
    3. The Risk Expert challenges assumptions and highlights risks
    4. All team members debate the merits of each investment
    5. The team reaches consensus through collaborative reasoning
    
    Please show your collaborative process - I want to see the debate and 
    discussion that leads to your final recommendations.
    
    Focus on institutional-grade analysis with multiple perspectives.
    """
    
    print("🤝 Starting Collaborative Investment Analysis...")
    print("=" * 60)
    print("Note: This demonstrates AGNO's 'collaborate' mode with deeper reasoning")
    print("=" * 60)
    
    response = team.run(query)
    
    print("\n" + "=" * 60)
    print("🎯 Collaborative Analysis Complete!")
    print("This shows advanced AGNO team coordination patterns")
    
    return response

if __name__ == "__main__":
    # Demo with tech stocks
    symbols = ["AAPL", "MSFT", "NVDA"]
    investment_amount = 2000000
    
    result = collaborative_investment_analysis(symbols, investment_amount)
    print(result.content)