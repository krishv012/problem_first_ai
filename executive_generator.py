import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from pydantic import BaseModel
from typing import List, Dict, Any
from data_processor import SalesData, create_data_summary_prompt
from search_tool import IndustryResearch, create_industry_research_prompt
from opik.evaluation.metrics import Hallucination



class ExecutiveRecommendation(BaseModel):
    recommendation: str
    category: str
    priority: str  # High, Medium, Low
    timeline: str
    expected_impact: str

class ExecutiveSummary(BaseModel):
    executive_summary: str
    key_findings: List[str]
    strategic_recommendations: List[ExecutiveRecommendation]
    risk_assessment: str
    next_steps: List[str]

class ExecutiveReportGenerator:
    def __init__(self, openai_api_key: str = None, opik_api_key: str = None):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.opik_api_key = opik_api_key or os.getenv("OPIK_API_KEY")
        
        self.llm = ChatOpenAI(
            api_key=self.openai_api_key,
            model="gpt-4",
            temperature=0.3
        )
        
        # Initialize Opik if API key is available
        self.opik = None
        if self.opik_api_key:
            try:
                # Opik initialization removed since we're only using evaluation metrics
                self.opik = True  # Just mark as available
            except Exception as e:
                print(f"Warning: Failed to initialize Opik: {e}")
                self.opik = None
    
    def generate_executive_report(
        self, 
        company_name: str, 
        executive_role: str,
        sales_data: SalesData, 
        industry_research: IndustryResearch
    ) -> tuple[ExecutiveSummary, float | None]:
        """
        Generate comprehensive executive report with summary and recommendations
        """
        
        # Create data summary
        data_summary = create_data_summary_prompt(sales_data, company_name)
        
        # Create industry research summary
        research_summary = create_industry_research_prompt(industry_research, company_name)
        
        # Generate executive summary and recommendations
        system_prompt = self._create_system_prompt(executive_role)
        human_prompt = self._create_human_prompt(company_name, data_summary, research_summary)
        
        try:
            # Use structured output with Pydantic model
            structured_llm = self.llm.with_structured_output(ExecutiveSummary)
            
            response = structured_llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ])
            
            # Response is already a structured ExecutiveSummary object
            parsed_response = response
            
            # Evaluate the response if Opik is available
            hallucination_score = None
            try:
                hallucination_metric = Hallucination()
                
                # Create context string safely
                context_parts = [str(sales_data)]
                if industry_research:
                    if hasattr(industry_research, 'company_trends') and industry_research.company_trends:
                        context_parts.append(str(industry_research.company_trends))
                    if hasattr(industry_research, 'product_trends') and industry_research.product_trends:
                        context_parts.append(str(industry_research.product_trends))
                    if hasattr(industry_research, 'industry_news') and industry_research.industry_news:
                        context_parts.append(str(industry_research.industry_news))
                    if hasattr(industry_research, 'competitive_landscape') and industry_research.competitive_landscape:
                        context_parts.append(str(industry_research.competitive_landscape))
                
                context = "\n".join(context_parts)
                
                hallucination_score = hallucination_metric.score(
                    output=parsed_response,
                    input=system_prompt + "\n" + human_prompt,
                    context=context
                )
                print(f"Hallucination score: {hallucination_score}")
            
            except Exception as e:
                print(f"Error evaluating hallucination: {e}")
            
            # Return both the parsed response and hallucination score separately
            return parsed_response, hallucination_score
            
        except Exception as e:
            raise Exception(f"Error generating executive report: {str(e)}")

        
    
    def _create_system_prompt(self, executive_role: str) -> str:
        """Create system prompt based on executive role"""
        
        role_contexts = {
            "ceo": "chief executive officer focused on overall strategy, growth, and shareholder value",
            "cfo": "chief financial officer focused on financial performance, profitability, and risk management", 
            "coo": "chief operating officer focused on operational efficiency, process optimization, and execution",
            "cmo": "chief marketing officer focused on brand strategy, customer acquisition, and market positioning",
            "cto": "chief technology officer focused on technology strategy, innovation, and digital transformation",
            "head of sales": "sales leader focused on revenue growth, sales performance, and market expansion",
            "head of product": "product leader focused on product strategy, development, and market fit"
        }
        
        role_context = role_contexts.get(executive_role.lower(), f"{executive_role} focused on strategic leadership and business performance")
        
        return f"""You are an expert business analyst creating an executive briefing for a {role_context}.

Your task is to analyze sales data and industry research to provide:
1. A concise executive summary (2-3 paragraphs)
2. Key findings (3-5 bullet points)
3. Strategic recommendations with priority, timeline, and expected impact
4. Risk assessment
5. Next steps

Tailor your analysis and recommendations specifically for the {executive_role} perspective.
Be data-driven, actionable, and strategic in your recommendations.
Focus on insights that would be most relevant and valuable for this executive role.

For strategic recommendations:
- Provide 2-3 detailed, actionable recommendations
- Each recommendation should have a clear description of what to do
- Category should be one of: Strategic, Operational, Financial, Marketing
- Priority should be one of: High, Medium, Low
- Timeline should be one of: Immediate, Short-term, Long-term
- Expected Impact should describe the anticipated business impact

For key findings and next steps, provide 3-5 clear, specific items each."""
    
    def _create_human_prompt(self, company_name: str, data_summary: str, research_summary: str) -> str:
        """Create the human prompt with all context"""
        
        return f"""Please analyze the following information for {company_name} and create a comprehensive executive briefing:

{data_summary}

{research_summary}

Based on this sales data and industry research, provide strategic insights and actionable recommendations tailored for the executive role specified in the system prompt."""
    

    
