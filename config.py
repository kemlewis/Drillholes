# config.py

# File upload settings
ALLOWED_EXTENSIONS = ['csv', 'txt', 'xlsx', 'xls', 'xlsm']
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200 MB

# File categories
FILE_CATEGORIES = ['Collar', 'Survey', 'Point', 'Interval']

# Column data types
COLUMN_DATATYPES = ['Text', 'Category', 'Numeric', 'Datetime', 'Boolean']

# Required columns for each file category
REQUIRED_COLUMNS = {
    'Collar': ['HoleID', 'DH_X', 'DH_Y', 'DH_Z', 'Depth'],
    'Survey': ['HoleID', 'Depth', 'Dip', 'Azimuth'],
    'Point': ['HoleID', 'Depth'],
    'Interval': ['HoleID', 'From', 'To']
}

# Default values for missing data
DEFAULT_MISSING_VALUES = {
    'Text': 'Unknown',
    'Numeric': 0.0,
    'Datetime': '1900-01-01',
    'Boolean': False
}

# Plotting settings
PLOT_COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
PLOT_MARKER_SIZE = 5
PLOT_LINE_WIDTH = 2

# Validation settings
MAX_DEPTH_WARNING = 10000  # Maximum depth in meters before warning
MIN_DIP = -90
MAX_DIP = 90
MIN_AZIMUTH = 0
MAX_AZIMUTH = 360

# Analysis settings
DEPTH_BIN_SIZE = 50  # Bin size for depth histogram in meters
DIP_BIN_SIZE = 5  # Bin size for dip histogram in degrees
AZIMUTH_BIN_SIZE = 10  # Bin size for azimuth histogram in degrees

# Logging settings
LOG_FILE = 'drillhole_processor.log'
LOG_LEVEL = 'INFO'

# User interface settings
APP_TITLE = "Drillhole Data Processor"
APP_ICON = ":drill:"
SIDEBAR_WIDTH = 300
MAIN_CONTENT_WIDTH = 800

# Data processing settings
CHUNK_SIZE = 10000  # Number of rows to process at a time for large files

# 3D plot settings
PLOT_3D_HEIGHT = 800
PLOT_3D_WIDTH = 1000

# Error messages
ERROR_MESSAGES = {
    'file_not_found': "File not found. Please upload the file again.",
    'invalid_file_type': "Invalid file type. Please upload a file with one of the following extensions: {allowed_extensions}",
    'file_too_large': "File is too large. Maximum allowed size is {max_size} MB.",
    'missing_required_columns': "Missing required columns: {missing_columns}",
    'invalid_data_format': "Invalid data format in column {column_name}. Expected {expected_format}.",
    'calculation_error': "Error occurred during calculation: {error_message}",
    'plotting_error': "Error occurred while creating the plot: {error_message}",
}

# Success messages
SUCCESS_MESSAGES = {
    'file_uploaded': "File {filename} uploaded successfully.",
    'data_processed': "Data processed successfully.",
    'plot_created': "Plot created successfully.",
    'analysis_complete': "Analysis completed successfully.",
}