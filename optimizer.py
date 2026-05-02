import pandas as pd
import numpy as np

# 1. DATA INGESTION & GENERATION
# This demonstrates data handling skills as learned in your Google Data Analytics course
def load_data():
    data = {
        'Product_ID': ['P001', 'P002', 'P003', 'P004', 'P005'],
        'Category': ['Electronics', 'Groceries', 'Electronics', 'Pharma', 'Groceries'],
        'Daily_Demand_Mean': [50, 120, 30, 10, 80],
        'Daily_Demand_Std': [5, 12, 4, 1, 8], # Variability in demand
        'Lead_Time_Days': [7, 3, 5, 15, 4],    # Days to restock
        'Current_Stock': [250, 400, 100, 200, 50],
        'Unit_Cost': [1200, 50, 1500, 2000, 40]
    }
    return pd.DataFrame(data)

def optimize_inventory(df):
    # 2. SAFETY STOCK CALCULATION
    # Formula: Service Level (95%) * Std Dev of Demand during Lead Time
    # Reflects Python programming fundamentals from Infosys Springboard
    z_score = 1.645 
    df['Safety_Stock'] = round(z_score * np.sqrt(df['Lead_Time_Days'] * (df['Daily_Demand_Std']**2)))

    # 3. REORDER POINT (ROP) CALCULATION
    # ROP = (Average Daily Demand * Lead Time) + Safety Stock
    df['Reorder_Point'] = (df['Daily_Demand_Mean'] * df['Lead_Time_Days']) + df['Safety_Stock']

    # 4. ACTION LOGIC
    # Identifying if we need to restock immediately
    df['Status'] = np.where(df['Current_Stock'] <= df['Reorder_Point'], 'REORDER NOW', 'STABLE')

    # 5. ABC ANALYSIS (Inventory Prioritization)
    # Categorizing based on Annual Consumption Value
    df['Annual_Value'] = df['Daily_Demand_Mean'] * 365 * df['Unit_Cost']
    df = df.sort_values(by='Annual_Value', ascending=False)
    df['Cumulative_Value_Share'] = df['Annual_Value'].cumsum() / df['Annual_Value'].sum()

    def classify_abc(share):
        if share <= 0.7: return 'A (High Value)'
        if share <= 0.9: return 'B (Medium Value)'
        return 'C (Low Value)'

    df['ABC_Category'] = df['Cumulative_Value_Share'].apply(classify_abc)
    return df

if __name__ == "__main__":
    # Main execution flow
    inventory_df = load_data()
    results = optimize_inventory(inventory_df)
    
    # Save results to CSV for Power BI visualization
    results.to_csv('inventory_optimization_results.csv', index=False)
    
    print("--- Inventory Optimization Report ---")
    print(results[['Product_ID', 'Status', 'ABC_Category', 'Reorder_Point']])
    print("\nResults saved to 'inventory_optimization_results.csv' for Dashboarding.")
