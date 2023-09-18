"""
Recommends books using member ID.

Funtions:

RecommendBooks(String) -> ([String, String, String, String, String, String, int],
                            dictionary, dictionary, dictionary)
RankBooks() -> [[String, String, String, String, String, String, int]]
InsertRanking(Dictionary, String)
InsertPopularityRanking(String,String)
CalculateAverageBookLoanPeriod() -> int
MergeSortRankings([String,String,String,String,String,String,int])
MergeRankings([String,String,String,String,String,String,int],
            [String,String,String,String,String,String,int],
            [String,String,String,String,String,String,int])
TestMergeSort()
TestInsertRanking()
TestInsertPopularityRanking()
TestCalculateAverageBookLoanPeriod()
TestRankBooks()
TestRecommendBooks()
"""

# Imports database module
import Database.database as DB

# Dictionary containing frequency of genres logged by the member
# (popularty of genres for a particular member) (Genre : Frequency)
__GenreRankings = {}
# Dictionary containing frequency of authors logged by the member
# (popularty of authors for a particular member) (Author : Frequency)
__AuthorRankings = {}
# Dictionary containing popularity density of titles logged by all members
# (Popularity of all books) (Title : Popularity)
__PopularityRankings = {}
# Dictionary conataining all books read by member
__ReadBooks = []


def RecommendBooks(MemberID):
    """
    Recommends book for specified member.

    Does this using the Genres read by member, Authors for books read by
    member, and popularity of all books in the log history
    Sorts these recommendations into decending order using the books
    recommendation ranking
    Returns 10 recommended books

    Member ID = ID of member that books are being recommended for (String)

    Return: 4 tuple:
    (list: [[ID (String), Genre (String), Title (String), Author (String),
    PurchaseDate (String), MemberID (String), Ranking (int)]],
    dictionary, dictionary, dictionary)
    """

    # Wipes dictionaries and lists populated by previous recommendation
    RecommendBooks = []
    global __GenreRankings
    __GenreRankings = {}
    global __AuthorRankings
    __AuthorRankings = {}
    global __PopularityRankings
    __PopularityRankings = {}
    global __ReadBooks
    __ReadBooks = []
    global __AverageBookLoanPeriod
    # Finds average book loan period (average number of days between two book withdrawals)
    __AverageBookLoanPeriod = CalculateAverageBookLoanPeriod()
    # For every log
    Logs = DB.GetAllLogs()
    for Log in Logs:
        Book = DB.GetDatabaseEntry(Log[0])
        # If the log has matching Member ID
        if Log[3] == MemberID:
            # Adds the genre of the book to GenreRankings
            InsertRanking(__GenreRankings, Book[1])
            # Adds the author of the book to AuthorRankings
            InsertRanking(__AuthorRankings, Book[3])
            # Adds book tile to list of read books
            if not Book[2] in __ReadBooks:
                __ReadBooks.append(Book[2])
        # Adds the title of the book to PopularityRankings
        InsertPopularityRanking(Book[2], Book[4])

    # Ranks books using genre, author, and popularity rankings
    RecommendBooks = RankBooks()
    # Sorts rankings using merge sort
    MergeSortRankings(RecommendBooks)
    # Reduces the list length to below 10
    RecommendBooks = RecommendBooks[:min(10, len(RecommendBooks))]
    # Returns recommended books in order of ranking
    return RecommendBooks, __GenreRankings, __AuthorRankings, __PopularityRankings


def RankBooks():
    """
    Ranks all books based on genre, author, and tile frequency lists.

    Does this using the Genres read by member, Authors for books read by
    member, and popularity of all books in the log history
    Also ignores books already read by the member

    Return type: list:
    [[ID (String), Genre (String), Title (String), Author (String),
    PurchaseDate (String), MemberID (String), Ranking (int)]]
    """
    RankedBooks = []
    # For every book in the database
    for Book in DB.GetAllEntries():

        Unique = True
        # Ignores if book already read by member
        if Book[2] in __ReadBooks:
            Unique = False
        else:
            # Checks if book title already ranked
            for RankedBook in RankedBooks:
                if RankedBook[2] == Book[2]:
                    Unique = False
                    break
        # If book title not yet ranked
        if Unique:

            # Ranks book
            Rank = 0
            # If the books genre is in genre frequency dictionary
            if Book[1] in __GenreRankings:

                # Increase rank by 4 * frequency of that genre for this member
                Rank += __GenreRankings[Book[1]] * 4

            # If the books genre is in author frequency dictionary
            if Book[3] in __AuthorRankings:

                # Increase rank by 2 * frequency of that author for this member
                Rank += __AuthorRankings[Book[3]] * 2

            # If the books title is in title frequency dictionary
            if Book[2] in __PopularityRankings:

                # Increase rank by the frequency density of that title
                # (1 ≈ 1 loan every average book loan period)
                Rank += __PopularityRankings[Book[2]]

            # Adds book and its calculated rank to list of ranked books
            Book = Book + [Rank]

            RankedBooks.append(Book)
    # Returns list of ranked books
    return RankedBooks


