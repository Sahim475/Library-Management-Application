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
