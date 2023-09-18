"""
Returns books using their IDs.

Funtions:

ReturnBook(object) -> String
TestReturnBook() 
"""

# Imports database module
import Database.database as DB
# Imports date module
from datetime import date


def ReturnBook(ID):
    """
    Attempts to return book with ID specified.

    Checks if ID is valid and if book is available already
    Returns message based on return success or failure
    If the returned book was loaned for more than 60 days then it also returns
    how long the book was loand for along with a warning message


    ID = ID of book being returned (int)

    Return: Error message(String)
    """

    # If the ID is an integer and exists in database (valid)
    if DB.CheckValidID(ID) and DB.CheckIDExists(ID):
        # If the book with corresponding ID is not available
        if not DB.CheckAvailability(ID):
            # Gets books details
            BookDatabaseEntry = DB.GetDatabaseEntry(ID)
            # Gets member ID from returned book
            MemberID = BookDatabaseEntry[5]
            # Gets log details
            BookLogEntryDate = DB.GetLatestLogEntry(ID)[1]
            # Changes member ID in database entry to 0 meaning book is available again
            DB.UpdateEntry(BookDatabaseEntry[0], BookDatabaseEntry[1],
                           BookDatabaseEntry[2], BookDatabaseEntry[3],
                           BookDatabaseEntry[4], "0")
            # Changes return date to today for corrisponding log
            DB.UpdateLatestLogEntry(ID, BookLogEntryDate, date.today()
                                    .strftime("%d-%m-%Y"), MemberID)
            # Message to be displayed on GUI
            Error = ("Book (ID = " + str(ID) + ") returned successfully")
            # Finds latest log entry of book with same ID
            LogEntry = DB.GetLatestLogEntry(ID)
            # Finds the loan time for this log
            LoanTime = DB.CalculateLoanTime(LogEntry[1], LogEntry[2])
            if (LoanTime > 60):
                # Appends a warning including how long the book was loaned for
                Error = Error + (".\nWarning, this book was loaned for " +
                                 str(LoanTime) + " days.")

        # If the book with corresponding ID is not available or does not exist
        else:
            # Message to be displayed on GUI
            Error = ("Book (ID = " + str(ID) + ") already available")
    # If the ID is nor an integer (invalid)
    else:
        # Message to be displayed on GUI
        Error = ("Invalid ID")
    return Error


def TestReturnBook():
    """
    Tests ReturnBook function with ID of 25.

    It is useful to insert test data in database.txt and logfile.txt for this test
    Prints returned values from function
    """
    print("\nTesting returning a book")
    # Attempts to return book with invalid ID
    print(ReturnBook("a"))
    # Expects "Invalid ID" returned

    # Attempts to return a book with valid ID 25
    print(ReturnBook(25))
    # If book is already available then expects "Book already available" returned
    # Otherwise, epects the database entry to be updated with new member ID of "0"
    # and the latest log entry to be updated with today as the return date
    # Then expects "Book returned successfully" returned
    # If the book was on loan for more than 60 days then expects a warning
    # message returned includes how long the book was loaned for


if __name__ == "__main__":
    print("Testing bookreturn.py")
    # Tests all functions in bookreturn module

    TestReturnBook()
