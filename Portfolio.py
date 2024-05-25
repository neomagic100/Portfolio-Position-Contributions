from copy import deepcopy
from Table import Table

class Portfolio:
    def __init__(self, positions):
        """
         @brief Initializes the class by populating the list of positions to be used in the calculation. 
            This is the first step in the calculation of percentages.
         @param positions A list of positions that will be used in the calculation
        """
        self.positions = positions
        self.initDesiredPercentages()
        self.balance = self.getPositionSum()
        self.initPositionChanges()
        self.percentageDistribution = {}
        self.calculatePercentages()
    
    def updatePortfolio(self):
        """
         @brief Update the portfolio based on the changes made. 
            This is called by the position changes and should not be called directly by the user.
         @return A dictionary of position changes that need to be applied to the portfolio in order to get the portfolio up to date
        """
        changeSum = 0
        
        # Add the current value and change sum of the position changes for each symbol.
        for symbol, posChange in self.positionChanges.items():
            position = self.getPositionBySymbol(symbol)
            position.currentValue += posChange
            changeSum += posChange
        
        self.balance += changeSum
        self.calculatePercentages()
        changesToPortfolio = deepcopy(self.positionChanges)
        self.initPositionChanges()
        return changesToPortfolio    
        
    def initPositionChanges(self):
        """
         @brief Initialize self.positionChanges to a dictionary mapping symbols to 0. This is used to avoid recomputing 
            the values when a position is changed
        """
        self.positionChanges = {}
        # Reset the position changes for each position.
        for position in self.positions:
            self.positionChanges[position.symbol] = 0
    
    def getPositionSum(self):
        """
         @brief Sum of all positions' current values.
         @return The sum of all positions' current values as a floating point number
        """
        res = 0
        # Returns the current value of all positions in the current position
        for pos in self.positions:
            res += pos.currentValue
        return res
    
    def initDesiredPercentages(self):
        """
         @brief Initialize the dictionary that maps symbols to percentWanted. This is used to determine the percentage 
            of a position that should be displayed
        """
        self.desiredPercentages = {}
        # Set the desired percentages for each position in the position.
        for pos in self.positions:
            self.desiredPercentages[pos.symbol] = pos.percentWanted
    
    def calculatePercentages(self):            
        """
         @brief Calculate and store the percentages of each positioin in the percentageDistribution.
        """
        # Calculates the percentage of the current value and percentage distribution for each position.
        for pos in self.positions:
            pos.actualPercent = pos.currentValue / self.balance
            self.percentageDistribution[pos.symbol] = pos.actualPercent
    
    def calcDistribution(self, value):
        """
         @brief Calculates the distribution of positions based on the current value. This is called by the update () method to update the position changes
         @param value the value we want to
        """
        remain = value
        positionsUnderDesired = self._getPercentagesToChange()
        # Calculate the amount of remaining values for a given symbol.
        for symbol, percentToAdd in positionsUnderDesired.items():
            if self.getPositionBySymbol(symbol).ignore:
                continue
            tempVal = percentToAdd * remain
            currentPositionValue = self.getPositionBySymbol(symbol).currentValue
            updatedValue = tempVal + currentPositionValue
            # If the value of the symbol is bigger than the desiredPercentages symbol then the value is added to the desiredPercentages.
            if updatedValue > self.desiredPercentages[symbol] * (self.balance + remain): # value > percentWanted
                actualValueToAdd = self._calcValueToAdd(symbol)
                tempVal = actualValueToAdd
            remain -= tempVal
            # Calculation error in amount remaining upon distribution
            if remain < -0.05:
                raise Exception("Calculation error in amount remaining upon distribution")
            
            self.positionChanges[symbol] = tempVal
        
        # Add the remaining percentages to the position changes.
        if remain > 0:
            amountsToAdd = {}
            # Adds a percentage to the amount of percentages to add to the positionChanges.
            for symbol, percent in self.desiredPercentages.items():
                # Add symbol to amountsToAdd.
                if symbol not in amountsToAdd.keys():
                    amountsToAdd[symbol] = 0
                    if self.getPositionBySymbol(symbol).ignore:
                        continue
                amountsToAdd[symbol] += remain * percent
                self.positionChanges[symbol] += amountsToAdd[symbol]
                
    def _calcValueToAdd(self, symbol):
        """
         @brief Calculate the value to add to the balance. This is based on the balance of the symbol and the current position
         @param symbol The symbol to calculate the value for
         @return The value to add to the balance as a float
        """
        return self.balance * self.desiredPercentages[symbol] - self.getPositionBySymbol(symbol).currentValue
        
    def _getPercentagesToChange(self):
        """
         @brief Returns a dictionary of percentages to change based on how many changes have been made. The keys of the dictionary are 
            symbols and the values are the percentage of changes that need to be made in order to make the change.
         @return A dictionary of symbols to change as a percentage of the difference between the current and the last time it was
        """
        diffPercents = self.findPercentDiff()
        perSum = 0
        # Calculate the total percentage of the differences in the percentage.
        for diff in diffPercents.values():
            if diff > 0:
                perSum += diff
        percentagesToChange = {}
        # Set percentagesToChange for each symbol.
        for symbol, diff in diffPercents.items():
            if diff > 0:
                percentagesToChange[symbol] = diff / perSum
        return percentagesToChange
    
    def getPositionBySymbol(self, symbol):
        """
         @brief Returns position by symbol. Throws exception if position not found.
         @param symbol symbol of position to look for
         @return Position object found in the portfolio (exception will be raised in case of position not existing)
        """
        # Returns the position of the symbol in the position list.
        for pos in self.positions:
            # Returns the position of the current position.
            if pos.symbol == symbol:
                return pos
        raise Exception(f"Position '{symbol}' not found in portfolio")
        
    # Get DesiredPercent - Actual Percent    
    def findPercentDiff(self):
        """
         @brief Finds the difference between the desired percentages and the percentage distribution.
         @return A dictionary with the difference between the desired percentages and the percentage distribution. 
            Keys are the symbols and values are the percent
        """
        diff = {}
        for symbol in self.desiredPercentages.keys():
            diff[symbol] = self.desiredPercentages[symbol] - self.percentageDistribution[symbol]
        return diff
    
    def printPositions(self, columns = None):
        """
         @brief Print the positions of the postitions in a table.
         @param columns List of columns to display. Default is all (default = None)
        """
        sortedPostitions = sorted(self.positions, reverse = True)
        tableRows = Table.createOutputTable(sortedPostitions, columns)
        table = Table.createTable(tableRows)
        print(table)      
            
    def _toString(self, orderedList = []):
        """
         @brief Returns a string representation of the positions. If orderedList is given the positions are ordered by 
            percentage of Portfolio
         @param orderedList a list of positions to order (default = [])
         @return a string representation of the positions in the order of portfolio percentage
        """
        positions = self.positions
        # Set positions to the list of positions
        if orderedList:
            positions = orderedList
            
        s = ""
        for pos in positions:
            s += (str(pos) + "\n")
        return s
    
    def __str__(self):
        """
         @brief Returns a string representation of the object. This is useful for debugging purposes. The string representation 
            can be parsed by : py : meth : ` __str__ `.
         @return A string representation of the object or None if the object is not a string or cannot be parsed by
        """
        return self._toString()
    
    def __repr__(self):
        """
         @brief Returns a string representation of the object. This is useful for debugging purposes. The string representation 
            can be parsed by : func : ` __repr__ `.
         @return A string representation of the object. Example :. >>> object = 42x4 ; print ( object. __repr__
        """
        return self._toString()
