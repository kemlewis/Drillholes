from fuzzywuzzy import process

# Define the possible categories for files and data columns
FILE_CATEGORIES = ['Collar', 'Survey', 'Point', 'Interval']
COLUMN_DATATYPES = ['Text', 'Category', 'Numeric', 'Datetime', 'Boolean']
REQUIRED_COLUMNS = {
    'Collar': ['HoleID', 'DH_X', 'DH_Y', 'DH_Z', 'Depth'],
    'Survey': ['HoleID', 'Depth', 'Dip', 'Azimuth'],
    'Point': ['HoleID', 'Depth'],
    'Interval': ['HoleID', 'From', 'To']
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

def guess_column_type(column_name):
    """
    Guess the column type based on the column name.
    
    Parameters:
    column_name (str): The name of the column to guess the type for.
    
    Returns:
    str: The best guess for the column type.
    """
    all_columns = [col for sublist in REQUIRED_COLUMNS.values() for col in sublist] + COLUMN_DATATYPES
    best_guess, _ = process.extractOne(column_name, all_columns)
    return best_guess

def guess_type(type_name, name):
    """
    Guess the type based on the type name and name.
    
    Parameters:
    type_name (str): The type name ("file" or "datacolumn").
    name (str): The name to guess the type for.
    
    Returns:
    str: The best guess for the type.
    """
    if type_name.lower() == 'file':
        return guess_file_type(name)
    elif type_name.lower() == 'datacolumn':
        return guess_column_type(name)
    else:
        raise ValueError("Invalid type name. Use 'file' or 'datacolumn'.")

# Example usage
if __name__ == "__main__":
    print(guess_type('file', 'my_collars.csv'))  # Should return 'Collar'
    print(guess_type('datacolumn', 'HoleID'))  # Should return 'HoleID'
    print(guess_type('datacolumn', 'Depth'))  # Should return 'Depth'
