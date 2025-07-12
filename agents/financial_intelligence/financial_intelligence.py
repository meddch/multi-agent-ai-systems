#!/usr/bin/env python3
"""
Financial Intelligence Platform - Level 4 Multi-Agent System
Simple local development version
"""

import os
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools
from agno.storage.sqlite import SqliteStorage

# Load environment variables
load_dotenv()

# Structured Output Models (AGNO Best Practice)
class StockRecommendation(BaseModel):
    """Structured stock recommendation output"""
    symbol: str = Field(description="Stock symbol")
    recommendation: str = Field(description="BUY, HOLD, or SELL")
    target_price: float = Field(description="12-month price target")
    confidence: float = Field(description="Confidence level 0-1")
    allocation_percent: float = Field(description="Recommended portfolio allocation %")

class PortfolioAnalysis(BaseModel):
    """Structured portfolio analysis output"""
    total_investment: float = Field(description="Total investment amount")
    stock_recommendations: List[StockRecommendation] = Field(description="Individual stock recommendations")
    portfolio_risk_score: float = Field(description="Overall risk score 0-10")
    expected_return: float = Field(description="Expected annual return %")
    executive_summary: str = Field(description="Key insights and recommendations")

def create_financial_intelligence_team():
    """Create the financial intelligence team with 5 specialized agents"""
    
    # Create storage instance
    storage = SqliteStorage(
        table_name="financial_intelligence_team",
        db_file="financial_intelligence.db"
    )
    
    # Market Data Analyst
    market_analyst = Agent(
        name="Market Data Analyst",
        role="Analyze individual stock performance and market conditions",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[
            YFinanceTools(
                stock_price=True,
                company_info=True,
                analyst_recommendations=True,
                company_news=True
            )
        ],
        instructions=[
            "You are a senior market analyst with expertise in equity research.",
            "Analyze each stock's financial metrics, recent performance, and market position.",
            "Provide specific price targets and recommendation rationales.",
            "Include quantitative metrics: P/E, ROE, revenue growth, market cap.",
            "Structure your analysis with clear buy/hold/sell recommendations."
        ],
        show_tool_calls=True,
        markdown=True
    )
    
    # Market Sentiment Analyst
    sentiment_analyst = Agent(
        name="Market Sentiment Analyst",
        role="Analyze market sentiment and news impact on stocks",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[
            DuckDuckGoTools(cache_results=True),
            ReasoningTools(add_instructions=True)
        ],
        instructions=[
            "You are a sentiment analysis expert specializing in financial markets.",
            "Analyze recent news, social media sentiment, and market psychology.",
            "Identify sentiment trends that could impact stock performance.",
            "Provide sentiment scores and trend analysis.",
            "Consider both short-term and long-term sentiment implications."
        ],
        show_tool_calls=True,
        markdown=True
    )
    
    # Risk Assessment Specialist
    risk_assessor = Agent(
        name="Risk Assessment Specialist",
        role="Evaluate portfolio risk and provide mitigation strategies",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[
            YFinanceTools(stock_fundamentals=True),
            ReasoningTools(add_instructions=True)
        ],
        instructions=[
            "You are a risk management expert with deep knowledge of portfolio theory.",
            "Analyze systematic and unsystematic risks for each investment.",
            "Calculate portfolio volatility, beta, and correlation metrics.",
            "Identify potential risk factors: sector concentration, market cycles, liquidity.",
            "Provide specific risk mitigation strategies and position sizing guidance."
        ],
        show_tool_calls=True,
        markdown=True
    )
    
    # Portfolio Strategy Advisor
    portfolio_strategist = Agent(
        name="Portfolio Strategy Advisor",
        role="Design optimal portfolio allocation and investment strategy",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[ReasoningTools(add_instructions=True)],
        instructions=[
            "You are a portfolio strategist with expertise in asset allocation.",
            "Design optimal portfolio allocations based on risk-return profiles.",
            "Consider investment timeline, risk tolerance, and diversification.",
            "Provide specific allocation percentages and rebalancing schedules.",
            "Include tactical and strategic allocation recommendations."
        ],
        show_tool_calls=True,
        markdown=True
    )
    
    # Research Coordinator
    research_coordinator = Agent(
        name="Research Coordinator",
        role="Synthesize analysis and ensure comprehensive coverage",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[ReasoningTools(add_instructions=True)],
        instructions=[
            "You are a research director responsible for comprehensive investment analysis.",
            "Synthesize insights from market, sentiment, and risk analysis.",
            "Ensure all aspects of investment decision-making are covered.",
            "Provide executive summary with clear actionable recommendations.",
            "Maintain high analytical standards and quality control."
        ],
        show_tool_calls=True,
        markdown=True
    )
    
    # Create coordinated team with AGNO best practices
    team = Team(
        name="Financial Intelligence Team",
        mode="coordinate",  # AGNO coordination mode for collaborative problem-solving
        members=[market_analyst, sentiment_analyst, risk_assessor, portfolio_strategist, research_coordinator],
        instructions=[
            "Work together systematically to provide comprehensive investment analysis.",
            "Build upon each other's analysis to create cohesive recommendations.",
            "Ensure quantitative rigor and risk-aware decision making.",
            "Deliver institutional-quality investment research.",
            "Each agent should contribute their specialized expertise to the team goal.",
            "Share context and insights to enable collective intelligence."
        ],
        success_criteria=[
            "All stocks analyzed with quantitative metrics and clear recommendations",
            "Portfolio risk assessment completed with specific risk scores",
            "Allocation percentages provided for each investment",
            "Executive summary delivered with actionable insights",
            "Analysis meets institutional investment standards"
        ],
        storage=storage,
        show_tool_calls=True,
        markdown=True,
        debug_mode=True,
    )
    
    return team

def analyze_portfolio(symbols, investment_amount=100000):
    """Analyze a portfolio of stocks"""
    
    team = create_financial_intelligence_team()
    
    query = f"""
    Conduct comprehensive investment analysis for the following portfolio:
    
    Symbols: {', '.join(symbols)}
    Investment Amount: ${investment_amount:,.2f}
    
    Please provide:
    1. Individual stock analysis with financial metrics and recommendations
    2. Market sentiment analysis and news impact assessment
    3. Portfolio risk evaluation with quantitative measures
    4. Optimal allocation strategy with specific percentages
    5. Executive summary with actionable investment recommendations
    
    Ensure analysis meets institutional investment standards.
    """
    
    print("🏦 Starting Financial Intelligence Analysis...")
    print("=" * 60)
    
    response = team.run(query)
    
    print("\n" + "=" * 60)
    print("🎯 Analysis Complete!")
    
    return response

if __name__ == "__main__":
    # Example usage
    symbols = ["AAPL", "MSFT", "GOOGL"]
    investment_amount = 500000
    
    result = analyze_portfolio(symbols, investment_amount)
    print(result.content)