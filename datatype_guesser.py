# datatype_guesser.py

from fuzzywuzzy import process
import pandas as pd
import re
import numpy as np

# Define the possible categories for files and data columns
FILE_CATEGORIES = ['Collar', 'Survey', 'Point', 'Interval']
COLUMN_DATATYPES = ['Text', 'Category', 'Numeric', 'Datetime', 'Boolean']
REQUIRED_COLUMNS = {
    'Collar': ['HoleID', 'DH_X', 'DH_Y', 'DH_Z', 'Depth'],
    'Survey': ['HoleID', 'Depth', 'Dip', 'Azimuth'],
    'Point': ['HoleID', 'Depth'],
    'Interval': ['HoleID', 'From', 'To']
}

# Define common variations for each mandatory field
MANDATORY_FIELD_VARIATIONS = {
    'HoleID': ['holeid', 'hole_id', 'id', 'hole', 'bhid', 'bh_id', 'dh_id', 'dhid'],
    'DH_X': ['dh_x', 'x', 'easting', 'longitude', 'east', 'lon', 'long'],
    'DH_Y': ['dh_y', 'y', 'northing', 'latitude', 'north', 'lat'],
    'DH_Z': ['dh_z', 'z', 'elevation', 'depth_start', 'start_depth', 'elev', 'rl'],
    'Depth': ['depth', 'total_depth', 'end_depth', 'td', 'eoh'],
    'Dip': ['dip', 'inclination', 'incl'],
    'Azimuth': ['azimuth', 'bearing', 'direction', 'azi'],
    'From': ['from', 'start_depth', 'depth_from', 'top'],
    'To': ['to', 'end_depth', 'depth_to', 'bottom']
}

def normalize_string(s):
    """Normalize string by removing non-alphanumeric characters and converting to lowercase."""
    return re.sub(r'\W+', '', s).lower()

def guess_file_type(file_name):
    """Guess the file type based on the file name."""
    normalized_name = normalize_string(file_name)
    best_guess, score = process.extractOne(normalized_name, FILE_CATEGORIES, scorer=process.fuzz.partial_ratio)
    return best_guess if score > 60 else 'Collar'

def is_numeric(column_data):
    """Check if a column is numeric."""
    try:
        pd.to_numeric(column_data, errors='raise')
        return True
    except ValueError:
        return False

def guess_column_type(file_type, column_name, column_data):
    """Guess the column type based on the file type, column name, and column data."""
    normalized_name = normalize_string(column_name)
    mandatory_fields = REQUIRED_COLUMNS.get(file_type, [])
    
    # Check for mandatory fields first
    for field in mandatory_fields:
        if any(variation in normalized_name for variation in MANDATORY_FIELD_VARIATIONS.get(field, [])):
            return field

    # Check for numeric columns (including those with some non-numeric values)
    if is_numeric(column_data) or (column_data.dtype == 'object' and column_data.str.isnumeric().mean() > 0.8):
        return 'Numeric'

    # Check for datetime columns
    if 'date' in normalized_name or pd.api.types.is_datetime64_any_dtype(column_data):
        return 'Datetime'
    
    # Check for boolean columns
    if set(column_data.dropna().unique()) <= {True, False, 1, 0, 'True', 'False', 'true', 'false', 'TRUE', 'FALSE', 'T', 'F', 'Y', 'N'}:
        return 'Boolean'
    
    # Check for categorical columns
    unique_ratio = column_data.nunique() / len(column_data)
    if unique_ratio < 0.1:  # If less than 10% of values are unique
        return 'Category'
    
    # Default to Text for any other case
    return 'Text'

def guess_type(type_name, name, column_data=None):
    """Guess the type based on the type name and name."""
    if type_name.lower() == 'file':
        return guess_file_type(name)
    elif type_name.lower() == 'datacolumn':
        if column_data is None:
            raise ValueError("column_data must be provided for type 'datacolumn'")
        file_type, column_name = name.split('_', 1)
        return guess_column_type(file_type, column_name, column_data)
    else:
        raise ValueError("Invalid type name. Use 'file' or 'datacolumn'.")

# Example usage
if __name__ == "__main__":
    print(guess_type('file', 'my_collars.csv'))  # Should return 'Collar'
    print(guess_type('datacolumn', 'Collar_HoleID', pd.Series(['A', 'B', 'C'])))  # Should return 'HoleID'
    print(guess_type('datacolumn', 'Survey_Depth', pd.Series([10, 20, 30])))  # Should return 'Depth'
    print(guess_type('datacolumn', 'Interval_From', pd.Series([10, 90, 180])))  # Should return 'From'