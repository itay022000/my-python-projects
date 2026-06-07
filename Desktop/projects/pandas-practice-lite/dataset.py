"""Dataset loading and column helpers mixin."""

import random

import pandas as pd


class DatasetMixin:
    """Mixin for PandasPractice."""

    def load_dataset(self, filename, *, verbose=True):
        """Load a dataset from the data directory."""
        filepath = self.data_dir / filename
        if not filepath.exists():
            print(f"❌ Dataset '{filename}' not found!")
            return None

        if self.current_dataset_name == filename and self.current_dataset is not None:
            return self.current_dataset

        try:
            df = pd.read_csv(filepath)
            self.current_dataset = df
            self.current_dataset_name = filename
            self.save_progress()
            if verbose:
                print(f"✅ Loaded dataset: {filename}")
                print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns")
            return df
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            return None
    def get_numeric_columns(self, df=None):
        """Get numeric columns from dataframe."""
        if df is None:
            df = self.current_dataset
        if df is None:
            return []
        return df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    def get_categorical_columns(self, df=None):
        """Get categorical/object columns from dataframe."""
        if df is None:
            df = self.current_dataset
        if df is None:
            return []
        return df.select_dtypes(include=['object', 'string']).columns.tolist()
    def get_random_numeric_column(self, df=None):
        """Get a random numeric column."""
        cols = self.get_numeric_columns(df)
        return random.choice(cols) if cols else None
    def get_random_categorical_column(self, df=None):
        """Get a random categorical column."""
        cols = self.get_categorical_columns(df)
        return random.choice(cols) if cols else None
    def get_random_column(self, df=None):
        """Get a random column of any type."""
        if df is None:
            df = self.current_dataset
        if df is None:
            return None
        return random.choice(df.columns.tolist())
    def get_random_value_from_column(self, column, df=None):
        """Get a random value from a column."""
        if df is None:
            df = self.current_dataset
        if df is None or column not in df.columns:
            return None
        values = df[column].dropna().unique()
        return random.choice(values) if len(values) > 0 else None
    def get_random_threshold(self, column, df=None, percentile=50):
        """Get a random threshold value from a numeric column."""
        if df is None:
            df = self.current_dataset
        if df is None or column not in df.columns:
            return None
        if df[column].dtype not in ['int64', 'float64']:
            return None
        return df[column].quantile(percentile / 100.0)
    def check_dataset_loaded(self):
        """Check if a dataset is loaded, prompt to load one if not."""
        if self.current_dataset is None:
            print("\n❌ No dataset loaded!")
            print("💡 The dataset should be automatically loaded. Please restart the program.")
            return False
        return True
