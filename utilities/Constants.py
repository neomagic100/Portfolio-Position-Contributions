import os

class FileConstants:
    OUTPUT_FILE_DIR  = "outputFiles"
    ARCHIVE_FILE_DIR = "archivedFiles"
    DIR_PATH         = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) # Get root project dir
    SAVE_PATH        = os.path.join(DIR_PATH, OUTPUT_FILE_DIR)
    ALT_SAVE_PATH    = os.path.join(SAVE_PATH, ARCHIVE_FILE_DIR)

class TableNames:
    CURRENT_PORTOLIO  = "Current Portfolio"
    UPDATED_PORTFOLIO = "Updated Portfolio"
    BUY_AMOUNTS       = "Buy per Position"
    
class FloatStringFormat:
    FLOAT_2_PLACES   = ".2f"
    PERCENT_2_PLACES = ".2%"
    FLOAT_3_PLACES   = ".3f"
    PERCENT_3_PLACES = ".3%"
    STRING_FORMAT    = ""
    DEFAULT_FLOAT_FORMAT  = [STRING_FORMAT, PERCENT_2_PLACES, PERCENT_2_PLACES, FLOAT_2_PLACES]