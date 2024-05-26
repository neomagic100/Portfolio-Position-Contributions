from enum import Enum
from tabulate import tabulate
from utilities.saveData import printTableToFile

FLOAT_2_PLACES   = ".2f"
PERCENT_2_PLACES = ".2%"
FLOAT_3_PLACES   = ".3f"
PERCENT_3_PLACES = ".3%"
STRING_FORMAT    = ""

class Column(Enum):
    SYMBOL         = 1
    PERCENT_WANTED = 2
    PERCENT_ACTUAL = 3
    QUANTITY       = 4
    CURRENT_VALUE  = 5
    CHANGE_VALUE   = 6
    
    TABLE_HEADERS  = {SYMBOL         : "Symbol", 
                      PERCENT_WANTED : "Desired Weight (%)",
                      PERCENT_ACTUAL : "Actual Weight (%)",
                      QUANTITY       : "Quantity (Shares)", 
                      CURRENT_VALUE  : "Current Value ($)"}
    
    OTHER_HEADERS  = {CHANGE_VALUE   : "Buy Amount ($)"}
        
    def getPositionRowData(columns, position, row):
        """
         @brief Adds data from position to row. This is used to fill the table data when inserting a row
         @param columns List of columns that should be added
         @param position Position object to be added
         @param row List to be filled with data from position ( list )
        """
        # Add symbol to the row if it is a symbol column
        if Column.SYMBOL.value in columns:
            row.append(position.symbol)
        # Add percent wanted column to row
        if Column.PERCENT_WANTED.value in columns:
            row.append(position.percentWanted)
        # Add the actual percent to the row.
        if Column.PERCENT_ACTUAL.value in columns:
            row.append(position.actualPercent)
        # Add the number of shares to the row.
        if Column.QUANTITY.value in columns:
            row.append(position.quantityShares)
        # Append current value to row.
        if Column.CURRENT_VALUE.value in columns:
            row.append(position.currentValue)
            
    def getColumnHeaders(columns, row):
        """
         @brief Adds headers to the row based on the columns. This is used to determine which columns are displayed in the table
         @param columns List of columns to be displayed
         @param row List to be filled with headers for each column
        """
        # Add column headers to row.
        if Column.SYMBOL.value in columns:
            row.append(Column.TABLE_HEADERS.value[Column.SYMBOL.value])
        # Add column. PERCENT_WANTED column to row.
        if Column.PERCENT_WANTED.value in columns:
            row.append(Column.TABLE_HEADERS.value[Column.PERCENT_WANTED.value])
        # Add column. PERCENT_ACTUAL column to row.
        if Column.PERCENT_ACTUAL.value in columns:
            row.append(Column.TABLE_HEADERS.value[Column.PERCENT_ACTUAL.value])
        # Add the number of shares to the row.
        if Column.QUANTITY.value in columns:
            row.append(Column.QUANTITY.value[Column.QUANTITY.value])
        # Add the current value to the row.
        if Column.CURRENT_VALUE.value in columns:
            row.append(Column.TABLE_HEADERS.value[Column.CURRENT_VALUE.value])
        # Add the value to buy to the row
        if Column.CHANGE_VALUE.value in columns:
            row.append(Column.OTHER_HEADERS.value[Column.CHANGE_VALUE.value])

