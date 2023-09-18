"""
Searches through a list of books using their titles.

Funtions:

SearchForBook(String) -> [([String, String, String, String, String, String],bool)]
PreSearchForBook(String) -> [([String, String, String, String, String, String],bool)]
TestSearchForBook()
TestPreSearchForBook()
"""

# Imports database module
import Database.database as DB
# Imports module used for regular expressions
import re


def SearchForBook(Title):
    """
    Searches for books with title matching that specified.

    Uses regular expression to search for books
    Also specifies if Book has been on loan for more than 60 days

    Title = Title of book being searched for (String)

    Return: list: [([ID (String), Genre (String), Title (String), Author (String),
    PurchaseDate (String), MemberID (String)], highlight (boolean))]
    """

    SearchResults = []
    # Gets list of all database entries
    Books = DB.GetAllEntries()
    # For books with matching title
    for i in range(len(Books)):
        if Books[i][2] == Title:
            # Finds latest log entry of book with same ID
            LogEntry = DB.GetLatestLogEntry(Books[i][0])
            LoanedFor60DaysPlus = False
            # Finds if book has been on loan for more than 60 days
            if LogEntry:
                LoanedFor60DaysPlus = DB.CalculateLoanTime(
                    LogEntry[1], LogEntry[2]) > 60
            # Appends book details and whether it has been on loan
            # for more than 60 days to search results
            SearchResults.append((Books[i], LoanedFor60DaysPlus))
    # Reduces the list length to below 10
    SearchResults = SearchResults[:min(10, len(SearchResults))]
    # Returns search results
    return SearchResults


def PreSearchForBook(Title):
    """
    Searches for books with title including that specified.

    Uses regular expression to search for books
    Also specifies if Book has been on loan for more than 60 days

    Title = Title of book being searched for (String)

    Return: list: [([ID (String), Genre (String), Title (String), Author (String),
    PurchaseDate (String), MemberID (String)], highlight (boolean))]
    """

    # Regular expression
    # (any characters followed by entered title followed by any characters)
    Pattern = ".*" + Title.lower() + ".*"
    SearchResults = []
    # Gets list of all database entries
    Books = DB.GetAllEntries()
    # For books with title including that specified
    for i in range(len(Books)):
        if re.search(Pattern, Books[i][2].lower()):
            # Finds latest log entry of book with same ID
            LogEntry = DB.GetLatestLogEntry(Books[i][0])
            LoanedFor60DaysPlus = False
            # Finds if book has been on loan for more than 60 days
            if LogEntry:
                LoanedFor60DaysPlus = DB.CalculateLoanTime(
                    LogEntry[1], LogEntry[2]) > 60
            # Appends book details and whether it has been on loan
            # for more than 60 days to search results
            SearchResults.append((Books[i], LoanedFor60DaysPlus))
    # Reduces the list length to below 10
    SearchResults = SearchResults[:min(10, len(SearchResults))]
    # Returns search results
    return SearchResults


def TestSearchForBook():
    """
    Tests SearchForBook function with title of "shades".

    Prints search results
    """
    print("\nTesting searching for a book")
    # Gets list of all books with book title matching the inputed string
    SearchResults = SearchForBook("Star Wars")
    # Prints off details of all of these books
    for Result in SearchResults:
        print(Result)
    # Expects book details of all books that have the title "Star Wars"


def TestPreSearchForBook():
    """
    Tests PreSearchForBook function with title of "shades".

    Prints search results
    """
    print("\nTesting pre searching for a book")
    # Gets list of all books with book title containg the inputed string
    SearchResults = PreSearchForBook("shades")
    # Prints off details of all of these books
    for Result in SearchResults:
        print(Result)
    # Expects book details of all books that have titles containing the string "shades"


if __name__ == "__main__":
    print("Testing booksearch.py")
    # Tests all functions in booksearch module

    TestSearchForBook()

    TestPreSearchForBook()
