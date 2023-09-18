"""
Checks out books using their IDs.

Funtions:

CheckoutBook(object, String) -> (String,[(int,[String, String,
                                String, String, String, String])])
TestCheckOutBook()
"""

# Imports database module
import Database.database as DB
# Imports date module
from datetime import date


def CheckoutBook(ID, MemberID):
    """
    Attempts to checkout book with ID and member ID specified.

    Checks if ID is valid and if book is available
    Returns message based on checout success or failure
    Also returns all books currently loaned for more than 60 days by
    specified member


    ID = ID of book being checked out (String)
    MemberID = ID of member checking out the book (String)

    Return: 2 tuple with embedded list:
    (String,[(Loan time (int),[ID (String), Genre (String), Title (String),
            Author (String), PurchaseDate (String), MemberID (String)])])
    """

    LoanDetails = []
    # If the ID is an integer and exists in database (valid)
    if DB.CheckValidID(ID) and DB.CheckIDExists(ID):
        # If the book with corresponding ID is available
        if DB.CheckAvailability(ID):

            # Message to be displayed on GUI
            Error = ("Book (ID = " + str(ID) + ") withdrawn successfully")
            # Gets details of all books loaned for more than 60 days by that member
            LoanDetails = DB.LoanedFor60DaysPlus(MemberID)
            if LoanDetails:
                Error = Error + \
                    ". Warning, this member\n \
                    has the following books on loan for more than 60 days"

            # Gets books details
            BookDatabaseEntry = DB.GetDatabaseEntry(ID)
            # Changes member ID in database entry
            DB.UpdateEntry(BookDatabaseEntry[0], BookDatabaseEntry[1],
                           BookDatabaseEntry[2], BookDatabaseEntry[3],
                           BookDatabaseEntry[4], MemberID)

            # Logs book checkout with today as checkout date
            DB.LogEntry(ID, date.today().strftime("%d-%m-%Y"),
                        "NotReturned", MemberID)

        # If the book with corresponding ID is not available or does not exist
        else:
            # Message to be displayed on GUI
            Error = ("Book (ID = " + str(ID) + ") unavailable")
    # If the ID is nor an integer (invalid)
    else:
        # Message to be displayed on GUI
        Error = ("Invalid ID")
    return Error, LoanDetails


def TestCheckOutBook():
    """
    Tests CheckOutBook function with ID of 25.

    It is useful to insert test data in database.txt and logfile.txt for this test
    Prints returned values from function
    """
    print("\nTesting checking out a book")
    # Attempts to return book with invalid ID
    print(CheckoutBook("a", "new1"))
    # Expects "Invalid ID" returned

    # Checks out book with valid ID 25 and member ID "new1"
    print(CheckoutBook(25, "new1"))
    # If book is unavailable then expects "Book unavailable" returned
    # Otherwise, epects the database entry to be updated with the new member ID
    # and a new log entry with today as the checkout date
    # and "NotReturned" as the return date
    # Then expects "Book withdrawn successfully" returned
    # Also expects a list of all books currently on loan for more than 60 days
    # by member "new1" returned


if __name__ == "__main__":
    print("Testing bookcheckout.py")
    # Tests all functions in bookcheckout module

    TestCheckOutBook()
