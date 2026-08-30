"""Dataset loading and column helpers mixin."""

import random
import sys

import env_quiet  # noqa: F401 — before pandas

import pandas as pd


class DatasetMixin:
    """Mixin for PandasPractice."""

    DATASET_FILE = "sales_data.csv"

    def ensure_dataset_loaded(self) -> bool:
        """Load sales_data.csv at startup; fail fast on error (B011)."""
        filepath = self.data_dir / self.DATASET_FILE
        if not filepath.exists():
            print(
                f"Could not load {self.DATASET_FILE}. "
                f"Check that data/{self.DATASET_FILE} exists."
            )
            return False
        try:
            df = pd.read_csv(filepath)
            self.current_dataset = df
            self.current_dataset_name = self.DATASET_FILE
            return True
        except Exception as exc:
            print(f"Error loading {self.DATASET_FILE}: {exc}")
            return False

    def fail_fast_if_no_dataset(self) -> None:
        if not self.ensure_dataset_loaded():
            sys.exit(1)

    def get_numeric_columns(self, df=None):
        if df is None:
            df = self.current_dataset
        if df is None:
            return []
        return df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    def get_categorical_columns(self, df=None):
        if df is None:
            df = self.current_dataset
        if df is None:
            return []
        return df.select_dtypes(include=["object", "string"]).columns.tolist()

    def get_random_numeric_column(self, df=None):
        cols = self.get_numeric_columns(df)
        return random.choice(cols) if cols else None

    def get_categorical_column(self, df=None):
        cols = self.get_categorical_columns(df)
        return random.choice(cols) if cols else None

    def get_random_categorical_column(self, df=None):
        return self.get_categorical_column(df)

    def get_random_column(self, df=None):
        if df is None:
            df = self.current_dataset
        if df is None:
            return None
        return random.choice(df.columns.tolist())

    def get_random_value_from_column(self, column, df=None):
        if df is None:
            df = self.current_dataset
        if df is None or column not in df.columns:
            return None
        values = df[column].dropna().unique()
        return random.choice(values) if len(values) > 0 else None

    def get_random_threshold(self, column, df=None, percentile=50):
        if df is None:
            df = self.current_dataset
        if df is None or column not in df.columns:
            return None
        if df[column].dtype not in ["int64", "float64"]:
            return None
        return df[column].quantile(percentile / 100.0)
