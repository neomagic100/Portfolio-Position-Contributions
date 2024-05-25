import sys
import traceback
from fetchData import getPortfolioFromFile
from Table import Table

def getContributionInput():
    """
     @brief Get amount to add from user. This is a function that asks user for amount to add and returns it
     @return float amount to add
    """
    valueToAdd = 0
    # Get the amount to add.
    while valueToAdd == 0:
        valueToAdd = input("Amount to add: $").strip() or 0
    valueToAdd = float(valueToAdd)
    return valueToAdd

# This is the main function of the program. It takes a file path as an argument
if __name__ == "__main__":
    if len(sys.argv) < 2:
        filename = "data.csv" # Used for debugging purposes, Normal execution in 'else'
    else:
        try:
            filename = sys.argv[1]
        except IndexError:
            print("A File Path must be included as a parameter")
            traceback.print_exc()
        except Exception:
            traceback.print_exc()
    
    portfolio = getPortfolioFromFile(filename)
    contributionAmount = getContributionInput()
    
    portfolio.calcDistribution(contributionAmount)
    changes = portfolio.updatePortfolio()
    Table.printOutput(portfolio, changes)
