"""
Retrieves/modifies entries in database.txt and
Retrieves/modifies/adds entries in logfile.txt.

Funtions:

GetAllEntries() -> [[String, String, String, String, String, String]]
UpdateEntry([object, String, String, String, String, String)
GetDatabaseEntry(object) -> [String, String, String, String, String, String]
LogEntry(object, String, String, String)
GetAllLogs() -> [[String, String, String, String]]
UpdateLatestLogEntry(object, String, String, String)
GetLatestLogEntry(object)  -> [String, String, String, String]
CheckValidID(object) -> bool
CheckIDExists(object) -> bool
CheckAvailability(object) -> bool
LoanedFor60DaysPlus(String) -> ([(int,[String, String, String, String, String, String])])
CalculateLoanTime(String, String) - int
TestGetAllEntries()
TestUpdateEntry()
TestGetDatabaseEntry()
TestLogEntry()
TestGetAllLogs()
TestUpdateLatestLogEntry()
TestGetLatestLogEntry()
TestCheckValidID()
TestCheckIDExists()
TestCheckAvailability()
TestCalculateLoanTime()
TestLoanedFor60DaysPlus()
"""

# Imports date module
from datetime import datetime

# Database entries list
# list: [[ID, Genre, Title, Author, PurchaseDate, MemberID]]
__DatabaseEntries = []
# Path of text files
__Path = "Database\\"


def GetAllEntries():
    """
    Gets all database entries in database.txt.

    Only accesses the file once per program run
    This is only done if the databse entries have not yet been read

    Return: list: [[ID (String), Genre (String), Title (String),
            Author (String), PurchaseDate (String), MemberID (String)]]
    """
    # If database entries list not populated
    if not __DatabaseEntries:
        # Populates database entries list with all entries from database.txt
        for line in open(__Path + "database.txt", "r").readlines():
            __DatabaseEntries.append(line.strip('\n').split("|"))
    # Returns database entries list - maybe sort by title
    return __DatabaseEntries


def UpdateEntry(ID, Genre, Title, Author, PurchaseDate, MemberID):
    """
    Gets database entry in database.text with matching ID.

    ID = ID of book being searched for
    Genre = Genre of book for new entry
    Title = Title of book for new entry
    Author = Author of book for new entry
    PurchaseDate = Purchase date of book for new entry
    MemberID = Member ID of book for new entry
    """
    # Gets list of all database entries
    global __DatabaseEntries
    __DatabaseEntries = GetAllEntries()
    # Empties database.text file
    file = open(__Path + "database.txt", "w")
    Entry = str(ID) + "|" + Genre + "|" + Title + "|" + Author + "|" +\
        PurchaseDate + "|" + MemberID
    # Rewrites all database entries to database.txt
    for i in range(len(__DatabaseEntries)):
        # Updates entry with matching ID with new details
        if __DatabaseEntries[i][0] == ID:
            __DatabaseEntries[i] = Entry.split("|")
        file.write(__DatabaseEntries[i][0] + "|" + __DatabaseEntries[i][1] + "|" +
                   __DatabaseEntries[i][2] + "|" + __DatabaseEntries[i][3] + "|" +
                   __DatabaseEntries[i][4] + "|" + __DatabaseEntries[i][5])
        file.write("\n")
    file.close()


def GetDatabaseEntry(ID):
    """
    Gets database entry in database.txt with matching ID.

    ID = ID of book being searched for

    Return: list: [ID (String), Genre (String), Title (String),
                Author (String), PurchaseDate (String), MemberID (String)]
    """
    # Gets list of all database entries
    AllEntries = GetAllEntries()
    # Found entry initiated as nothing
    FoundEntry = []
    for i in range(len(AllEntries)):
        # Updates entry with matching ID with new details
        if AllEntries[i][0] == str(ID):
            # Found entry set to this entry
            FoundEntry = AllEntries[i]
            break
    # Returns the entry found from the search
    return FoundEntry


# log entries list
# list: [[ID, CheckoutDate, ReturnDate, MemberID]]
__LogEntries = []


