"""Pandas code execution and result validators (sales_data.csv practice app)."""

import pandas as pd


def is_valid_pandas_code(code):
    """Check if the code is actually pandas code, not just a literal value."""
    code_stripped = code.strip()

    try:
        float(code_stripped)
        return False, "Please enter pandas code, not just a number"
    except ValueError:
        pass

    if (code_stripped.startswith('"') and code_stripped.endswith('"')) or (
        code_stripped.startswith("'") and code_stripped.endswith("'")
    ):
        return False, "Please enter pandas code, not just a string"

    if code_stripped.lower() in ['true', 'false']:
        return False, "Please enter pandas code, not just a boolean"

    if code_stripped.lower() == 'none':
        return False, "Please enter pandas code, not just None"

    if 'df' not in code_stripped and 'pd' not in code_stripped:
        if not any(keyword in code_stripped for keyword in ['print', 'len', 'type', 'isinstance']):
            return False, "Please enter pandas code that uses 'df' or 'pd'"

    return True, None


def execute_pandas_code(df, code, expected_result=None, description="", include_plotting=False):
    """Execute pandas code and return (result, error)."""
    try:
        safe_dict = {"df": df, "pd": pd}
        if include_plotting:
            import matplotlib.pyplot as plt
            import matplotlib
            matplotlib.use('Agg')
            safe_dict["plt"] = plt
            safe_dict["matplotlib"] = matplotlib

        code_stripped = code.strip()
        has_equals = '=' in code_stripped

        if has_equals:
            temp_code = code_stripped.replace('==', 'XX').replace('!=', 'XX').replace('<=', 'XX').replace('>=', 'XX')
            has_standalone_equals = '=' in temp_code
            looks_like_assignment = has_standalone_equals and ('df[' in code_stripped or 'df.' in code_stripped)
            is_assignment = looks_like_assignment
        else:
            is_assignment = False

        if is_assignment:
            df_copy = df.copy()
            safe_dict_copy = {"df": df_copy, "pd": pd}
            if include_plotting:
                safe_dict_copy["plt"] = safe_dict.get("plt")
                safe_dict_copy["matplotlib"] = safe_dict.get("matplotlib")
            exec(code, {"__builtins__": {}}, safe_dict_copy)
            return None, None

        result = eval(code, {"__builtins__": {}}, safe_dict)
        return result, None
    except Exception as e:
        return None, str(e)


def validate_head_result(result, df, n=10):
    """Validate that result shows first n rows."""
    if not hasattr(result, 'shape'):
        return False, "Result is not a DataFrame"
    expected_rows = min(n, df.shape[0])
    if result.shape[0] != expected_rows:
        return False, f"Expected {expected_rows} rows, got {result.shape[0]}"
    try:
        if not result.iloc[0].equals(df.iloc[0]):
            return False, "First row doesn't match - this might not be the head"
        if result.shape[0] > 1:
            expected_last_idx = min(n - 1, df.shape[0] - 1)
            if not result.iloc[-1].equals(df.iloc[expected_last_idx]):
                return False, "Rows don't match - this might not be the head"
        if not all(result.columns == df.columns):
            return False, "Column names don't match"
    except Exception as e:
        return False, f"Error validating: {str(e)}"
    return True, "Correct! You displayed the first rows correctly."


def validate_shape_result(result, df):
    """Validate that result is the shape tuple."""
    if result == df.shape:
        return True, "Correct!"
    return False, f"Expected {df.shape}, got {result}"


def validate_columns_result(result, df):
    """Validate that result contains column names."""
    try:
        if hasattr(result, 'tolist'):
            result_list = result.tolist()
        elif hasattr(result, 'values'):
            result_list = list(result.values)
        elif isinstance(result, (list, tuple)):
            result_list = list(result)
        elif hasattr(result, '__iter__') and not isinstance(result, str):
            result_list = list(result)
        else:
            return False, "Result is not a list or array of column names"

        expected = list(df.columns)
        if set(result_list) == set(expected) and len(result_list) == len(expected):
            return True, "Correct! You got all the column names."
        elif len(result_list) != len(expected):
            return False, f"Expected {len(expected)} columns, got {len(result_list)}"
        else:
            missing = set(expected) - set(result_list)
            extra = set(result_list) - set(expected)
            if missing:
                return False, f"Missing columns: {missing}"
            if extra:
                return False, f"Extra columns that don't exist: {extra}"
            return False, "Column names don't match"
    except Exception as e:
        return False, f"Error validating: {str(e)}"


