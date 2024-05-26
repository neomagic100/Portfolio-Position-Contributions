import os
import traceback

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) # Get root project dir
save_path = os.path.join(dir_path, "outputFiles")

def checkForExistingFile(filename):
    """
     @brief Checks if a file exists in the save path. If it does it appends a number to the filename so that it doesn't conflict with an existing file
     @param filename Name of the file to check
     @return Name of the file to use.
    """
    appendCount = 1
    
    # Append the append count of the append count to the save path.
    for _, _, files in os.walk(save_path):
        # Append append count to the end of the file.
        while filename in files:
            filename += f".bak.{appendCount}"
            appendCount += 1
            
    return filename

def printTableToFile(table, tableName):
    """
     @brief Prints a table to a file. It will create a filename from the table name and write the table to that file
     @param table the table to be printed
     @param tableName the name of the table that will be printed
    """
    filename = checkForExistingFile(createFilenameFromTablename(tableName))
    try:
        with open(f"outputFiles/{filename}", "w") as f:
            f.writelines(table)
    except:
        traceback.print_exc()
        
def createFilenameFromTablename(tableName):
    """
     @brief Create a filename from a table name. Change to Cabbot Case.
     @param tableName The name of the table
     @return The filename as a string with. md appended to the table name as extension
    """
    return "".join(token for token in tableName.title() if not token.isspace()) + ".md"
