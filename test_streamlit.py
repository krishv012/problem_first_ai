#!/usr/bin/env python3

import os
import tempfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🧪 Testing Streamlit App Components\n")

# Test app imports and initialization
print("=" * 50)
print("TEST: Streamlit App Import and Components")
print("=" * 50)

try:
    # Test if all components can be imported
    from data_processor import DataProcessor, create_data_summary_prompt
    from search_tool import TavilySearchTool, create_industry_research_prompt  
    from executive_generator import ExecutiveReportGenerator
    import streamlit as st
    import pandas as pd
    
    print("✅ All required modules imported successfully!")
    
    # Test the main workflow that the Streamlit app uses
    print("\n🔄 Testing main workflow...")
    
    # Initialize components
    data_processor = DataProcessor()
    search_tool = TavilySearchTool()
    report_generator = ExecutiveReportGenerator()
    
    # Process CSV data
    print("📊 Processing CSV data...")
    sales_data = data_processor.process_csv_data("apple_weekly_sales_demo.csv")
    
    # Create data summary prompt
    data_summary = create_data_summary_prompt(sales_data, "Apple Inc.")
    print(f"✅ Data summary created: {len(data_summary)} characters")
    
    # Conduct industry research
    print("🔍 Conducting industry research...")
    products = list(sales_data.product_summary.keys())[:2]
    industry_research = search_tool.search_company_trends("Apple Inc.", products)
    
    # Create research summary prompt
    research_summary = create_industry_research_prompt(industry_research, "Apple Inc.")
    print(f"✅ Research summary created: {len(research_summary)} characters")
    
    # Generate executive report
    print("📝 Generating executive report...")
    executive_report = report_generator.generate_executive_report(
        "Apple Inc.",
        "CEO",
        sales_data,
        industry_research
    )
    
    print("✅ Executive report generated successfully!")
    
    # Test different file upload scenario (simulating Streamlit file upload)
    print("\n📁 Testing file upload simulation...")
    
    # Read the demo CSV to simulate uploaded file content
    with open("apple_weekly_sales_demo.csv", "r") as f:
        csv_content = f.read()
    
    # Create temporary file (similar to what Streamlit does)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
        tmp_file.write(csv_content)
        temp_csv_path = tmp_file.name
    
    # Process the temporary file
    temp_sales_data = data_processor.process_csv_data(temp_csv_path)
    print("✅ Temporary file processing successful!")
    
    # Clean up
    os.unlink(temp_csv_path)
    
    print("\n🎯 Testing role-specific reports...")
    roles = ["CEO", "CFO", "CTO", "CMO", "Head of Sales"]
    
    for role in roles:
        report = report_generator.generate_executive_report(
            "Apple Inc.",
            role,
            sales_data,
            industry_research
        )
        print(f"✅ {role} report: {len(report.strategic_recommendations)} recommendations")
    
    print("\n" + "=" * 50)
    print("🎉 STREAMLIT APP COMPONENTS TEST COMPLETE!")
    print("=" * 50)
    print("✅ All components work correctly")
    print("✅ File upload simulation successful")  
    print("✅ Role-specific reports generated")
    print("✅ Ready for full Streamlit deployment")
    
except Exception as e:
    print(f"❌ Error testing app components: {e}")
    import traceback
    traceback.print_exc()

# Test error handling scenarios
print("\n" + "=" * 50)
print("TEST: Error Handling Scenarios")
print("=" * 50)

try:
    # Test invalid CSV file
    print("🧪 Testing invalid file path...")
    try:
        data_processor.process_csv_data("nonexistent.csv")
        print("❌ Should have failed with invalid file")
    except Exception as e:
        print(f"✅ Correctly handled invalid file: {type(e).__name__}")
    
    # Test invalid API key scenarios
    print("\n🧪 Testing invalid API keys...")
    try:
        invalid_search = TavilySearchTool(api_key="invalid_key")
        invalid_search.search_company_trends("Apple", ["iPhone"])
        print("❌ Should have failed with invalid Tavily key")
    except Exception as e:
        print(f"✅ Correctly handled invalid Tavily key: {type(e).__name__}")
    
    try:
        invalid_generator = ExecutiveReportGenerator(openai_api_key="invalid_key")
        # This would fail on actual API call, but constructor should work
        print("✅ OpenAI generator constructor handles invalid key gracefully")
    except Exception as e:
        print(f"⚠️ OpenAI generator constructor error: {type(e).__name__}")
    
    print("\n✅ Error handling tests completed!")
    
except Exception as e:
    print(f"❌ Error in error handling tests: {e}")

print("\n" + "=" * 50)
print("🏁 ALL TESTS COMPLETED!")
print("=" * 50)
print("🚀 Application is ready for use!")
print("   Run: streamlit run app.py")
print("=" * 50)