def validate_filter_result(result, df, condition_check):
    """Validate filtering result."""
    if not hasattr(result, 'shape'):
        return False, "Result is not a DataFrame"
    return True, "Result looks like filtered data"


def validate_filter_greater_than(result, df, column, threshold):
    """Validate that filter result contains only rows where column > threshold."""
    if not hasattr(result, 'shape'):
        return False, "Result is not a DataFrame"
    if column not in result.columns:
        return False, f"Column '{column}' not found in result"

    expected = df[df[column] > threshold]
    expected_count = len(expected)

    if len(result) == 0:
        if expected_count == 0:
            return True, "Correct! No rows satisfy the condition."
        return False, f"Result is empty, but {expected_count} rows should satisfy the condition"

    if not (result[column] > threshold).all():
        invalid_count = (result[column] <= threshold).sum()
        return False, f"{invalid_count} rows don't satisfy the condition (should be > {threshold})"

    if len(result) != expected_count:
        return False, f"Expected {expected_count} rows, got {len(result)}. You might be missing some rows or have extra ones."

    try:
        result_indices = set(result.index)
        expected_indices = set(expected.index)
        if result_indices != expected_indices:
            missing = expected_indices - result_indices
            extra = result_indices - expected_indices
            if missing:
                return False, f"Missing {len(missing)} rows that should be included"
            if extra:
                return False, f"Have {len(extra)} extra rows that shouldn't be included"
    except Exception:
        pass

    return True, f"Correct! All {len(result)} rows satisfy the condition."


def validate_groupby_sum(result, df, group_col, agg_col):
    """Validate groupby sum result."""
    if not hasattr(result, '__iter__'):
        return False, "Result should be a Series or DataFrame"

    try:
        expected = df.groupby(group_col)[agg_col].sum()
    except Exception as e:
        return False, f"Error calculating expected result: {str(e)}"

    try:
        if getattr(result, 'ndim', 1) > 1 and result.shape[1] > 1:
            if agg_col in result.columns:
                result_series = result[agg_col]
            elif len(result.columns) == 1:
                result_series = result.iloc[:, 0]
            else:
                return False, "Result is a DataFrame with multiple columns - should be a Series or single column"
        elif hasattr(result, 'values'):
            result_series = result
        else:
            return False, "Result format not recognized"

        if len(result_series) != len(expected):
            return False, f"Expected {len(expected)} groups, got {len(result_series)}"

        if not all(result_series.index == expected.index):
            missing = set(expected.index) - set(result_series.index)
            extra = set(result_series.index) - set(expected.index)
            if missing:
                return False, f"Missing groups: {missing}"
            if extra:
                return False, f"Extra groups: {extra}"
            return False, "Group indices don't match"

        if hasattr(result_series, 'values') and hasattr(expected, 'values'):
            differences = abs(result_series.values - expected.values)
            max_diff = differences.max()
            if max_diff > 0.01:
                return False, f"Values don't match. Max difference: {max_diff:.4f}"

            if hasattr(result_series, 'equals'):
                if result_series.equals(expected):
                    return True, "Correct! Groupby sum is accurate."

            return True, "Correct! Groupby sum is accurate."
        return False, "Could not compare values"
    except Exception as e:
        return False, f"Error validating: {str(e)}"


