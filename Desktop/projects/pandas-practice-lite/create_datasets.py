"""
Script to generate sample datasets for pandas practice.
Run this once to create the practice datasets.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import random

def create_sales_data():
    """Create a sales dataset."""
    np.random.seed(42)
    random.seed(42)
    
    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones', 
                'Webcam', 'Speaker', 'Tablet', 'Phone', 'Charger']
    categories = ['Electronics', 'Accessories', 'Computers', 'Audio']
    
    dates = []
    start_date = datetime(2023, 1, 1)
    for i in range(1000):
        dates.append(start_date + timedelta(days=random.randint(0, 365)))
    
    data = {
        'sale_id': range(1, 1001),
        'date': [d.strftime('%Y-%m-%d') for d in dates],
        'customer_id': np.random.randint(1, 201, 1000),
        'product': np.random.choice(products, 1000),
        'category': np.random.choice(categories, 1000),
        'quantity': np.random.randint(1, 11, 1000),
        'unit_price': np.round(np.random.uniform(10, 500, 1000), 2),
        'sales_rep': np.random.choice(['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'], 1000)
    }
    
    df = pd.DataFrame(data)
    df['total_sales'] = df['quantity'] * df['unit_price']
    
    return df

def main():
    """Generate all datasets."""
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    print("Creating sample datasets...")
    
    # Create sales data
    sales_df = create_sales_data()
    sales_df.to_csv(data_dir / "sales_data.csv", index=False)
    print(f"✅ Created sales_data.csv ({sales_df.shape[0]} rows)")
    
    print("\n🎉 All datasets created successfully!")
    print("You can now run main.py to start practicing pandas!")

if __name__ == "__main__":
    main()

