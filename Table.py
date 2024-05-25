from enum import Enum
from tabulate import tabulate

class Column(Enum):
    SYMBOL         = 1
    PERCENT_WANTED = 2
    PERCENT_ACTUAL = 3
    CURRENT_VALUE  = 4
    
    TABLE_HEADERS = {SYMBOL         : "Symbol", 
                     PERCENT_WANTED : "Desired Weight (%)",
                     PERCENT_ACTUAL : "Actual Weight (%)", 
                     CURRENT_VALUE  : "Current Value ($)"}
    
    def getPositionRowData(columns, position, row):
        """
         @brief Adds data from position to row. This is used to fill the table data when inserting a row
         @param columns List of columns that should be added
         @param position Position object to be added
         @param row List to be filled with data from position ( list )
        """
        # Add symbol to the row if it is a symbol column
        if Column.SYMBOL in columns:
            row.append(position.symbol)
        # Add percent wanted column to row
        if Column.PERCENT_WANTED in columns:
            row.append(position.percentWanted)
        # Add the actual percent to the row.
        if Column.PERCENT_ACTUAL in columns:
            row.append(position.actualPercent)
        # Append current value to row.
        if Column.CURRENT_VALUE in columns:
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
        # Add the current value to the row.
        if Column.CURRENT_VALUE.value in columns:
            row.append(Column.TABLE_HEADERS.value[Column.CURRENT_VALUE.value])

class Table:
    FLOAT_FORMAT  = ["", ".2%", ".2%", ".2f"]
               
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
                row.append(position.currentValue)
            else:
                Column.getPositionRowData(columns, position, row)
                
            table.append(row)
            
        return table
    
    def createTable(tableRows):
        """
         @brief Create a table from a list of rows. This is a function to use with the output of createOutputTable.
         @param tableRows The rows of the table. Must be a list of lists
         @return A table that can be printed
        """
        return tabulate(tableRows, 
                        headers  = "firstrow", 
                        tablefmt = "fancy_grid",
                        floatfmt = Table.getFloatFormat(tableRows))
        
    def getFloatFormat(tableRows):
        """
         @brief Create a list of table rows to float format used by tabulate to display values in specific floating point format
         @param tableRows list of rows from table
         @return list of floats formatted to display values in floating point format used by tabulate
        """
        floatList = []
        sampleRow = tableRows[-1]
        headers   = tableRows[0]
        # Format the sample row as a list of floats.
        for colIndex, col in enumerate(sampleRow):
            # Format the column as a float list.
            if isinstance(col, str):
                floatList.append("")
            elif headers[colIndex] == Column.TABLE_HEADERS.value[Column.PERCENT_WANTED.value] or \
                 headers[colIndex] == Column.TABLE_HEADERS.value[Column.PERCENT_ACTUAL.value]:
                floatList.append(".2%")
            elif headers[colIndex] == Column.TABLE_HEADERS.value[Column.CURRENT_VALUE.value]:
                floatList.append(".2f")
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
        print("Add amounts to each position:")
        # Prints the changes to the console.
        for symbol, amountToAdd in changes.items():
            print(f"{symbol}: ${amountToAdd:.2f}")
        print()    
        print("Portfolio:")
        portfolio.printPositions()