def InsertRanking(Rankings, Attribute):
    """
    Inserts an attribute into a dictionary containing the frequency of
    different attributes.

    If the attribute already exists in the dictionary then in inrements its
    frequency count by 1.
    Otherwise it appeneds the attribute with a frequency of 1.

    Rankings = the dictionary that the attribute will
    be insterted into (dictionary: Attribute:Frequency)
    Attribute = the attribute (genre or author)
    that is to be inserted (String)
    """

    # If the books attribute is already stored in the frequency dictionary
    if Attribute in Rankings:
        # Increments frequency count
        Rankings[Attribute] = Rankings[Attribute] + 1
    # If the books attribute is not already stored in the frequency dictionary
    else:
        # Adds books attribute to the frequency dictionary with a frequency of 1
        Rankings[Attribute] = 1


def InsertPopularityRanking(Title, PurchaseDate):
    """
    Inserts title into a dictionary (PopularityRankings) containing the
    popularity density of different book titles.

    If the title already exists in the dictionary then in increments its
    popularity density count by (average book loan period / age of book in days).
    Otherwise it appeneds the attribute with a popularity density of
    (average book loan period / age of book in days).

    Title = the title that is to be inserted (String)
    PurchaseDate = the purchase date (%d-%m-%Y) of the book with corrisponding title
    that is to be inserted (String)
    """

    # Average book loan period (90 means average of 1 loan every 90 days)
    #AverageBookLoanPeriod = 90
    # If the books title is already stored in the dictionary
    if Title in __PopularityRankings:
        # Increases popularity density by (90 / age of book in days)
        # (1 ≈ 1 loan every average book loan period)
        # Limits to two decimal places
        __PopularityRankings[Title] = __PopularityRankings[Title] + \
            float("{:.2f}".format(((__AverageBookLoanPeriod /
                                    DB.CalculateLoanTime(PurchaseDate, "NotReturned")))))
    # If the books tilte is not already stored in the dictionary
    else:
        # Adds books title to the  dictionary with a popularity density
        # of (average book loan period / age of book in days)
        # (1 ≈ 1 loan every average book loan period)
        # Limits to two decimal places
        __PopularityRankings[Title] = float("{:.2f}".format(((__AverageBookLoanPeriod /
                                                              DB.CalculateLoanTime(PurchaseDate, "NotReturned")))))


def CalculateAverageBookLoanPeriod():
    """
    Calculates average number of days between withdrawals.

    Finds average number of days between withdrawals for each book and calculates mean
    """
    # for each log find count of loans and its age
    AverageBookLoanPeriodSample = []
    # For every log
    for Log in DB.GetAllLogs():
        Book = DB.GetDatabaseEntry(Log[0])
        # Finds number of times book has been withdrawn
        Count = 0
        for MatchingLogs in DB.GetAllLogs():
            if Log[0] == MatchingLogs[0]:
                Count += 1
        # Calculates average number of days between withdrawals
        AverageBookLoanPeriod = DB.CalculateLoanTime(
            Book[4], "NotReturned") / Count
        AverageBookLoanPeriodSample.append(AverageBookLoanPeriod)
    # Returns mean of average number of days between withdrawals for all books
    return sum(AverageBookLoanPeriodSample) / len(AverageBookLoanPeriodSample)


# Average number of days between withdrawals
__AverageBookLoanPeriod = CalculateAverageBookLoanPeriod()


