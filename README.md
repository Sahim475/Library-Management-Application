# Library-Management-Application
Library management application to allow library staff to manage book loans and analyse trends to give suitable recommendations to clients.
Uses Tkinter and Matplotlib for graphical user interface (GUI) and visualisation of data.

Python version 3.7 64-bit

Run menu.py to run the whole program.

Only member IDs consisting of 4 characters are valid
Multiple IDs can be entered separated by commas into ID entry fields

Test code for every function in a module (except menu.py) are at the bottom of the module
There is a separate function to test each function, towards the bottom of each test function are comment(s) describing the expected result

Testing the bookcheckout, bookreturn, and bookrecommend module will add (undesired) entries to the txt files
I recommend using the system first (running menu.py) before testing individual modules
Then testing bookcheckout.py before bookreturn.py then maybe remove the latest entry in logfile.txt (created during the tests)
After testing the database.py, maybe remove the latest entry in logfile.txt (created during the test)
Testing booksearch.py and bookrecommend.py does not alter the text files so testing them has no side effects

How to read book recommendation graph:
Overall length of bars show total recommendation ranking for the book
Different coloured sections of that bar show what different proportions of the overall ranking were based on (as indicated by key)

Below are some example "persona" members which may be useful when testing with member IDs such as testing
recommendations or returning books loaned for more than 60 days (names are member IDs):

Adam likes "Classics" and "Fantasy"
Jess likes "Thrillers" and "Romance"
Paul likes "Sci-Fi" a lot but tries some other books
Pool only reads "Sci-Fi" books
Eric reads all the genres: "Sci-Fi",""Classics","Fantasy","Thrillers","Romance"
Rick reads all the genres: "Sci-Fi",""Classics","Fantasy","Thrillers","Romance" and has read each book at least twice
Luke only reads "Romance"
Ryan has read one "Fantasy" book and nothing else
Liam has checked out all the "Star Wars" books and has not returned any of them after 60 days
Harv has only checked out harry potter books
John has read a variety of books very recently
Megg has only read from the "fifty shades" series