def validate_merge_result(result, df1, df2, on_col):
    """Validate merge result."""
    if not hasattr(result, 'shape'):
        return False, "Result is not a DataFrame"
    if on_col not in result.columns:
        return False, f"Merge column '{on_col}' not found in result"

    df1_cols = set(df1.columns)
    df2_cols = set(df2.columns)
    result_cols = set(result.columns)

    if not (df1_cols.issubset(result_cols) or df2_cols.issubset(result_cols)):
        df1_cols_in_result = df1_cols.intersection(result_cols)
        df2_cols_in_result = df2_cols.intersection(result_cols)
        if len(df1_cols_in_result) == 0 or len(df2_cols_in_result) == 0:
            return False, "Merged dataframe should have columns from both original dataframes"

    if on_col in df1.columns and on_col in df2.columns:
        result_values = set(result[on_col].unique())
        df1_values = set(df1[on_col].unique())
        df2_values = set(df2[on_col].unique())
        valid_values = df1_values.union(df2_values)
        invalid = result_values - valid_values
        if invalid:
            return False, f"Merge column contains values not in either original: {list(invalid)[:5]}"

    max_possible = len(df1) * len(df2)
    if result.shape[0] > max_possible:
        return False, f"Result has {result.shape[0]} rows, which is more than possible"

    return True, "Correct! Merge was performed successfully."


def validate_drop_duplicates(result, df):
    """Validate drop_duplicates result."""
    if not hasattr(result, 'shape'):
        return False, "Result is not a DataFrame"
    if result.shape[0] > df.shape[0]:
        return False, "Result has more rows than original - duplicates weren't removed"

    original_dupes = df.duplicated().sum()
    removed = df.shape[0] - result.shape[0]

    if removed > original_dupes:
        return False, f"Removed {removed} rows, but only {original_dupes} duplicates exist"

    result_dupes = result.duplicated().sum()
    if result_dupes > 0:
        return False, f"Result still has {result_dupes} duplicate rows"

    try:
        if result.shape[1] != df.shape[1]:
            return False, "Column count doesn't match - result might be modified incorrectly"

        original_unique = df.drop_duplicates()
        if result.shape[0] < original_unique.shape[0]:
            return False, f"Removed {original_unique.shape[0] - result.shape[0]} unique rows that shouldn't have been removed"
    except Exception:
        pass

    return True, f"Correct! Removed {removed} duplicate row(s)."


def validate_handle_missing(result, df, method='fill', fill_value=None):
    """Validate missing value handling."""
    if not hasattr(result, 'shape'):
        return False, "Result is not a DataFrame"

    missing_after = result.isnull().sum().sum()
    missing_before = df.isnull().sum().sum()

    if method == 'drop':
        if missing_after >= missing_before:
            return False, f"Missing values weren't removed (had {missing_before}, still have {missing_after})"
        if result.shape[0] >= df.shape[0]:
            return False, "No rows were removed - did you use dropna()?"
        cols_with_missing = df.columns[df.isnull().any()].tolist()
        if cols_with_missing:
            remaining_missing = result[cols_with_missing].isnull().sum().sum()
            if remaining_missing > 0:
                return False, f"Still have {remaining_missing} missing values in columns that had them"
        return True, f"Correct! Removed rows with missing values. ({missing_before - missing_after} missing values removed)"

    if method == 'fill':
        if missing_after >= missing_before:
            return False, f"Missing values weren't filled (had {missing_before}, still have {missing_after})"
        if result.shape[0] != df.shape[0]:
            return False, "Row count changed - fillna() should keep all rows"
        if fill_value is not None:
            cols_with_missing = df.columns[df.isnull().any()].tolist()
            for col in cols_with_missing:
                if df[col].isnull().any():
                    filled_indices = df[df[col].isnull()].index
                    if len(filled_indices) > 0:
                        filled_values = result.loc[filled_indices, col]
                        if not (filled_values == fill_value).all():
                            return False, f"Fill value incorrect! Expected all missing values to be filled with {fill_value}"
            return True, f"Correct! Filled missing values with {fill_value}. ({missing_before - missing_after} values filled)"
        return True, f"Correct! Filled missing values. ({missing_before - missing_after} values filled)"

    return True, "Result looks good!"
