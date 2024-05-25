import csv
import traceback
from Position import Position
from Portfolio import Portfolio
from random import random
from fetchStock import fetchLatestPrices

def _readCSVFile(filename):
    """
     @brief Reads a CSV file and returns a list of rows. This function is used to read the contents of a CSV file into a list
     @param filename The name of the file to read
     @return A list of lists of strings from the CSV file
    """
    rawText = []
    try:
        with open(filename) as f:
            csvReader = csv.reader(f, delimiter=',', quotechar='|')
            for row in csvReader:
                temp = row
                # Remove whitespace from ends of token.
                for i, entry in enumerate(temp):
                    temp[i] = entry.strip()
                rawText.append(row)
    
    except Exception:
        traceback.print_exc()
    
    # Raise exception if the file is empty
    if len(rawText) == 0:
        raise Exception(f"Specified file {filename} is empty")
    
    return rawText

def getPortfolioFromFile(filename):
    """
     @brief Reads a portfolio from a file.
     @param filename The name of the file to read. Must be a valid path
     @return A Portfolio object with the positions initialized
    """
    positions = []
    rawText = _readCSVFile(filename)
    stripBlankRows(rawText)   
    stripHeaderRow(rawText)    
    
    # Add a position to the positions list
    for row in rawText:
        tempPosition = Position(row)
        #TODO debug, change price to quantity of stocks
        positions.append(tempPosition)
        
    portfolio = Portfolio(positions)
    return portfolio
    
def stripBlankRows(rawText):
    """
     @brief Removes blank rows from rawText.
     @param rawText A list of list of strings
    """
    blanks = []
    
    # Add blanks to the blanks list.
    for rowIndex, row in enumerate(rawText):
        # Append the row to the blanks list.
        if not row or row == []:
            blanks.append(rowIndex)
            continue
        
        foundBlank = False
        # Check if there is no blank characters in the row.
        for token in row:
            # If the token is blank or empty set foundBlank to true.
            if not token or token.strip() == "":
                foundBlank = True
        
        # Append the row index to the blanks list.
        if foundBlank:
            blanks.append(rowIndex)
    
    # Return the blanks if blanks.
    if not blanks:
        return
    
    # Removes all blanks from rawText.
    blanks.reverse()
    for blankIndex in blanks:
        del rawText[blankIndex]

def stripHeaderRow(rawText):
    """
     @brief Strip header row from rawText. This is used to ensure that the first row is a float and not a row of headers
     @param rawText text from which to strip the header row
     @return text from rawText after stripping the header row
    """
    firstRow = rawText[0]
   
    # Check if no float values are in row
    # Return the first row of the first row.
    for token in firstRow:
        try:
            floatToken = float(token)
            # Return the floatToken if it is a floatToken.
            if isinstance(floatToken, float):
                return
        except ValueError:
            continue
        except Exception as e:
            raise e
    
    # No floats found, remove first row
    del rawText[0]
        