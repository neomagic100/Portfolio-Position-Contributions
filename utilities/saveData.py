import os
import traceback
from utilities.Constants import FileConstants

if not os.path.exists(FileConstants.SAVE_PATH):
    os.makedirs(FileConstants.SAVE_PATH)

def checkForExistingFile(filename):
    """
     @brief Checks if a file exists in the save path. If it does it appends a number to the filename so that it doesn't conflict with an existing file
     @param filename Name of the file to check
     @return Filepath of the file to use.
    """
    appendCount = 1
    pathname    = FileConstants.SAVE_PATH
    oldFilename = filename
    oldFilePath = os.path.join(FileConstants.SAVE_PATH, oldFilename)
    files       = os.listdir(pathname)
    
    # Append append count to the end of the file.
    if filename in files:
        pathname = FileConstants.ALT_SAVE_PATH
        filename += ".bak"
        if not os.path.exists(pathname):
            os.makedirs(pathname)
            
        subfiles = os.listdir(pathname)
        compFilename = filename
        while compFilename in subfiles:
            compFilename = f"{filename}{str(appendCount)}"
            appendCount += 1
        filename = compFilename
        
        # Move old files into archive
        if pathname != FileConstants.SAVE_PATH:
            newFilePath = os.path.join(pathname, filename)
            os.rename(oldFilePath, newFilePath)    
            
    return oldFilePath

def printTableToFile(table, tableName):
    """
     @brief Prints a table to a file. It will create a filename from the table name and write the table to that file
     @param table the table to be printed
     @param tableName the name of the table that will be printed
    """
    
    filePath = checkForExistingFile(createFilenameFromTablename(tableName))
    try:
        with open(filePath, "w") as f:
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
