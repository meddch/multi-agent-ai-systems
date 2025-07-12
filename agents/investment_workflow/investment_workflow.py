#!/usr/bin/env python3
"""
Self-Improving Investment Research Workflow - Level 5 Agentic System
Simple local development version
"""

import os
import time
from datetime import datetime
from typing import List, Iterator, Dict, Any
from dotenv import load_dotenv
from agno.agent import Agent
# Removed Workflow import - implementing custom workflow pattern
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools
from agno.storage.sqlite import SqliteStorage

# Load environment variables
load_dotenv()

class SelfImprovingInvestmentWorkflow:
    """Level 5 workflow with self-improvement capabilities"""
    
    def __init__(self, session_id: str = None, quality_threshold: float = 0.85, max_iterations: int = 3):
        
        self.session_id = session_id or f"workflow_{int(time.time())}"
        self.quality_threshold = quality_threshold
        self.max_iterations = max_iterations
        self.session_state = {}
        self.iteration_count = 0
        self.quality_history = []
        
        # Shared storage for state persistence
        self.storage = SqliteStorage(table_name="workflow_sessions", db_file="investment_workflow.db")
        
        # Initialize agents
        self.market_researcher = Agent(
            name="Market Researcher",
            role="Comprehensive market research and data analysis",
            model=OpenAIChat(id="gpt-4o-mini"),
            tools=[
                YFinanceTools(
                    stock_price=True,
                    stock_fundamentals=True,
                    company_info=True,
                    company_news=True
                ),
                DuckDuckGoTools(cache_results=True)
            ],
            instructions=[
                "You are a senior market researcher with deep expertise in financial analysis.",
                "Conduct thorough research on market conditions, company fundamentals, and industry trends.",
                "Provide comprehensive data-driven insights with quantitative metrics.",
                "Focus on actionable intelligence for investment decision-making.",
                "Ensure all analysis is current and based on the latest available data."
            ],
            storage=self.storage,
            show_tool_calls=True,
            markdown=True,
            debug_mode=True
        )
        
        self.risk_analyst = Agent(
            name="Risk Analyst",
            role="Advanced risk assessment and portfolio optimization",
            model=OpenAIChat(id="gpt-4o-mini"),
            tools=[
                YFinanceTools(stock_fundamentals=True),
                ReasoningTools(add_instructions=True)
            ],
            instructions=[
                "You are a risk management expert specializing in quantitative analysis.",
                "Evaluate portfolio risk using modern portfolio theory and advanced metrics.",
                "Calculate VaR, beta, correlation matrices, and stress test scenarios.",
                "Provide specific risk mitigation strategies and position sizing recommendations.",
                "Focus on preserving capital while optimizing risk-adjusted returns."
            ],
            storage=self.storage,
            show_tool_calls=True,
            markdown=True,
            debug_mode=True
        )
        
        self.portfolio_optimizer = Agent(
            name="Portfolio Optimizer",
            role="Optimal portfolio construction and allocation strategy",
            model=OpenAIChat(id="gpt-4o-mini"),
            tools=[ReasoningTools(add_instructions=True)],
            instructions=[
                "You are a portfolio optimization expert with advanced quantitative skills.",
                "Design optimal portfolios using mean-variance optimization and modern techniques.",
                "Consider constraints, transaction costs, and rebalancing frequencies.",
                "Provide specific allocation percentages and implementation guidelines.",
                "Optimize for risk-adjusted returns while meeting investor objectives."
            ],
            storage=self.storage,
            show_tool_calls=True,
            markdown=True,
            debug_mode=True
        )
        
        self.quality_evaluator = Agent(
            name="Quality Evaluator",
            role="Assess analysis quality and identify improvement opportunities",
            model=OpenAIChat(id="gpt-4o"),
            tools=[ReasoningTools(add_instructions=True)],
            instructions=[
                "You are a quality assurance expert for investment research.",
                "Evaluate analysis quality across multiple dimensions: accuracy, completeness, insight depth.",
                "Identify gaps, weaknesses, and areas for improvement in investment analysis.",
                "Provide specific recommendations for enhancing analysis quality.",
                "Maintain high standards consistent with institutional investment research."
            ],
            storage=self.storage,
            show_tool_calls=True,
            markdown=True,
            debug_mode=True
        )
        
        self.improvement_strategist = Agent(
            name="Improvement Strategist",
            role="Generate targeted improvements for analysis enhancement",
            model=OpenAIChat(id="gpt-4o"),
            tools=[ReasoningTools(add_instructions=True)],
            instructions=[
                "You are an expert in systematic improvement of investment analysis.",
                "Generate specific, actionable improvements based on quality assessments.",
                "Focus on enhancing analytical rigor, depth, and practical utility.",
                "Provide step-by-step improvement strategies with clear implementation guidance.",
                "Ensure improvements address identified weaknesses systematically."
            ],
            storage=self.storage,
            show_tool_calls=True,
            markdown=True,
            debug_mode=True
        )
        
        self.final_validator = Agent(
            name="Final Validator",
            role="Final validation and synthesis of improved analysis",
            model=OpenAIChat(id="gpt-4o-mini"),
            tools=[ReasoningTools(add_instructions=True)],
            instructions=[
                "You are a senior investment committee member responsible for final validation.",
                "Review and validate the complete investment analysis for accuracy and completeness.",
                "Ensure all recommendations are well-supported and actionable.",
                "Provide final synthesis with executive summary and clear next steps.",
                "Maintain institutional-grade standards for investment decision-making."
            ],
            storage=self.storage,
            show_tool_calls=True,
            markdown=True,
            debug_mode=True
        )
    
    def run(self, symbols: List[str], investment_amount: float = 1000000) -> Iterator[str]:
        """Execute the self-improving workflow"""
        
        print(f"🚀 Starting Self-Improving Investment Workflow")
        print(f"Session ID: {self.session_id}")
        print(f"Symbols: {symbols}")
        print(f"Investment Amount: ${investment_amount:,.2f}")
        print(f"Quality Threshold: {self.quality_threshold}")
        print("=" * 60)
        
        # Stage 1: Market Research
        self.session_state['stage'] = 'market_research'
        print("📊 Stage 1: Market Research")
        
        research_query = f"""
        Conduct comprehensive market research for: {', '.join(symbols)}
        Investment amount: ${investment_amount:,.2f}
        
        Provide detailed analysis including:
        - Current market conditions and trends
        - Individual company fundamentals and financial metrics
        - Industry analysis and competitive positioning
        - Recent news and market sentiment
        - Technical and fundamental analysis
        """
        
        research_result = self.market_researcher.run(research_query)
        yield f"✅ Market Research Complete\n\n{research_result.content}"
        
        # Stage 2: Risk Analysis
        self.session_state['stage'] = 'risk_analysis'
        print("\n⚠️ Stage 2: Risk Analysis")
        
        risk_query = f"""
        Based on the market research, conduct advanced risk analysis for: {', '.join(symbols)}
        
        Market Research Context:
        {research_result.content}
        
        Provide comprehensive risk assessment including:
        - Individual stock risk metrics (beta, volatility, VaR)
        - Portfolio risk analysis and correlation matrix
        - Stress testing and scenario analysis
        - Risk mitigation strategies
        - Position sizing recommendations
        """
        
        risk_result = self.risk_analyst.run(risk_query)
        yield f"✅ Risk Analysis Complete\n\n{risk_result.content}"
        
        # Stage 3: Portfolio Optimization
        self.session_state['stage'] = 'portfolio_optimization'
        print("\n🎯 Stage 3: Portfolio Optimization")
        
        optimization_query = f"""
        Based on market research and risk analysis, optimize portfolio for: {', '.join(symbols)}
        Investment amount: ${investment_amount:,.2f}
        
        Context:
        Market Research: {research_result.content[:1000]}...
        Risk Analysis: {risk_result.content[:1000]}...
        
        Provide optimal portfolio construction including:
        - Specific allocation percentages for each symbol
        - Risk-adjusted return optimization
        - Rebalancing strategy and timeline
        - Implementation guidance
        - Performance expectations
        """
        
        optimization_result = self.portfolio_optimizer.run(optimization_query)
        yield f"✅ Portfolio Optimization Complete\n\n{optimization_result.content}"
        
        # Combine initial analysis
        combined_analysis = f"""
        Market Research:
        {research_result.content}
        
        Risk Analysis:
        {risk_result.content}
        
        Portfolio Optimization:
        {optimization_result.content}
        """
        
        # Stage 4: Quality Evaluation & Self-Improvement Loop
        current_analysis = combined_analysis
        
        for iteration in range(self.max_iterations):
            self.iteration_count = iteration + 1
            
            print(f"\n🔍 Quality Evaluation - Iteration {self.iteration_count}")
            
            # Evaluate quality
            quality_query = f"""
            Evaluate the quality of this investment analysis:
            
            {current_analysis}
            
            Assess quality across these dimensions:
            1. Analytical rigor and methodology
            2. Completeness of coverage
            3. Depth of insights
            4. Practical utility and actionability
            5. Risk awareness and mitigation
            
            Provide overall quality score (0-1) and specific improvement recommendations.
            """
            
            quality_result = self.quality_evaluator.run(quality_query)
            
            # Extract quality score (simplified - in production would use structured output)
            quality_score = self._extract_quality_score(quality_result.content)
            self.quality_history.append(quality_score)
            
            print(f"Quality Score: {quality_score:.2f} (Threshold: {self.quality_threshold})")
            
            if quality_score >= self.quality_threshold:
                print("✅ Quality threshold achieved!")
                break
            
            print("🔄 Generating improvements...")
            
            # Generate improvements
            improvement_query = f"""
            Based on the quality evaluation, generate specific improvements:
            
            Current Analysis:
            {current_analysis}
            
            Quality Assessment:
            {quality_result.content}
            
            Provide specific, actionable improvements to enhance the analysis quality.
            Focus on addressing identified weaknesses and gaps.
            """
            
            improvement_result = self.improvement_strategist.run(improvement_query)
            
            # Apply improvements
            improvement_application_query = f"""
            Apply the following improvements to enhance the investment analysis:
            
            Original Analysis:
            {current_analysis}
            
            Improvements to Apply:
            {improvement_result.content}
            
            Provide the enhanced analysis incorporating all improvements.
            """
            
            enhanced_result = self.final_validator.run(improvement_application_query)
            current_analysis = enhanced_result.content
            
            yield f"🔄 Iteration {self.iteration_count} - Quality Score: {quality_score:.2f}\n\nImprovements Applied:\n{improvement_result.content}"
        
        # Stage 5: Final Validation
        self.session_state['stage'] = 'final_validation'
        print("\n✅ Final Validation")
        
        final_query = f"""
        Provide final validation and executive summary for this investment analysis:
        
        {current_analysis}
        
        Provide:
        1. Executive summary with key recommendations
        2. Final validation of analysis quality
        3. Clear next steps and implementation guidance
        4. Risk warnings and disclaimers
        """
        
        final_result = self.final_validator.run(final_query)
        
        # Save session state
        self.session_state['completed_at'] = datetime.now().isoformat()
        self.session_state['final_quality'] = self.quality_history[-1] if self.quality_history else 0
        self.session_state['iterations_completed'] = self.iteration_count
        
        yield f"🎉 Workflow Complete!\n\nFinal Analysis:\n{final_result.content}"
    
    def _extract_quality_score(self, quality_text: str) -> float:
        """Extract quality score from quality evaluation text (simplified)"""
        # In production, this would use structured output or more sophisticated parsing
        import re
        
        # Look for patterns like "quality score: 0.85" or "score of 0.85"
        patterns = [
            r'quality score:?\s*(\d+\.?\d*)',
            r'score of\s*(\d+\.?\d*)',
            r'overall.*?(\d+\.?\d*)',
            r'(\d+\.?\d*)/1\.0',
            r'(\d+\.?\d*)%'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, quality_text.lower())
            if match:
                score = float(match.group(1))
                # Handle percentage
                if '%' in pattern:
                    score = score / 100
                # Ensure score is in 0-1 range
                if score > 1:
                    score = score / 100
                return min(max(score, 0), 1)
        
        # Default to 0.75 if no score found
        return 0.75

def run_investment_workflow(symbols: List[str], investment_amount: float = 1000000, 
                          quality_threshold: float = 0.85, max_iterations: int = 3):
    """Run the self-improving investment workflow"""
    
    workflow = SelfImprovingInvestmentWorkflow(
        quality_threshold=quality_threshold,
        max_iterations=max_iterations
    )
    
    print("💼 Self-Improving Investment Research Workflow")
    print("=" * 60)
    
    # Execute the workflow and iterate over results
    for stage_result in workflow.run(symbols, investment_amount):
        print(stage_result)
        print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    # Example usage
    symbols = ["AAPL", "MSFT", "GOOGL", "NVDA"]
    investment_amount = 2000000
    quality_threshold = 0.85
    max_iterations = 3
    
    run_investment_workflow(symbols, investment_amount, quality_threshold, max_iterations)