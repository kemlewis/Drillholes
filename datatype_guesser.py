from fuzzywuzzy import process
import pandas as pd
import re

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
    """
    Guess the file type based on the file name.
    
    Parameters:
    file_name (str): The name of the file to guess the type for.
    
    Returns:
    str: The best guess for the file type.
    """
    normalized_name = normalize_string(file_name)
    best_guess, score = process.extractOne(normalized_name, FILE_CATEGORIES, scorer=process.fuzz.partial_ratio)
    
    # If the score is too low, default to 'Collar' as it's the most common type
    return best_guess if score > 60 else 'Collar'

def guess_column_type(file_type, column_name, column_data):
    """
    Guess the column type based on the file type, column name, and column data.
    
    Parameters:
    file_type (str): The type of the file.
    column_name (str): The name of the column to guess the type for.
    column_data (pd.Series): The data of the column.
    
    Returns:
    str: The best guess for the column type.
    """
    normalized_name = normalize_string(column_name)
    mandatory_fields = REQUIRED_COLUMNS.get(file_type, [])
    
    # Check for mandatory fields first
    for field in mandatory_fields:
        if any(variation in normalized_name for variation in MANDATORY_FIELD_VARIATIONS.get(field, [])):
            return field

    # Check for datetime columns
    if 'date' in normalized_name or pd.api.types.is_datetime64_any_dtype(column_data):
        return 'Datetime'
    
    # Check for boolean columns
    if set(column_data.dropna().unique()) <= {True, False, 1, 0, 'True', 'False', 'true', 'false', 'TRUE', 'FALSE', 'T', 'F', 'Y', 'N'}:
        return 'Boolean'
    
    # Check for numeric columns
    if pd.api.types.is_numeric_dtype(column_data):
        return 'Numeric'
    
    # Check for categorical columns
    unique_ratio = column_data.nunique() / len(column_data)
    if unique_ratio < 0.1:  # If less than 10% of values are unique
        return 'Category'
    
    # Default to Text for any other case
    return 'Text'

def guess_type(type_name, name, column_data=None):
    """
    Guess the type based on the type name and name.
    
    Parameters:
    type_name (str): The type name ("file" or "datacolumn").
    name (str): The name to guess the type for.
    column_data (pd.Series, optional): The data of the column if guessing a datacolumn type.
    
    Returns:
    str: The best guess for the type.
    """
    if type_name.lower() == 'file':
        return guess_file_type(name)
    elif type_name.lower() == 'datacolumn':
        if column_data is None:
            raise ValueError("column_data must be provided for type 'datacolumn'")
        file_type = name.split('_')[0]
        return guess_column_type(file_type, name.split('_', 1)[-1], column_data)
    else:
        raise ValueError("Invalid type name. Use 'file' or 'datacolumn'.")

# Example usage
if __name__ == "__main__":
    print(guess_type('file', 'my_collars.csv'))  # Should return 'Collar'
    print(guess_type('datacolumn', 'Collar_HoleID', pd.Series(['A', 'B', 'C'])))  # Should return 'HoleID'
    print(guess_type('datacolumn', 'Survey_Depth', pd.Series([10, 20, 30])))  # Should return 'Depth'
    print(guess_type('datacolumn', 'Interval_From', pd.Series([10, 90, 180])))  # Should return 'From'