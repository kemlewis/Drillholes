from fuzzywuzzy import process
import pandas as pd

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
    'HoleID': ['HoleID', 'Hole_ID', 'ID', 'Hole'],
    'DH_X': ['DH_X', 'X', 'Easting', 'Longitude'],
    'DH_Y': ['DH_Y', 'Y', 'Northing', 'Latitude'],
    'DH_Z': ['DH_Z', 'Z', 'Elevation', 'Depth_Start', 'Start_Depth'],
    'Depth': ['Depth', 'Total_Depth', 'End_Depth', 'TD'],
    'Dip': ['Dip', 'Inclination'],
    'Azimuth': ['Azimuth', 'Bearing', 'Direction'],
    'From': ['From', 'Start_Depth', 'Depth_From'],
    'To': ['To', 'End_Depth', 'Depth_To']
}

def guess_file_type(file_name):
    """
    Guess the file type based on the file name.
    
    Parameters:
    file_name (str): The name of the file to guess the type for.
    
    Returns:
    str: The best guess for the file type.
    """
    best_guess, _ = process.extractOne(file_name, FILE_CATEGORIES)
    return best_guess

def guess_column_type(file_type, column_name, column_data):
    """
    Guess the column type based on the file type and column name.
    
    Parameters:
    file_type (str): The type of the file.
    column_name (str): The name of the column to guess the type for.
    column_data (pd.Series): The data of the column.
    
    Returns:
    str: The best guess for the column type.
    """
    mandatory_fields = REQUIRED_COLUMNS.get(file_type, [])
    all_mandatory_variations = [variation for field in mandatory_fields for variation in MANDATORY_FIELD_VARIATIONS.get(field, [])]
    best_guess, _ = process.extractOne(column_name, all_mandatory_variations + COLUMN_DATATYPES)

    if best_guess in all_mandatory_variations:
        return next((field for field in mandatory_fields if best_guess in MANDATORY_FIELD_VARIATIONS.get(field, [])), 'Text')
    
    # Additional logic for non-mandatory columns
    if 'date' in column_name.lower():
        return 'Datetime'
    
    unique_values = column_data.nunique()
    total_values = column_data.size
    
    if unique_values / total_values < 0.05:
        return 'Category'
    
    if pd.api.types.is_numeric_dtype(column_data):
        return 'Numeric'
    
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
        return guess_column_type(name.split('_')[0], name, column_data)
    else:
        raise ValueError("Invalid type name. Use 'file' or 'datacolumn'.")

# Example usage
if __name__ == "__main__":
    print(guess_type('file', 'my_collars.csv'))  # Should return 'Collar'
    print(guess_type('datacolumn', 'HoleID', pd.Series(['A', 'B', 'C'])))  # Should return 'HoleID'
    print(guess_type('datacolumn', 'Depth', pd.Series([10, 20, 30])))  # Should return 'Depth'
    print(guess_type('datacolumn', 'Azimuth', pd.Series([10, 90, 180])))  # Should return 'Azimuth'
