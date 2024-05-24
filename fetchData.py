import csv
import traceback
from Position import Position
from Portfolio import Portfolio

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
    rawText = _readCSVFile(filename)    
    
    positions = []
    # Add a position to the positions list
    for row in rawText:
        positions.append(Position(row))

    portfolio = Portfolio(positions)
    return portfolio
