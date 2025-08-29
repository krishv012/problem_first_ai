import streamlit as st
import pandas as pd
import os
from io import StringIO
import tempfile
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from data_processor import DataProcessor, create_data_summary_prompt
from search_tool import TavilySearchTool, create_industry_research_prompt
from executive_generator import ExecutiveReportGenerator


# Load environment variables
load_dotenv()

def main():
    st.set_page_config(
        page_title="Executive Deep Research",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Executive Deep Research Assistant")
    st.markdown("Generate comprehensive executive reports with sales data analysis and industry research")
    
    # Create two columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("Input Parameters")
        
        # Company Information
        st.subheader("Company Details")
        company_name = "Apple Inc."
        st.info(f"🏢 **Company:** {company_name}")
        
        executive_roles = [
            "CEO", "CFO", "COO", "CTO", "CMO", 
            "Head of Sales", "Head of Product", "VP Marketing",
            "VP Operations", "Chief Strategy Officer"
        ]
        executive_role = st.selectbox("Executive Role", executive_roles)
        
        # API Keys
        st.subheader("API Configuration")
        openai_key = st.text_input(
            "OpenAI API Key", 
            type="password", 
            value=os.getenv("OPENAI_API_KEY", ""),
            help="Required for generating executive summaries"
        )
        
        tavily_key = st.text_input(
            "Tavily API Key", 
            type="password", 
            value=os.getenv("TAVILY_API_KEY", ""),
            help="Required for industry research"
        )
        
        # File Upload
        st.subheader("Sales Data")
        uploaded_file = st.file_uploader(
            "Upload CSV Sales Data",
            type="csv",
            help="CSV should contain columns: product, region, sales"
        )
        
        # Show sample data format
        if st.checkbox("Show sample data format"):
            sample_data = {
                'product': ['iPhone', 'MacBook', 'iPad', 'iPhone', 'MacBook'],
                'region': ['North America', 'Europe', 'Asia', 'Europe', 'North America'],
                'sales': [1500000, 800000, 600000, 1200000, 900000]
            }
            st.dataframe(pd.DataFrame(sample_data))
        
        # Generate Report Button
        generate_button = st.button(
            "🚀 Generate Executive Report", 
            type="primary",
            use_container_width=True
        )
    
    with col2:
        st.header("Executive Report")
        
        if generate_button:
            logger.info("Generate button clicked")
            logger.debug(f"Company name: {company_name}")
            logger.debug(f"Executive role: {executive_role}")
            logger.debug(f"OpenAI key provided: {bool(openai_key)}")
            logger.debug(f"Tavily key provided: {bool(tavily_key)}")
            logger.debug(f"File uploaded: {uploaded_file is not None}")
            
            # Validate inputs
            if not openai_key:
                st.error("Please provide OpenAI API key")
                logger.warning("OpenAI API key validation failed")
                return
            
            if not uploaded_file:
                st.error("Please upload a CSV file")
                logger.warning("CSV file validation failed")
                return
            
            # Process the request
            with st.spinner("Generating your executive report..."):
                try:
                    logger.info("Starting report generation process")
                    
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue().decode('utf-8'))
                        csv_path = tmp_file.name
                    logger.debug(f"CSV file saved to: {csv_path}")
                    
                    # Initialize components
                    logger.info("Initializing data processor and report generator")
                    data_processor = DataProcessor()
                    report_generator = ExecutiveReportGenerator(openai_api_key=openai_key)
                    
                    # Process sales data
                    st.info("📊 Processing sales data...")
                    logger.info("Processing CSV data")
                    sales_data = data_processor.process_csv_data(csv_path)
                    logger.info(f"Sales data processed successfully. Total sales: {sales_data.total_sales}")
                    
                    # Display sales summary
                    display_sales_summary(sales_data, company_name)
                    
                    # Industry research (optional)
                    industry_research = None
                    if tavily_key:
                        st.info("🔍 Researching industry trends...")
                        try:
                            search_tool = TavilySearchTool(api_key=tavily_key)
                            products = list(sales_data.product_summary.keys())
                            industry_research = search_tool.search_company_trends(company_name, products)
                            st.success("Industry research completed!")
                        except Exception as e:
                            st.warning(f"Industry research failed: {str(e)}")
                            st.info("Continuing with sales data analysis only...")
                    else:
                        st.warning("Tavily API key not provided. Skipping industry research.")
                    
                    # Generate executive report
                    st.info("📝 Generating executive summary...")
                    if not industry_research:
                        # Create empty research object
                        from search_tool import IndustryResearch
                        industry_research = IndustryResearch(
                            company_trends=[],
                            product_trends=[],
                            industry_news=[],
                            competitive_landscape=[]
                        )
                    
                    executive_report, hallucination_score = report_generator.generate_executive_report(
                        company_name,
                        executive_role,
                        sales_data,
                        industry_research
                    )
                    
                    
                    # Display executive report
                    display_executive_report(executive_report, executive_role, hallucination_score)
                    
                    # Clean up temp file
                    os.unlink(csv_path)
                    
                    st.success("✅ Executive report generated successfully!")
                    
                except Exception as e:
                    logger.error(f"Error generating report: {str(e)}", exc_info=True)
                    st.error(f"Error generating report: {str(e)}")
                    if 'csv_path' in locals():
                        try:
                            os.unlink(csv_path)
                        except:
                            pass

