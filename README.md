# Executive Deep Research Assistant

A generative AI application that creates comprehensive executive reports by analyzing sales data and conducting industry research.

## Features

1. **Sales Data Analysis**: Process CSV sales data to create summaries by product and region
2. **Industry Research**: Use Tavily API to search for latest industry trends and competitive intelligence  
3. **Executive Reports**: Generate tailored summaries and recommendations for specific executive roles

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up API Keys

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

Or set these as environment variables.

### 3. Run the Application

```bash
streamlit run app.py
```

## Usage

1. **Input Parameters** (Left Panel):
   - Enter company name (e.g., "Apple Inc.")
   - Select executive role (CEO, CFO, etc.)
   - Provide API keys if not set in environment
   - Upload CSV sales data

2. **CSV Format**:
   The application automatically detects sales data columns. Supported formats include:
   - `product, region, sales`
   - `product, region, revenue_millions_usd`
   - `product, region, revenue`

3. **Generate Report**:
   Click "Generate Executive Report" to process data and create the report.

## Sample Data

The included `apple_weekly_sales_demo.csv` contains sample Apple sales data with columns:
- `week_start`: Week starting date
- `product`: Product category (iPhone, iPad, Mac, etc.)
- `region`: Geographic region (Americas, EMEA, etc.)
- `revenue_millions_usd`: Revenue in millions USD
- `units_thousands`: Units sold in thousands
- Additional metrics like targets and growth rates

## Executive Roles Supported

- CEO (Chief Executive Officer)
- CFO (Chief Financial Officer) 
- COO (Chief Operating Officer)
- CTO (Chief Technology Officer)
- CMO (Chief Marketing Officer)
- Head of Sales
- Head of Product
- VP Marketing
- VP Operations
- Chief Strategy Officer

Each role receives tailored analysis and recommendations relevant to their responsibilities.

## API Requirements

- **OpenAI API**: Required for generating executive summaries and recommendations
- **Tavily API**: Optional but recommended for industry research and competitive intelligence

## Output

The application generates:

1. **Sales Performance Overview**: Key metrics, product performance, regional breakdown
2. **Executive Summary**: Tailored for the selected executive role
3. **Key Findings**: Data-driven insights from the analysis
4. **Strategic Recommendations**: Prioritized actionable recommendations
5. **Risk Assessment**: Potential risks and challenges identified
6. **Next Steps**: Immediate action items

## Example

For Apple Inc. with CEO role:
- Analyzes iPhone, iPad, Mac, Services revenue across regions
- Researches latest Apple industry news and trends
- Generates CEO-focused strategic recommendations around growth, market expansion, competitive positioning
- Identifies risks like regional performance variations or product concentration

## Error Handling

- The app continues with sales analysis even if industry research fails
- Clear error messages for missing data or API issues
- Graceful handling of different CSV formats and column names