def MergeSortRankings(RankingsArray):
    """
    Sorts rankings into descending order.

    This method uses a merge sort to sort the Rankings into descending order.
    It recursively repeats until the array has been divided into single elements.

    RankingsArray = The Rankings list that will be sorted

    Return: list: [[ID (String), Genre (String), Title (String), Author (String),
    PurchaseDate (String), MemberID (String), Ranking (int)]]
    """

    # If the unsorted array contains more then one element
    if(len(RankingsArray) > 1):
        # Finds the midpoint of the unsorted array
        MidPoint = len(RankingsArray)//2
        # Splits and copies the values between the two sub arrays
        LeftSubArray = RankingsArray[0:MidPoint]
        RightSubArray = RankingsArray[MidPoint:]
        # Recursively repeats the merge sort method
        MergeSortRankings(LeftSubArray)
        MergeSortRankings(RightSubArray)
        # Merges the two sub arrays
        MergeRankings(RankingsArray, LeftSubArray, RightSubArray)


def MergeRankings(SortedRankingsArray, LeftSubArray, RightSubArray):
    """
    This method merges the two sub arrays into a sorted array.

    SortedRankingsArray = The list that the left and right subarrays are being
    merged into (list: [ID, Genre, Title, Author, PurchaseDate, MemberID, Ranking])
    LeftSubArray = one of two subarrays that will be merged together
    (list: [ID, Genre, Title, Author, PurchaseDate, MemberID, Ranking])
    RightSubArray = one of two subarrays that will be merged together
    (list: [ID, Genre, Title, Author, PurchaseDate, MemberID, Ranking])
    """

    # Initial index pointer for merged array
    Index = 0
    # Initial index pointer for two sub arrays
    LeftIndex = 0
    RightIndex = 0
    # While loop until all values of one sub arrays are merged
    while(LeftIndex < len(LeftSubArray) and RightIndex < len(RightSubArray)):
        # Merges the left and right sub arrays
        if(LeftSubArray[LeftIndex][6] > RightSubArray[RightIndex][6]):
            SortedRankingsArray[Index] = LeftSubArray[LeftIndex]
            # Increments the left sub array index pointer
            LeftIndex += 1
        else:
            SortedRankingsArray[Index] = RightSubArray[RightIndex]
            # Increments the right sub array index pointer
            RightIndex += 1
        # Increments the merged array index pointer
        Index += 1

    # Adds remaining elements in the left sub array to the end of the merged array
    while(LeftIndex < len(LeftSubArray)):
        SortedRankingsArray[Index] = LeftSubArray[LeftIndex]

        LeftIndex += 1
        Index += 1

    # Adds remaining elements in the right sub array to the end of the merged array
    while(RightIndex < len(RightSubArray)):
        SortedRankingsArray[Index] = RightSubArray[RightIndex]

        RightIndex += 1
        Index += 1


def TestMergeSort():
    """
    Tests MergeSortRankings function with realistic book ranking data.

    Prints the list before and after sorting
    """
    print("\nTesting merge sort wtih realistic book rankings:")
    # Test book ranking data
    TestBookRanking = \
        [['1', 'Sci-Fi', 'Star Wars', 'Philip Harrington', '1-8-2010', 'aaaa', 16],
         ['2', 'Fantasy', 'The Lord of the Rings',
             'JRR Tolkien', '7-6-2012', 'aaaa', 26],
            ['4', 'Classic', 'Pride and Prejudice',
                'Jane Austen', '28-11-2000', 'bbbb', 8],
            ['8', 'Classic', 'To Kill a Mockingbird', 'Harper Lee', '28-11-1960', '0', 4]]
    print("Before sorting")
    # Prints book ranking data
    for TestRanking in TestBookRanking:
        print(TestRanking)
    # Sorts book ranking data with a merge sort
    MergeSortRankings(TestBookRanking)
    print("After sorting")
    # Prints sorted book ranking data
    for TestRanking in TestBookRanking:
        print(TestRanking)
    # Expects the unsorted list of books to be printed followed by the
    # sorted (by ranking in decending order) list of book printed


def TestInsertRanking():
    """
    Tests InsertRanking function with various genres and the genre frequency dictionary.

    Prints the contents of GenreRankings at the start and after each genre is entered
    """
    print("\nTesting insert ranking")
    # Prints genre ranking dictionary after inserting multiple genres
    print(__GenreRankings)
    # Expects "{}"
    InsertRanking(__GenreRankings, "Thriller")
    print(__GenreRankings)
    # Expects "{'Thriller': 1}"
    InsertRanking(__GenreRankings, "Thriller")
    print(__GenreRankings)
    # Expects "{'Thriller': 2}"
    InsertRanking(__GenreRankings, "Thriller")
    print(__GenreRankings)
    # Expects "{'Thriller': 3}"
    InsertRanking(__GenreRankings, "Sci-Fi")
    print(__GenreRankings)
    # Expects "{'Thriller': 3, 'Sci-Fi': 1}"
    InsertRanking(__GenreRankings, "Sci-Fi")
    print(__GenreRankings)
    # Expects "{'Thriller': 3, 'Sci-Fi': 2}"