def LogEntry(ID, CheckoutDate, ReturnDate, MemberID):
    """
    Writes new log entry into logfile.txt.

    ID = ID of book for log entry
    CheckoutDate = checkout date for log entry
    ReturnDate = return date for log entry
    MemberID = member ID for log entry
    """
    # Initialises log entires array if it has not been already
    global __LogEntries
    __LogEntries = GetAllLogs()
    # Writes new entry to dataabase
    file = open(__Path + "logfile.txt", "a")
    # Creates new log entry string
    LogEntry = str(ID) + "|" + CheckoutDate + "|" + ReturnDate + "|" + MemberID
    file.write(LogEntry)
    file.write("\n")
    file.close()
    # Adds entry to log entries list
    __LogEntries.append(LogEntry.split("|"))


def GetAllLogs():
    """
    Returns all logs in logfile.txt.

    Only accesses the file once per program run
    This is only done if the logs have not yet been read

    Return: list: [[ID, CheckoutDate, ReturnDate, MemberID]]
    """
    # If database entries list not populated
    if not __LogEntries:
        # Populates database entries list with all entries from database.txt
        for line in open(__Path + "logfile.txt", "r").readlines():
            __LogEntries.append(line.strip('\n').split("|"))
    # Returns database entries list - maybe sort by title
    return __LogEntries


def UpdateLatestLogEntry(ID, CheckoutDate, ReturnDate, MemberID):
    """
    Updates latest log entry in logfile.text with matching ID.

    Overwirtes this entry with new entry

    ID = ID of book being searched for
    CheckoutDate = checkout date for log entry
    ReturnDate = return date for log entry
    MemberID = member ID for log entry
    """
    # Gets list of all log entries
    global __LogEntries
    __LogEntries = GetAllLogs()
    # Empties logfile.txt
    file = open(__Path + "logfile.txt", "w")
    # Creates new log entry string
    LogEntry = str(ID) + "|" + CheckoutDate + "|" + ReturnDate + "|" + MemberID
    LogEntriesLength = len(__LogEntries) - 1
    # Loops through all log entries backwards
    for i in range(LogEntriesLength + 1):
        # Updates entry with matching ID with new details
        if __LogEntries[LogEntriesLength - i][0] == str(ID):
            __LogEntries[LogEntriesLength - i] = LogEntry.split("|")
            # Ends loop
            break

    # Rewrites all log entries to logfile.txt
    for i in range(LogEntriesLength + 1):
        file.write(__LogEntries[i][0] + "|" + __LogEntries[i][1] + "|" +
                   __LogEntries[i][2] + "|" + __LogEntries[i][3])
        file.write("\n")
    file.close()


def GetLatestLogEntry(ID):
    """
    Gets latest log entry in logfile.text with matching ID.

    ID = ID of book being searched for

    Return: list: [ID (String), CheckoutDate (String),
                    ReturnDate (String), MemberID (String)]
    """
    # Gets list of all log entries
    AllLogs = GetAllLogs()
    # Found entry initiated as nothing
    FoundEntry = []
    LogEntriesLength = len(AllLogs) - 1
    # Loops through all log entries backwards
    for i in range(LogEntriesLength + 1):
        # If log entry has matching ID
        if AllLogs[LogEntriesLength - i][0] == str(ID):
            # Found entry set to this entry
            FoundEntry = AllLogs[LogEntriesLength - i]
            # Ends search
            break
    # Returns the entry found from the search
    return FoundEntry


def CheckValidID(ID):
    """
    Returns true if the ID is an integer.

    ID = ID being checked

    Return: If ID valid (boolean)
    """
    # Checks if ID is an integer
    try:
        int(ID)
        IsValid = True
    except:
        IsValid = False
    # Returns true if it is an integer
    return IsValid


def CheckIDExists(ID):
    """
    Returns true if the book with specified ID is stored in the database.

    ID = ID of the book being checked

    Return: If ID exists (boolean)
    """
    # Gets list of all database entries
    Books = GetAllEntries()
    # Finds largest ID in database entries
    MaxID = Books[len(Books)-1][0]
    # Retruns true if ID is between zero and maximum ID inclusive
    return 0 <= int(ID) <= int(MaxID)


