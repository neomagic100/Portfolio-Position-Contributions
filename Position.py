class Position:
    def __init__(self, row):
        """
         @brief Initializes the object with data from the CSV file. This is called by __init__ and should not be called directly
         @param row A list containing the symbol, percent wanted, current value in dollars, (and optionally, [T/t] to ignore the position
            in calculations)
        """
        self.symbol = row[0]
        self.percentWanted = float(row[1])
        # Ensure percentages are in range [0, 1]
        if self.percentWanted > 1:
            self.percentWanted /= 100
        self.currentValue = float(row[2])
        self.actualPercent = 0
        self.ignore = False
        # If the optional ignore flag is present
        if len(row) > 3:
            if row[3].lower() == "t":
                self.ignore = True

    def __str__(self):
        """
         @brief Returns a string representation of the progress. This is used for debugging purposes. The string representation 
            will be in the form " symbol percentWanted currentValue actualPercent ".
         @return A string representation of the progress. Example : " symbol percentWanted currentValue actualPercent " >>> 
            progress = Progress. __str__
        """
        return f"{self.symbol}, {self.percentWanted:.2f}, {self.currentValue:.2f}, {self.actualPercent:.2%}"

    def addValue(self, value):
        """
         @brief Adds a value to the current value.
         @param value Value to add
        """
        self.currentValue += value
        