def TestInsertPopularityRanking():
    """
    Tests InsertPopularityRanking function with various dates and titles

    Prints the contents of popularity at the start and after each title is entered
    """
    print("\nTesting insert popularity ranking")
    # Prints genre ranking dictionary after inserting multiple genres
    print(__PopularityRankings)
    # Expects "{}"
    InsertPopularityRanking("Star Wars", "1-8-2000")
    print(__PopularityRankings)
    # Expects "{'Star Wars': small value}"
    InsertPopularityRanking("Star Wars", "1-8-2000")
    print(__PopularityRankings)
    # Expects "{'Star Wars': 2 * small value}"
    InsertPopularityRanking("Star Wars", "1-8-2000")
    print(__PopularityRankings)
    # Expects "{'Star Wars': 3 * small value}"
    InsertPopularityRanking("Star Wars 2", "01-09-2021")
    print(__PopularityRankings)
    # Expects "{'Star Wars': 3 * small value, 'Star Wars 2': larger value}"
    InsertPopularityRanking("Star Wars 2", "01-09-2021")
    print(__PopularityRankings)
    # Expects "{'Star Wars': 3 * small value, 'Star Wars 2': 2 * larger value}"
    # Test results depend on current date hence the use of "small" and "larger" value


def TestCalculateAverageBookLoanPeriod():
    """
    Tests CalculateAverageBookLoanPeriod function.

    Prints returned values from function
    """
    print("\nTesting calculating average book loan period")

    print(CalculateAverageBookLoanPeriod())
    # Expects the sum of the average number of days between loan for each book
    # divided by the number of books (mean number of days between loan for all books)


def TestRankBooks():
    """
    Tests RankBooks function with "Adam" as member ID.

    Fist populates frequency dictionaries and read books list before ranking every book
    Then prints off returned list
    """
    print("\nTesting ranking books")
    # Wipes dictionaries and lists populated by previous recommendation
    global __GenreRankings
    __GenreRankings = {}
    global __AuthorRankings
    __AuthorRankings = {}
    global __PopularityRankings
    __PopularityRankings = {}
    global __ReadBooks
    __ReadBooks = []
    global __AverageBookLoanPeriod
    # Finds average book loan period (average number of days between two book withdrawals)
    __AverageBookLoanPeriod = CalculateAverageBookLoanPeriod()
    # For every log
    Logs = DB.GetAllLogs()
    for Log in Logs:
        Book = DB.GetDatabaseEntry(Log[0])
        # If the log has matching Member ID
        if Log[3] == "Adam":
            # Adds the genre of the book to GenreRankings
            InsertRanking(__GenreRankings, Book[1])
            # Adds the author of the book to AuthorRankings
            InsertRanking(__AuthorRankings, Book[3])
            # Adds book tile to list of read books
            if not Book[2] in __ReadBooks:
                __ReadBooks.append(Book[2])
        # Adds the title of the book to PopularityRankings
        InsertPopularityRanking(Book[2], Book[4])

    BookRankings = RankBooks()
    # Prints of returned list of book rankings
    for Ranking in BookRankings:
        print(Ranking)
    # Expects a list of all books in the database, each assigned a ranking
    # in no particular order


def TestRecommendBooks():
    """
    Tests RecommendBooks function with "Adam" as member ID.

    Then prints off returned list
    """
    # Prints recommended books for Adam
    print("\nTesting recommending book")
    RankedBooks = RecommendBooks("Adam")
    for Book in RankedBooks[0]:
        print(Book)
    # Expects a sorted (by ranking in descending order) list of the top 10 books
    # in the database, each assigned a ranking


if __name__ == "__main__":
    print("Testing bookrecommend.py")
    # Tests all functions in bookrecommend module

    TestMergeSort()

    TestInsertRanking()

    TestInsertPopularityRanking()

    TestCalculateAverageBookLoanPeriod()

    TestRankBooks()

    TestRecommendBooks()