def CheckAvailability(ID):
    """
    Returns true if the book with specified ID is available to be loaned
    (not currently loaned).

    ID = ID of the book being checked

    Return: If book with ID available (boolean)
    """
    BookAvailable = False
    # Gets list of all database entries
    Books = GetAllEntries()
    # Checks for entry with matching ID that is available
    for i in range(len(Books)):
        if Books[i][0] == str(ID) and Books[i][5] == "0":
            BookAvailable = True
    # Returns whether or not the book is available for checkout
    return BookAvailable


def LoanedFor60DaysPlus(MemberID):
    """
    Returns loan times and details of all books with matching member IDs that
    have been on loan for more than 60 days.

    Member ID = ID for member that is having there loans checked

    Return type: list:
    ([(Loan time (int),[ID (String), Genre (String), Title (String), Author (String),
    PurchaseDate (String), MemberID (String)])])
    """
    LoanDetails = []
    # Gets list of all log entries
    LogEntries = GetAllLogs()
    # Loops through all log entries
    for i in range(len(LogEntries)):
        # Finds the loan time in days for this log entry
        LoanTime = CalculateLoanTime(LogEntries[i][1], LogEntries[i][2])
        # If the log has matching member ID and has not been returned yet and
        # has been on loan for more that 60 days
        if LogEntries[i][3] == MemberID and\
                LogEntries[i][2] == "NotReturned" and LoanTime >= 60:
            # Adds loan time and book details to results list
            LoanDetails.append((LoanTime, GetDatabaseEntry(LogEntries[i][0])))
    # Returns books details and their loan times for books that have been on
    # loan for more than 60 days
    return LoanDetails


def CalculateLoanTime(CheckoutDatestr, ReturnDatestr):
    """
    Returns the number of days between the two dates.

    If "NotReturned" is entered as the return date then it will use today as
    thereturn date

    CheckoutDatestr = checkout date (String) Format: 'dd-mm-YYYY'
    ReturnDatestr = return date or "NotReturned" (String) Format: 'dd-mm-YYYY'

    Return: number of days between dat(int)
    """
    # Turns checkout date string into date format
    CheckoutDate = datetime.strptime(CheckoutDatestr, '%d-%m-%Y')
    # If the book has not been returned
    if ReturnDatestr == "NotReturned":
        # Gets todays date in date format
        ReturnDate = datetime.strptime(datetime.strftime(
            datetime.today(), '%d-%m-%Y'), '%d-%m-%Y')
    else:
        # Turns return date string into date format
        ReturnDate = datetime.strptime(ReturnDatestr, '%d-%m-%Y')
    # Returns the number of days between the checkout and return days
    return abs((ReturnDate - CheckoutDate).days)


def TestGetAllEntries():
    """
    Tests GetAllEntries function.

    Prints returned values from function
    """
    print("\nTesting getting all entries in database.txt:")
    # Gets list of all database entries
    AllEntries = GetAllEntries()
    # Prints off all database entries
    for Entry in AllEntries:
        print(Entry)
    # Expects a list containing all database entries
    # (each entry is a list with length 6 in the list)


def TestUpdateEntry():
    """
    Tests UpdateEntry function twice with different entries both with ID of 26.

    Changes entry in database.txt
    Prints details of changed entry
    """
    print("\nTesting updating an entry")
    # Updates entry with ID 29
    UpdateEntry("29", "Boring", "Software Engineering tenth edition",
                "Ian Sommerville", "1-10-2015", "test")
    # Print entry with ID 29
    print(GetDatabaseEntry(29))
    # Updates entry with ID 29
    UpdateEntry("29", "Boring", "Software Engineering tenth edition",
                "Ian Sommerville", "1-10-2015", "0")
    # Print entry with ID 29
    print(GetDatabaseEntry(29))
    # Expects the entry with ID of 29 to be changed inside the text file
    # (member id changed to "test" and then to "0")


def TestGetDatabaseEntry():
    """
    Tests GetDatabaseEntry function with ID of 26.

    Prints returned values from function
    """
    print("\nTesting ID search")
    # Print entry with ID 26
    print(GetDatabaseEntry(26))
    # Expected to return the database entry with ID of 26 (list of length 6)


def TestLogEntry():
    """
    Tests LogEntry function with a new log with ID of 25.

    Logs new entry in logfile.txt
    """
    print("\nTesting Logging entry")
    # Logs new entry
    LogEntry("29", "02-12-2021", "NotReturned", "test")
    # Expects new log entry into logfile.txt with details specified above


