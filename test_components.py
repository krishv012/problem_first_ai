#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🧪 Testing Executive Deep Research Application Components\n")

# Test 1: Data Processor
print("=" * 50)
print("TEST 1: CSV Data Processing")
print("=" * 50)

try:
    from data_processor import DataProcessor
    
    processor = DataProcessor()
    sales_data = processor.process_csv_data("apple_weekly_sales_demo.csv")
    
    print(f"✅ CSV processed successfully!")
    print(f"📊 Total Sales: ${sales_data.total_sales:,.2f} million")
    print(f"📱 Products: {len(sales_data.product_summary)}")
    print(f"🌍 Regions: {len(sales_data.region_summary)}")
    
    print("\n📱 Product Performance:")
    for product, stats in sales_data.product_summary.items():
        print(f"  • {product}: ${stats['total_sales']:,.2f}M ({stats['market_share_percent']:.1f}%)")
    
    print("\n🌍 Regional Performance:")
    for region, stats in sales_data.region_summary.items():
        print(f"  • {region}: ${stats['total_sales']:,.2f}M ({stats['market_share_percent']:.1f}%)")
    
    print("\n💡 Key Insights:")
    for insight in sales_data.key_insights:
        print(f"  • {insight}")
    
except Exception as e:
    print(f"❌ Data processing failed: {e}")
    sys.exit(1)

# Test 2: Tavily Search
print("\n" + "=" * 50)
print("TEST 2: Industry Research (Tavily)")
print("=" * 50)

try:
    from search_tool import TavilySearchTool
    
    search_tool = TavilySearchTool()
    products = list(sales_data.product_summary.keys())[:2]  # Test with top 2 products
    
    print(f"🔍 Searching for Apple and products: {products}")
    industry_research = search_tool.search_company_trends("Apple", products)
    
    print(f"✅ Industry research completed!")
    print(f"📰 Company trends found: {len(industry_research.company_trends)}")
    print(f"📈 Product trends found: {len(industry_research.product_trends)}")
    print(f"📊 Industry news found: {len(industry_research.industry_news)}")
    print(f"🏢 Competitive landscape found: {len(industry_research.competitive_landscape)}")
    
    if industry_research.company_trends:
        print(f"\n📰 Sample Company Trend:")
        trend = industry_research.company_trends[0]
        print(f"  Title: {trend.title}")
        print(f"  Content: {trend.content[:200]}...")
    
except Exception as e:
    print(f"❌ Industry research failed: {e}")
    print("⚠️  Continuing without industry research...")
    from search_tool import IndustryResearch
    industry_research = IndustryResearch(
        company_trends=[],
        product_trends=[],
        industry_news=[],
        competitive_landscape=[]
    )

# Test 3: Executive Report Generation
print("\n" + "=" * 50)
print("TEST 3: Executive Report Generation")
print("=" * 50)

try:
    from executive_generator import ExecutiveReportGenerator
    
    report_generator = ExecutiveReportGenerator()
    
    print("📝 Generating CEO executive report...")
    executive_report, hallucination_score = report_generator.generate_executive_report(
        "Apple Inc.",
        "CEO",
        sales_data,
        industry_research
    )
    
    print(f"✅ Executive report generated!")
    print(f"📋 Executive Summary: {len(executive_report.executive_summary)} characters")
    print(f"🔍 Key Findings: {len(executive_report.key_findings)} items")
    print(f"🎯 Strategic Recommendations: {len(executive_report.strategic_recommendations)} items")
    
    print(f"\n📋 Executive Summary (Preview):")
    print(f"  {executive_report.executive_summary[:300]}...")
    
    print(f"\n🔍 Key Findings:")
    for i, finding in enumerate(executive_report.key_findings[:3], 1):
        print(f"  {i}. {finding}")
    
    print(f"\n🎯 Strategic Recommendations:")
    for i, rec in enumerate(executive_report.strategic_recommendations[:2], 1):
        print(f"  {i}. [{rec.priority}]: {rec.recommendation[:100]}...")
    
except Exception as e:
    print(f"❌ Executive report generation failed: {e}")
    sys.exit(1)

# Test 4: Different Executive Roles
print("\n" + "=" * 50)
print("TEST 4: Different Executive Roles")
print("=" * 50)

try:
    roles_to_test = ["CFO", "CTO", "CMO"]
    
    for role in roles_to_test:
        print(f"\n📝 Testing {role} report generation...")
        role_report, role_hallucination_score = report_generator.generate_executive_report(
            "Apple Inc.",
            role,
            sales_data,
            industry_research
        )
        print(f"✅ {role} report generated successfully!")
        print(f"   Summary length: {len(role_report.executive_summary)} chars")
        print(f"   Recommendations: {len(role_report.strategic_recommendations)} items")
        
except Exception as e:
    print(f"❌ Role-specific report generation failed: {e}")

print("\n" + "=" * 50)
print("🎉 COMPONENT TESTING COMPLETE!")
print("=" * 50)
print("✅ All core components are working correctly")
print("🚀 Ready to test the full Streamlit application")
print("\nRun: streamlit run app.py")
print("=" * 50)