def display_sales_summary(sales_data, company_name):
    """Display sales data summary"""
    
    st.subheader("📈 Sales Performance Overview")
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sales", f"${sales_data.total_sales:,.2f}")
    with col2:
        st.metric("Products", len(sales_data.product_summary))
    with col3:
        st.metric("Regions", len(sales_data.region_summary))
    
    # Product performance
    st.subheader("🛍️ Product Performance")
    product_df = pd.DataFrame([
        {
            'Product': product,
            'Total Sales': f"${stats['total_sales']:,.2f}",
            'Market Share': f"{stats['market_share_percent']:.1f}%",
            'Transactions': stats['transaction_count']
        }
        for product, stats in sales_data.product_summary.items()
    ])
    st.dataframe(product_df, use_container_width=True)
    
    # Regional performance
    st.subheader("🌍 Regional Performance")
    region_df = pd.DataFrame([
        {
            'Region': region,
            'Total Sales': f"${stats['total_sales']:,.2f}",
            'Market Share': f"{stats['market_share_percent']:.1f}%",
            'Transactions': stats['transaction_count']
        }
        for region, stats in sales_data.region_summary.items()
    ])
    st.dataframe(region_df, use_container_width=True)
    
    # Key insights
    st.subheader("💡 Key Insights")
    for insight in sales_data.key_insights:
        st.write(f"• {insight}")

def display_executive_report(executive_report, executive_role, hallucination_score=None):
    """Display the executive report"""
    
    st.subheader(f"📋 Executive Summary for {executive_role}")
    st.write(executive_report.executive_summary)
    
    # Key findings
    st.subheader("🔍 Key Findings")
    for finding in executive_report.key_findings:
        st.write(f"• {finding}")
    
    # Strategic recommendations
    st.subheader("🎯 Strategic Recommendations")
    
    # Debug: Show recommendation count
    logger.debug(f"Number of recommendations: {len(executive_report.strategic_recommendations)}")
    
    for i, rec in enumerate(executive_report.strategic_recommendations, 1):
        logger.debug(f"Recommendation {i}: priority={rec.priority}, recommendation_length={len(rec.recommendation) if rec.recommendation else 0}")
        # Color code priority
        priority_color = {
            "High": "🔴",
            "Medium": "🟡", 
            "Low": "🟢"
        }.get(rec.priority, "⚪")
        
        # Create a better title for the expander
        title = f"{priority_color} Recommendation {i}"
        if rec.recommendation and len(rec.recommendation) > 10:
            # Use first part of recommendation as subtitle
            subtitle = rec.recommendation[:50].replace('\n', ' ').strip()
            if len(rec.recommendation) > 50:
                subtitle += "..."
            title += f": {subtitle}"
        
        with st.expander(title):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Priority:** {rec.priority}")
                st.write(f"**Timeline:** {rec.timeline}")
            with col2:
                st.write(f"**Expected Impact:** {rec.expected_impact}")
            
            st.write("**Recommendation Details:**")
            if rec.recommendation:
                st.write(rec.recommendation)
            else:
                st.write("*No recommendation details available*")
    
    # Risk assessment
    if executive_report.risk_assessment:
        st.subheader("⚠️ Risk Assessment")
        st.write(executive_report.risk_assessment)
    
    # Next steps
    if executive_report.next_steps:
        st.subheader("✅ Next Steps")
        for step in executive_report.next_steps:
            st.write(f"• {step}")
    
    # Hallucination score (if available and successfully calculated)
    if hallucination_score is not None:
        st.subheader("🎯 Quality Assessment")
        
        # Color code the score
        score = hallucination_score.value
        if score < 0.3:
            score_color = "🟢"
            score_text = "Low Hallucination Risk"
        elif score < 0.7:
            score_color = "🟡"
            score_text = "Medium Hallucination Risk"
        else:
            score_color = "🔴"

        score_text = hallucination_score.reason 
        st.write(f"{score_color} **Hallucination Score:** {score:.3f} - {score_text}")
        st.caption("Lower scores indicate more reliable content with less hallucination risk.")
    else:
        # Optionally show a note that quality assessment wasn't available
        st.caption("ℹ️ Quality assessment not available for this report.")

if __name__ == "__main__":
    main()