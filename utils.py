import pandas as pd

class File:
    def __init__(self, name, df, category, columns=[], columns_dtypes=[], required_cols={}, simplified_dtypes={}, user_defined_dtypes={}, df_reassigned_dtypes={}):
        self.name = name
        self.df = df
        self.category = category
        self.columns = columns
        self.columns_dtypes = columns_dtypes
        self.required_cols = required_cols
        self.simplified_dtypes = simplified_dtypes
        self.user_defined_dtypes = user_defined_dtypes
        self.df_reassigned_dtypes = df_reassigned_dtypes

def required_cols(file):
    required_cols_dict = {
        "Collar": ["HoleID", "DH_X", "DH_Y", "DH_Z", "Depth"],
        "Survey": ["HoleID", "Depth", "Dip", "Azimuth"],
        "Point": ["HoleID", "Depth"],
        "Interval": ["HoleID", "From", "To"]
    }
    return {col: None for col in required_cols_dict.get(file.category, [])}

def simplify_dtypes(df):
    dtypes = {}
    for col in df.columns:
        if pd.api.types.is_string_dtype(df[col]):
            dtypes[col] = "Text"
        elif pd.api.types.is_categorical_dtype(df[col]):
            dtypes[col] = "Category"
        elif pd.api.types.is_numeric_dtype(df[col]):
            dtypes[col] = "Numeric"
        elif pd.api.types.is_datetime64_dtype(df[col]):
            dtypes[col] = "Datetime"
        elif pd.api.types.is_bool_dtype(df[col]):
            dtypes[col] = "Boolean"
        else:
            dtypes[col] = "Other"
    return dtypes

def get_file_extension(filename):
    return filename.split('.')[-1].lower()

def is_valid_file_type(filename, allowed_extensions):
    return get_file_extension(filename) in allowed_extensions

def format_bytes(size):
    # Convert bytes to human-readable format
    power = 2**10
    n = 0
    units = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power:
        size /= power
        n += 1
    return f"{size:.2f} {units[n]}"

def validate_dataframe(df, required_cols):
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        return False, f"Missing required columns: {', '.join(missing_cols)}"
    return True, "Dataframe is valid"

def get_unique_values(df, column):
    return df[column].unique().tolist()

def get_column_stats(df, column):
    stats = {
        "count": df[column].count(),
        "unique": df[column].nunique(),
        "top": df[column].mode().iloc[0] if not df[column].empty else None,
        "freq": df[column].value_counts().iloc[0] if not df[column].empty else None,
    }
    
    if pd.api.types.is_numeric_dtype(df[column]):
        stats.update({
            "mean": df[column].mean(),
            "std": df[column].std(),
            "min": df[column].min(),
            "25%": df[column].quantile(0.25),
            "50%": df[column].median(),
            "75%": df[column].quantile(0.75),
            "max": df[column].max()
        })
    
    return stats

def merge_dataframes(df1, df2, on, how='inner'):
    return pd.merge(df1, df2, on=on, how=how)

def filter_dataframe(df, conditions):
    for column, condition in conditions.items():
        if condition:
            df = df[df[column] == condition]
    return df

def sort_dataframe(df, columns, ascending=True):
    return df.sort_values(columns, ascending=ascending)

def group_and_aggregate(df, group_by, agg_dict):
    return df.groupby(group_by).agg(agg_dict)

def pivot_table(df, values, index, columns, aggfunc):
    return pd.pivot_table(df, values=values, index=index, columns=columns, aggfunc=aggfunc)

def resample_time_series(df, time_column, freq, agg_dict):
    df[time_column] = pd.to_datetime(df[time_column])
    df = df.set_index(time_column)
    return df.resample(freq).agg(agg_dict).reset_index()