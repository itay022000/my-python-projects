# 🐼 Pandas Practice - Interactive Learning Tool

A hands-on Python project designed to help you learn and practice pandas through interactive exercises and real-world data analysis scenarios.

## 📚 What You'll Learn

This project covers essential pandas concepts:

- **Basic Operations**: Loading data, viewing datasets, understanding structure
- **Data Filtering**: Boolean indexing, conditional selection
- **Grouping & Aggregation**: GroupBy operations, aggregations
- **Data Merging**: Combining multiple DataFrames
- **Data Cleaning**: Handling missing values, duplicates, data types

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or navigate to this directory:**
   ```bash
   cd pandas-practice
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate sample datasets:**
   ```bash
   python create_datasets.py
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

## 📊 Features

### Interactive Dataset Exploration
- Load and explore CSV datasets
- View data statistics and information
- Filter, sort, and group data interactively
- Practice pandas operations in real-time

### Guided Exercises
- **Exercise 1**: Basic Operations - Learn fundamental pandas commands
- **Exercise 2**: Filtering Data - Master boolean indexing and conditional selection
- **Exercise 3**: Grouping & Aggregation - Understand GroupBy operations
- **Exercise 4**: Merging DataFrames - Combine multiple datasets
- **Exercise 5**: Data Cleaning - Handle real-world data issues

### Progress Tracking
- Track completed exercises
- Monitor datasets explored
- View learning statistics

## 📁 Project Structure

```
pandas-practice/
├── main.py                 # Main application
├── create_datasets.py      # Script to generate sample data
├── requirements.txt        # Python dependencies
├── progress.json          # Your learning progress (auto-generated)
├── data/                  # Sample datasets
│   ├── sales_data.csv     # Sales transactions dataset
│   ├── customer_data.csv  # Customer information dataset
│   └── messy_data.csv     # Dataset with data quality issues
└── README.md              # This file
```

## 📖 Sample Datasets

### sales_data.csv
- **Rows**: 1,000 sales transactions
- **Columns**: sale_id, date, customer_id, product, category, quantity, unit_price, total_sales, sales_rep
- **Use Cases**: Filtering, grouping, aggregations

### customer_data.csv
- **Rows**: 200 customers
- **Columns**: customer_id, customer_name, email, city, state, age, membership_tier, join_date
- **Use Cases**: Merging with sales data, customer analysis

### messy_data.csv
- **Rows**: 109 (with intentional issues)
- **Issues**: Missing values, duplicates, wrong data types, outliers, invalid dates
- **Use Cases**: Data cleaning practice

## 🎯 How to Use

1. **Start the application:**
   ```bash
   python main.py
   ```

2. **Main Menu Options:**
   - **Load Dataset**: Choose a dataset to work with
   - **Explore Current Dataset**: Interactive exploration menu
   - **Run Exercise**: Follow guided exercises
   - **View Learning Statistics**: Track your progress
   - **Exit**: Save progress and exit

3. **Exploration Menu Features:**
   - View head/tail of data
   - Get dataset info and statistics
   - Check for missing values
   - Filter by conditions
   - Group and aggregate
   - Sort data

## 💡 Learning Tips

1. **Start with Basic Operations**: Get comfortable with loading and viewing data
2. **Practice Filtering**: Try different conditions and see the results
3. **Experiment with GroupBy**: Understand how grouping works with different aggregations
4. **Master Merging**: Practice different merge types (inner, left, right, outer)
5. **Clean Real Data**: The messy_data.csv will challenge your cleaning skills

## 🔧 Customization

### Add Your Own Datasets
1. Place CSV files in the `data/` directory
2. Load them through the "Load Dataset" menu option
3. Explore and practice with your own data!

### Create New Exercises
Edit `main.py` and add new exercise methods following the existing pattern:
```python
def exercise_6_your_topic(self):
    """Your exercise description."""
    # Your exercise code here
```

## 📝 Example Pandas Operations

Here are some operations you'll practice:

```python
# Load data
df = pd.read_csv('data/sales_data.csv')

# View first rows
df.head()

# Filter data
df[df['total_sales'] > 1000]

# Group and aggregate
df.groupby('category')['total_sales'].sum()

# Merge dataframes
pd.merge(sales_df, customer_df, on='customer_id')

# Handle missing values
df.dropna()
df.fillna(0)
```

## 🎓 Next Steps

After completing the exercises:
1. Try analyzing your own datasets
2. Explore more pandas functions (pivot tables, time series, etc.)
3. Combine pandas with visualization libraries (matplotlib, seaborn)
4. Practice on real-world datasets from Kaggle or other sources

## 📚 Additional Resources

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [10 Minutes to Pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- [Pandas Tutorials](https://pandas.pydata.org/docs/getting_started/intro_tutorials/)

## 🤝 Contributing

Feel free to:
- Add more exercises
- Improve existing features
- Add new sample datasets
- Enhance documentation

## 📄 License

This is a learning project - feel free to use and modify as needed!

---

**Happy Learning! 🐼📊**

*Remember: The best way to learn pandas is by doing. Practice regularly and experiment with different operations!*