def TestGetAllLogs():
    """
    Tests GetAllLogs function.

    Prints returned values from function
    """
    print("Testing getting all logs in logfile.txt:")
    # Gets list of all log entries
    AllLogs = GetAllLogs()
    # Prints off all log entries
    for Log in AllLogs:
        print(Log)
    # Expects a list of all log entries
    # (each entry is a list with length 4 in the list)


def TestUpdateLatestLogEntry():
    """
    Tests UpdateLatestLogEntry function with a new log with ID of 25.

    Changes entry in logfile.txt
    Prints details of changed entry
    """
    print("\nTesting updating latest log entry")
    # Updates latest log entry with matching ID
    UpdateLatestLogEntry("29", "02-12-2021", "02-12-2021", "test")
    # Gets list of all log entries
    AllLogs = GetAllLogs()
    # Prints off all log entries
    for Log in AllLogs:
        print(Log)
    # Expects latest log entry with ID of 29 to be changed to above entry
    # in log file.txt


def TestGetLatestLogEntry():
    """
    Tests GetLatestLogEntry function with ID of 25.

    Prints returned values from function
    """
    print("\nTesting getting latest log entry")
    # Prints latest log entry with matching ID
    print(GetLatestLogEntry(25))
    # Expects the details of the latest (most recent) log entry with ID of 25


def TestCheckValidID():
    """
    Tests CheckValidID function three times with different IDs.

    Prints returned values from function
    """
    print("\nTesting check valid ID")
    # Returns true if 12 is a valid ID
    print(CheckValidID(12))
    # Expects True
    # Returns true if "12" is a valid ID
    print(CheckValidID("12"))
    # Expects True
    # Returns true if "aca" is a valid ID
    print(CheckValidID("aca"))
    # Expects False


def TestCheckIDExists():
    """
    Tests CheckIDExists function three times with different IDs.

    Prints returned values from function
    """
    print("\nTesting ID existence")
    # Checks if ID -11 exists in database
    print(CheckIDExists(-11))
    # Expects False
    # Checks if ID 11 exists in database
    print(CheckIDExists(11))
    # Expects True
    # Checks if ID 31 exists in database
    print(CheckIDExists(31))
    # Expects True


def TestCheckAvailability():
    """
    Tests CheckAvailability function twice with different IDs.

    Prints returned values from function
    """
    print("\nTesting book availability")
    # Returns true if the book with ID 13 is available to be loaned
    print(CheckAvailability(13))
    # Expects true if book with ID 13 is available and False if it has been loaned
    # Returns true if the book with ID 25 is available to be loaned
    print(CheckAvailability(25))
    # Expects true if book with ID 13 is available and False if it has been loaned


def TestCalculateLoanTime():
    """
    Tests CalculateLoanTime function twice with different dates.

    Prints returned values from function
    """
    print("\nTesting loan time calculation")
    # Returns number of days between the two dates
    print(CalculateLoanTime("02-6-2020", "02-12-2021"))
    # Expects 548
    # Returns number of days between the date and today
    print(CalculateLoanTime("01-12-2021", "NotReturned"))
    # Expects the number of days between 01-12-2021 and today


def TestLoanedFor60DaysPlus():
    """
    Tests LoanedFor60DaysPlus function with "test" as member ID.

    Prints returned values from function
    """
    print("\nTesting 60 day plus loan search")
    # Gets all books and loan times for said books that have been on loan for
    # more that 60 days by the specified member
    Loans = LoanedFor60DaysPlus("test")
    for Loan in Loans:
        print(Loan)
    # Expects details and loan time for all books currently loaned for more than
    # 60 days by member with member ID "test"


if __name__ == "__main__":
    print("Testing database.py")
    # Changes file path for database.py test
    # (by defualt, path is from menu.py file location)
    global __path
    __Path = ""
    # Tests all functions in database module

    TestGetAllEntries()

    TestUpdateEntry()

    TestGetDatabaseEntry()

    TestLogEntry()

    TestGetAllLogs()

    TestUpdateLatestLogEntry()

    TestGetLatestLogEntry()

    TestCheckValidID()

    TestCheckIDExists()

    TestCheckAvailability()

    TestCalculateLoanTime()

    TestLoanedFor60DaysPlus()
