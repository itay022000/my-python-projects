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

def create_customer_data():
    """Create a customer dataset."""
    np.random.seed(42)
    random.seed(42)
    
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
              'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
    states = ['NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'TX', 'CA', 'TX', 'CA']
    
    data = {
        'customer_id': range(1, 201),
        'customer_name': [f'Customer_{i}' for i in range(1, 201)],
        'email': [f'customer{i}@email.com' for i in range(1, 201)],
        'city': np.random.choice(cities, 200),
        'state': np.random.choice(states, 200),
        'age': np.random.randint(18, 80, 200),
        'membership_tier': np.random.choice(['Bronze', 'Silver', 'Gold', 'Platinum'], 200, 
                                           p=[0.4, 0.3, 0.2, 0.1]),
        'join_date': [(datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1095))).strftime('%Y-%m-%d') 
                      for _ in range(200)]
    }
    
    return pd.DataFrame(data)

def create_messy_data():
    """Create a messy dataset for cleaning practice."""
    np.random.seed(42)
    random.seed(42)
    
    n_rows = 106
    # Create data with intentional issues
    data = {
        'id': list(range(1, 101)) + [None] * 5,  # Missing values (105 items, need 106)
        'name': [f'Product_{i}' if i % 10 != 0 else None for i in range(1, n_rows + 1)],  # Some missing
        'price': [f'${np.random.uniform(10, 100):.2f}' if i % 7 != 0 else None for i in range(1, n_rows + 1)],  # String prices, some missing
        'quantity': list(np.random.randint(0, 100, 100)) + [None] * 5 + [9999],  # Outlier (106 items)
        'category': np.random.choice(['A', 'B', 'C', None, 'D'], n_rows),  # Missing values
        'date': [(datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d') 
                 if i % 8 != 0 else 'invalid_date' for i in range(1, n_rows + 1)],
        'rating': [f'{np.random.uniform(1, 5):.1f}' if i % 6 != 0 else None for i in range(1, n_rows + 1)]  # String numbers
    }
    
    # Fix id column to have 106 items
    data['id'] = list(range(1, 101)) + [None] * 6
    
    df = pd.DataFrame(data)
    
    # Add some duplicates
    df = pd.concat([df, df.iloc[:3]], ignore_index=True)
    
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
    
    # Create customer data
    customer_df = create_customer_data()
    customer_df.to_csv(data_dir / "customer_data.csv", index=False)
    print(f"✅ Created customer_data.csv ({customer_df.shape[0]} rows)")
    
    # Create messy data
    messy_df = create_messy_data()
    messy_df.to_csv(data_dir / "messy_data.csv", index=False)
    print(f"✅ Created messy_data.csv ({messy_df.shape[0]} rows)")
    
    print("\n🎉 All datasets created successfully!")
    print("You can now run main.py to start practicing pandas!")

if __name__ == "__main__":
    main()