class Table:
    DEFAULT_FLOAT_FORMAT  = [STRING_FORMAT, PERCENT_2_PLACES, PERCENT_2_PLACES, FLOAT_2_PLACES]
               
    def createOutputTable(positions, columns = None):
        """
         @brief Creates a table of positions. It is used to generate the output the to the user
         @param positions List of positions that need to be output
         @param columns List of Columns (Enumerated) to be displayed. Default is all (default = None)
         @return List of lists that represent the output table of the positions
        """
        table   = []
        headers = []
        
        # Get the headers for the columns.
        if not columns:
            headers = list(Column.TABLE_HEADERS.value.values())
        else:
            Column.getColumnHeaders(columns, headers)
            
        table.append(headers)
            
        # Generates a row of the positions in the table.
        # Add a row for each position in positions.
        for position in positions:
            row = []
            # Returns the position data for the current position.
            if not columns:
                row.append(position.symbol)
                row.append(position.percentWanted)
                row.append(position.actualPercent)
                row.append(position.quantityShares)
                row.append(position.currentValue)
            else:
                Column.getPositionRowData(columns, position, row)
                
            table.append(row)
            
        return table
    
    def createTable(tableRows, useForFile = False, use3Places = False):
        """
         @brief Create a table from a list of rows. This is a function to use with the output of createOutputTable.
         @param tableRows The rows of the table. Must be a list of lists
         @param useForFile Boolean True if the table is to be printed to a file
         @param use3Places Boolean to display floating points to 3 decimal places if True (default = False)
         @return A table that can be printed
        """
        tableFormat = "pipe" if useForFile else "fancy_grid"
        
        return tabulate(tableRows, 
                        headers  = "firstrow", 
                        tablefmt = tableFormat,
                        floatfmt = Table.getFloatFormat(tableRows, use3Places))
        
    def getFloatFormat(tableRows, use3Places = False):
        """
         @brief Create a list of table rows to float format used by tabulate to display values in specific floating point format
         @param tableRows list of rows from table
         @param use3Places Boolean to display floating points to 3 decimal places if True (default = False)
         @return list of floats formatted to display values in floating point format used by tabulate
        """
        floatList = []
        sampleRow = tableRows[-1]
        headers   = tableRows[0]
        # Format the sample row as a list of floats.
        for colIndex, col in enumerate(sampleRow):
            # Format the column as a float list.
            if isinstance(col, str):
                floatList.append(STRING_FORMAT)
            elif headers[colIndex] == Column.TABLE_HEADERS.value[Column.PERCENT_WANTED.value] or \
                 headers[colIndex] == Column.TABLE_HEADERS.value[Column.PERCENT_ACTUAL.value]:
                decimalFormat = PERCENT_3_PLACES if use3Places else PERCENT_2_PLACES
                floatList.append(decimalFormat)
            elif headers[colIndex] == Column.TABLE_HEADERS.value[Column.CURRENT_VALUE.value] or \
                 headers[colIndex] == Column.OTHER_HEADERS.value[Column.CHANGE_VALUE.value]  or \
                 headers[colIndex] == Column.TABLE_HEADERS.value[Column.QUANTITY.value]:
                decimalFormat = FLOAT_3_PLACES if use3Places else FLOAT_2_PLACES
                floatList.append(decimalFormat)
            else:
                raise Exception("Table value not identified for formatting")
            
        return floatList
    
    def printOutput(portfolio, changes):
        """
        @brief Prints the output to the console. This is a helper function for test and logging purposes. 
            It takes a portfolio and a list of changes to each position
        @param portfolio The portfolio to be printed
        @param changes A dictionary of position symbols and the amount to change for each
        """
        tableRows = []
        columns   = [Column.SYMBOL.value, Column.QUANTITY.value, Column.CHANGE_VALUE.value]
        headers   = [Column.TABLE_HEADERS.value[columns[0]],
                     Column.TABLE_HEADERS.value[columns[1]],
                     Column.OTHER_HEADERS.value[columns[2]]]
          
        tableRows.append(headers)
        # Prints the changes to the console.
        for symbol, valueToAdd in changes.items():
            quantityToAdd = valueToAdd / portfolio.latestPrices[symbol]
            row = [symbol, quantityToAdd, valueToAdd]
            tableRows.append(row)
        tableName = "Buy per Position"
        print(f"\n{tableName}:\n")
        table = Table.createTable(tableRows, use3Places = True)
        tableToFile = Table.createTable(tableRows, useForFile = True, use3Places = True)
        print(table)
        printTableToFile(tableToFile, tableName)
         
def printPortfolioTable(portfolio, title, columns = None):
    """
     @brief Prints a table of positions for a portfolio. This is a convenience function to print the positions of a Portfolio object to the console
     @param portfolio The portfolio to print the positions for
     @param title The title of the portfolio ( for example " Current Portfolio " )
     @param columns A list of column names to print. MUST be Column Enums (default = None)
    """
    print(f"\n{title}:\n")
    portfolio.printPositions(columns)
    portfolio.printPositionsToFile(title, columns)
    print()
    