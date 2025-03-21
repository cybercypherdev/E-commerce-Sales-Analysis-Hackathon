import json
from pathlib import Path
import os

def create_powerbi_template():
    """Create a Power BI template configuration"""
    template = {
        "version": "1.0",
        "dataConnections": [
            {
                "name": "Sales by Region",
                "source": "total_sales_by_region.csv",
                "type": "CSV"
            },
            {
                "name": "Category Revenue",
                "source": "product_category_revenue_analysis.csv",
                "type": "CSV"
            },
            {
                "name": "Shipping Analysis",
                "source": "average_shipping_fee_by_region.csv",
                "type": "CSV"
            },
            {
                "name": "Age Impact",
                "source": "customer_age_impact_analysis.csv",
                "type": "CSV"
            },
            {
                "name": "Gender Analysis",
                "source": "popular_products_by_gender.csv",
                "type": "CSV"
            },
            {
                "name": "Order Fulfillment",
                "source": "order_fulfillment_analysis.csv",
                "type": "CSV"
            }
        ],
        "pages": [
            {
                "name": "Sales Overview",
                "visualizations": [
                    {
                        "type": "Map",
                        "title": "Sales by Region",
                        "dataSource": "Sales by Region"
                    },
                    {
                        "type": "Pie Chart",
                        "title": "Revenue by Category",
                        "dataSource": "Category Revenue"
                    },
                    {
                        "type": "Line Chart",
                        "title": "Monthly Sales Trend",
                        "dataSource": "Sales by Region"
                    }
                ]
            },
            {
                "name": "Customer Analysis",
                "visualizations": [
                    {
                        "type": "Scatter Plot",
                        "title": "Age vs Purchase Amount",
                        "dataSource": "Age Impact"
                    },
                    {
                        "type": "Stacked Bar",
                        "title": "Product Preferences by Gender",
                        "dataSource": "Gender Analysis"
                    }
                ]
            },
            {
                "name": "Shipping & Fulfillment",
                "visualizations": [
                    {
                        "type": "Column Chart",
                        "title": "Shipping Fees by Region",
                        "dataSource": "Shipping Analysis"
                    },
                    {
                        "type": "Donut Chart",
                        "title": "Order Status Distribution",
                        "dataSource": "Order Fulfillment"
                    }
                ]
            }
        ],
        "filters": [
            {
                "name": "Date Range",
                "type": "DateRange",
                "field": "Order Date"
            },
            {
                "name": "Region",
                "type": "MultiSelect",
                "field": "Region"
            },
            {
                "name": "Category",
                "type": "MultiSelect",
                "field": "Category"
            }
        ]
    }
    
    # Get the project root directory
    project_root = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Create the powerbi directory if it doesn't exist
    powerbi_dir = project_root / 'powerbi'
    powerbi_dir.mkdir(parents=True, exist_ok=True)
    
    # Save the template configuration
    template_path = powerbi_dir / 'dashboard_template.json'
    with open(template_path, 'w') as f:
        json.dump(template, f, indent=2)
    
    print(f"Power BI template configuration saved to: {template_path}")
    
    # Create a README for Power BI dashboard creation
    readme_path = powerbi_dir / 'README.md'
    readme_content = """# Power BI Dashboard Creation Guide

## Setup Instructions

1. Open Power BI Desktop
2. Import Data:
   - Click 'Get Data' > 'Text/CSV'
   - Navigate to the `powerbi/data` directory
   - Import all CSV files
   
3. Create Visualizations:
   - Follow the structure in `dashboard_template.json`
   - Use the provided images in `powerbi/images` for reference
   
4. Apply Formatting:
   - Use consistent colors for categories
   - Add titles and legends to all visualizations
   - Ensure proper scaling and axis labels
   
5. Add Interactivity:
   - Implement cross-filtering between visuals
   - Add slicers for date range, region, and category
   
6. Publish Dashboard:
   - Save the dashboard
   - Publish to Power BI Service
   - Update the link in the main README.md

## Dashboard Structure

1. Sales Overview Page:
   - Regional sales map
   - Category revenue distribution
   - Monthly sales trends
   
2. Customer Analysis Page:
   - Age vs purchase analysis
   - Gender-based preferences
   - Customer segments
   
3. Shipping & Fulfillment Page:
   - Regional shipping analysis
   - Order status distribution
   - Delivery time trends

## Data Refresh

The dashboard uses static CSV files. To update:
1. Run the analysis pipeline again
2. Refresh data in Power BI Desktop
3. Republish the dashboard
"""
    
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"Power BI setup guide saved to: {readme_path}")

if __name__ == "__main__":
    create_powerbi_template() 