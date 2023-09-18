"""
Displays GUI and provides funcionality needed to utilise other modules in project

Funtions:

Close()
DisplayError(String)
ClearTable()
ClearComponents(bool)
Cancel()
SearchGUI()
PreSearch()
ExactSearch()
CheckoutGUI()
Checkout()
ReturnGUI()
Return()
RecommendGUI()
Recommend()
ShowGraph()
CreateGraph([String], [int], [int], [int], [int], String) -> figure
SortBarRankings([(int, String, String)]) -> [(int, String, String)]
CreateCell(String, int, int, int, int) -> Entry
CreateTable([([String],bool)])
"""

# Imports functions and variable nedded from matplotlib
from matplotlib.pyplot import figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from numpy import right_shift
# Imports other modules accessed via menu
import booksearch
import bookcheckout
import bookreturn
import bookrecommend
# Imports functions and variable nedded from tkinter
from tkinter import *
from tkinter.font import BOLD

# GUI properties for some colours and fonts
__SmallFont = ("Helvetica", 10, BOLD)
__BigFont = ("Helvetica", 20, BOLD)
__TitleFont = ("Helvetica", 40)
__ButtonColour = '#83B0E1'
__ButtonHoldColour = '#71A5DE'
__BackgroundColour = '#F2F2F2'
__ForegroundColour = '#CCCCCC'
__TextColour = '#000000'
__EntryColour = '#F2F2F2'
__HighlightColour = '#AECBEB'
# Window creation and properties
__Window = Tk()
__Window.title("Libary Managment System")
__Window.geometry("700x538")
__Window.minsize(700, 538)
__Window.configure(background=__BackgroundColour)


def Close():
    """
    Ends program.

    CAlle upon window closure
    """
    # Ends program
    __Window.destroy()
    quit()


# Ends program on window close
__Window.protocol("WM_DELETE_WINDOW", Close)


def DisplayError(Error):
    """
    Displays message on GUI.

    Error = message to be displayed on GUI (String)
    """
    # Displays message on GUI
    ErrorMessage.configure(text=Error)


def ClearTable():
    """
    Removes table from GUI.
    """
    # Deletes all cells from previous table
    for Cell in __AllCells:
        Cell.destroy()
    __AllCells.clear()


def ClearComponents(IsMessage):
    """
    Hides most GUI components and returns GUI to defualt state.

    IsMessage = whether or not "please select an option" message is displayed (bool)
    """

    # Removes previous table
    ClearTable()
    # Removes error message
    DisplayError("")
    # Hides most GUI components
    BookTileText.lower()
    BookTileEntry.lower()
    IDText.lower()
    IDEntry.lower()
    MemberIDText.lower()
    MemberIDEntry.lower()
    ReturnIDText.lower()
    ReturnIDEntry.lower()
    CancelButton.lower()
    SearchButton.lower()
    CheckoutButton.lower()
    ReturnButton.lower()
    RecommendButton.lower()
    GraphCanvas.get_tk_widget().destroy()
    # Displays the "please select an option" message depending on the IsMessage boolean
    if IsMessage:
        BoxMessage.lift()
    else:
        BoxMessage.lower()


def Cancel():
    """
    Hides most GUI components and returns GUI to defualt state.

    Called on cancel button press
    """
    # On cancel button press

    # Hides most GUI components
    ClearComponents(True)


def SearchGUI():
    """
    Displays GUI componenets needed for seach option and hides others.

    Called on search option button press
    """
    # On search option button press

    # Hides most GUI components
    ClearComponents(False)
    # GUI components used for search displayed
    BookTileText.lift()
    BookTileEntry.lift()
    CancelButton.lift()
    SearchButton.lift()
    # Gets all books in database
    SearchResults = booksearch.PreSearchForBook(BookTileEntry.get())
    # If search results are not empty
    if SearchResults:
        # Adds column names
        SearchResults = [(["ID", "Genre", "Title", "Author",
                           "Purchase date", "Member ID"], False)]\
            + SearchResults
        # Creates table displaying search results
        CreateTable(SearchResults)
        # If search results are empty
    else:
        # Removes table
        ClearTable()


def PreSearch():
    """
    Searches for books with title including that entered into entry.

    Highlights all books currently loaned for more than 60 days that also
    meet search critea

    Called on key press in book search entry field
    """

    # On key press in book search entry field

    # Gets book title entered
    Title = BookTileEntry.get()
    # If something has been entered
    if Title != "":
        # Finds search results from looking up book title in database
        SearchResults = booksearch.PreSearchForBook(Title)
        # If search results are not empty
        if SearchResults:
            # Adds column names
            SearchResults = [(["ID", "Genre", "Title", "Author",
                               "Purchase date", "Member ID"], False)]\
                + SearchResults
            # Creates table displaying search results
            CreateTable(SearchResults)
        # If search results are empty
        else:
            # Removes table
            ClearTable()


def ExactSearch():
    """
    Searches for books with matching titles to that entered into entry.

    Highlights all books currently loaned for more than 60 days that also
    meet search critea

    Called on search button press
    """

    # On search button press

    # Gets book title entered
    Title = BookTileEntry.get()
    # If something has been entered
    if Title != "":
        # Finds search results from looking up the exact book title in database
        SearchResults = booksearch.SearchForBook(Title)
        # If search results are not empty
        if SearchResults:
            # Adds column names
            SearchResults = [(["ID", "Genre", "Title", "Author",
                               "Purchase date", "Member ID"], False)]\
                + SearchResults
            # Creates table displaying search results
            CreateTable(SearchResults)
        # If search results are empty
        else:
            # Removes table
            ClearTable()


def CheckoutGUI():
    """
    Displays GUI componenets needed for checkout option and hides others.

    Called on checkout option button press
    """
    # On checkout option button press

    # Hides most GUI components
    ClearComponents(False)
    # GUI components used for checkout displayed
    IDText.lift()
    IDEntry.lift()
    MemberIDText.lift()
    MemberIDEntry.lift()
    CancelButton.lift()
    CheckoutButton.lift()


def Checkout():
    """
    Checkout book with ID and member Id entered into entries.

    Pops first ID if IDs seperated by commas in entry
    Also displays all books currently loaned for more than 60 days by specified
    member with a table on the GUI

    Called on checkout button press
    """

    # On checkout button press

    # Gets IDs entered
    IDs = IDEntry.get().split(",")
    ID = ""
    # If IDs have been entered
    if IDs:
        # ID equals first ID entered
        ID = IDs[0]
        # Removes first ID entered from ID entry
        del(IDs[0])
        IDEntry.delete(0, "end")
        IDEntry.insert(0, ",".join(IDs))
    # Gets member ID entered
    MemberID = MemberIDEntry.get()
    # If member ID has not got a length of 4
    if not len(MemberID) == 4:
        # Displays "Invalid member ID" on GUI
        DisplayError("Invalid member ID\n(must be 4 characters)")
    # If member ID has a length of 4
    else:
        DisplayError("")
        # Attempts to checkout book with sepcified ID with specified member ID
        Results = bookcheckout.CheckoutBook(ID, MemberID)
        # Displays returned message to GUI
        DisplayError(Results[0])
        # All results are not to be highlighted
        for i in range(len(Results[1])):
            Results[1][i] = ([Results[1][i][0]] + Results[1][i][1], False)
        # If result is populated
        if Results[1]:
            # Appends column names to results
            Results = [(["Loaned days", "ID", "Genre", "Title", "Author",
                         "Purchase date", "Member ID"], False)]\
                + Results[1]
            # Creates table using results
            CreateTable(Results)
        # If results are empty
        else:
            # Removes table
            ClearTable()


def ReturnGUI():
    """
    Displays GUI componenets needed for return option and hides others.

    Called on return option button press
    """
    # On return option button press

    # Hides most GUI components
    ClearComponents(False)
    # GUI components used for return displayed
    ReturnIDText.lift()
    ReturnIDEntry.lift()
    CancelButton.lift()
    ReturnButton.lift()


def Return():
    """
    Returns book with ID entered into entry.

    Pops first ID if IDs seperated by commas in entry

    Called on return button press
    """
    # On return button pressed

    # Gets IDs entered
    IDs = ReturnIDEntry.get().split(",")
    ID = ""
    # If IDs have been entered
    if IDs:
        # ID equals first ID entered
        ID = IDs[0]
        # Removes first ID entered from ID entry
        del(IDs[0])
        ReturnIDEntry.delete(0, "end")
        ReturnIDEntry.insert(0, ",".join(IDs))

    # Attempts to return book with specified ID
    Message = bookreturn.ReturnBook(ID)
    # Displays returned message on GUI
    DisplayError(Message)


def RecommendGUI():
    """
    Displays GUI componenets needed for recommend option and hides others.

    Called on recommend option button press
    """
    # On recommend option button press

    # Hides most GUI components
    ClearComponents(False)
    # GUI components used for recommending displayed
    MemberIDText.lift()
    MemberIDEntry.lift()
    CancelButton.lift()
    RecommendButton.lift()


def Recommend():
    """
    Gets and displays book recommendation ranking table on GUI.

    Called on recommend button press
    """
    # On recommend button press

    # Gets member ID entered
    MemberID = MemberIDEntry.get()
    # If member ID has not got a length of 4
    if not len(MemberID) == 4:
        # Displays "Invalid member ID" on GUI
        DisplayError("Invalid member ID\n(must be 4 characters)")
    # If member ID has a length of 4
    else:
        DisplayError("")
        # Gets recommended books for the specified member
        BookRecommendations = bookrecommend.RecommendBooks(MemberID)[0]
        # All results are not to be highlighted
        for i in range(len(BookRecommendations)):
            BookRecommendations[i] = (BookRecommendations[i], False)
        # If recommended books is populated
        if BookRecommendations:
            # Appends column names to recommended books
            BookRecommendations = [(["ID", "Genre", "Title", "Author",
                                    "Purchase date", "Member ID", "Ranking"], False)]\
                + BookRecommendations
            # Creates table using recommended books
            CreateTable(BookRecommendations)
        # If recommended books is empty
        else:
            # Removes table
            ClearTable()


def ShowGraph():
    """
    Gets and displays book recommendation ranking bar chart on GUI.

    Called on graph button press
    """
    # On graph button press

    # Gets member ID entered
    MemberID = MemberIDEntry.get()
    # If member ID has not got a length of 4
    if not len(MemberID) == 4:
        # Displays "Invalid member ID" on GUI
        DisplayError("Invalid member ID\n(must be 4 characters)")
    # If member ID has a length of 4
    else:
        DisplayError("")
        # Gets recommended books for the specified member
        Results = bookrecommend.RecommendBooks(MemberID)
        BookRecommendations = Results[0]
        GenreRecommendationRankings = Results[1]
        AuthorRecommendationRankings = Results[2]
        PopularityRecommendationRankings = Results[3]
        # If recommended books is populated
        if BookRecommendations:
            Books = []
            Rankings = []
            GenreRanks = []
            AuthorRanks = []
            PopularityRanks = []
            # Loops through all recommended books
            for i in range(len(BookRecommendations)):
                # Gets title of recommended book
                Title = BookRecommendations[i][2]
                # Adds title to books list (Y axis data)
                Books.append(Title)
                # Adds ranking to recommendation rankings list (X axis data)
                Rankings.append(BookRecommendations[i][6])
                # Adds ranking for genres
                if BookRecommendations[i][1] in GenreRecommendationRankings:
                    GenreRanks.append(
                        GenreRecommendationRankings[BookRecommendations[i][1]] * 4)
                else:
                    GenreRanks.append(0)
                # Adds ranking for authors
                if BookRecommendations[i][3] in AuthorRecommendationRankings:
                    AuthorRanks.append(
                        AuthorRecommendationRankings[BookRecommendations[i][3]] * 2)
                else:
                    AuthorRanks.append(0)
                # Adds ranking for popularity
                if BookRecommendations[i][2] in PopularityRecommendationRankings:
                    PopularityRanks.append(
                        PopularityRecommendationRankings[BookRecommendations[i][2]])
                else:
                    PopularityRanks.append(0)
            # Creates graph on GUI
            fig = CreateGraph(Books, Rankings, GenreRanks,
                              AuthorRanks, PopularityRanks, MemberID)
            global GraphCanvas
            GraphCanvas.get_tk_widget().destroy()
            GraphCanvas = FigureCanvasTkAgg(fig, master=__Window)
            GraphCanvas.draw()
            GraphCanvas.get_tk_widget().place(relx=0.5, x=0, y=415,
                                              anchor=CENTER, height=214, width=668)
        # If recommended books is empty
        else:
            # Removes graph
            GraphCanvas.get_tk_widget().destroy()

        # Removes previous table
        ClearTable()


def CreateGraph(Books, Rankings, GenreRankings, AuthorRanking, PopularityRankings, MemberID):
    """
    Creates a bar chart graph with books on Y axis and recommendation ranking on X axis.

    Multiple overlapping bars show rankings for genre, author, popularity, and overall ranking

    Books = Y axis data (book titles) ([String])
    Rankings = X axis data (book recommendation ranking) ([int])
    GenreRankings = X axis data (proportion of ranking based on genre) ([int])
    AuthorRanking = X axis data (proportion of ranking based on author) ([int])
    PopularityRankings = X axis data (proportion of ranking based on popularity) ([int])
    MemberID = ID of member the graph represents recommmendations for (String)

    Return: graph (figure)
    """
    # Creates bar chart with book titles on Y axis and recommendation ranking on x axis
    plt.rcParams.update({'font.size': 8})
    fig = plt.figure()
    plt.gcf().subplots_adjust(left=0.36)
    axis = fig.add_subplot(1, 1, 1)
    axis.title.set_text('Book Recommendation Rankings for ' + MemberID)
    # For each bar in the bar chart
    for i in range(len(Books)):
        # Creates list of bar charts rankings, colour, and title
        Title = Books[i]
        BarRankings = [(GenreRankings[i], "red", "Genre"),
                       (AuthorRanking[i], "green", "Author"),
                       (PopularityRankings[i], "orange", "Popularity")]
        # Sorts bar chart list by ranking values
        BarRankings = SortBarRankings(BarRankings)
        BarValue = 0
        # Displays bars on graph - different colour bars show what each
        # proportion of total ranking is based on
        for j in range(len(BarRankings)):
            axis.barh(Title, Rankings[i] - BarValue,
                      color=BarRankings[j][1], label=BarRankings[j][2])
            BarValue += BarRankings[j][0]
    # Adds legend to graph with only unique labels
    labels = axis.get_legend_handles_labels()[1]
    uniqueLabels = []
    for i in range(len(labels)):
        if(labels[i] not in labels[:i]):
            uniqueLabels.append(labels[i])
    axis.legend(uniqueLabels, loc='lower right')
    # Inverts y axis
    axis.invert_yaxis()
    axis.set_anchor('E')
    # Returns created graph
    return fig


def SortBarRankings(BarRankings):
    """
    Sorts single bar chart rankings into descending order.

    Uses insertion sort

    BarRankings = list of bar chart rankins (list:[(Ranking, colour, label)])

    Return: list:[(Ranking (int), Colour (String), Label (String))]
    """
    BarRankingsSorted = []
    # Sorts using insertion sort
    for i in range(len(BarRankings)):
        Added = False
        for j in range(len(BarRankingsSorted)):
            if(BarRankingsSorted[j][0] < BarRankings[i][0]):
                BarRankingsSorted.insert(j, BarRankings[i])
                Added = True
                break
        if not Added:
            BarRankingsSorted.append(BarRankings[i])
    # Returns sorted list
    return BarRankingsSorted


# Title creation and properties
Title = LabelFrame(__Window, text='Library Management System', background=__BackgroundColour,
                   fg=__TextColour)
Title.configure(font=__TitleFont)
Title.place(relx=0.5, y=35, anchor=CENTER, height=70, width=684)
# Search option creation and properties
SearchOption = Button(__Window, text='Search for book', command=SearchGUI,
                      background=__ButtonColour, activebackground=__ButtonHoldColour,
                      fg=__TextColour)
SearchOption.configure(font=__BigFont)
SearchOption.place(relx=0.5, x=-217, y=100,
                   anchor=CENTER, height=50, width=250)
# Checkout option creation and properties
CheckoutOption = Button(__Window, text='Checkout book', command=CheckoutGUI,
                        background=__ButtonColour, activebackground=__ButtonHoldColour,
                        fg=__TextColour)
CheckoutOption.configure(font=__BigFont)
CheckoutOption.place(relx=0.5, x=-217, y=155,
                     anchor=CENTER, height=50, width=250)
# Return option creation and properties
ReturnOption = Button(__Window, text='Return book', command=ReturnGUI,
                      background=__ButtonColour, activebackground=__ButtonHoldColour,
                      fg=__TextColour)
ReturnOption.configure(font=__BigFont)
ReturnOption.place(relx=0.5, x=-217, y=210,
                   anchor=CENTER, height=50, width=250)
# Recommend option creation and properties
RecommendOption = Button(__Window, text='Recommend book', command=RecommendGUI,
                         background=__ButtonColour, activebackground=__ButtonHoldColour,
                         fg=__TextColour)
RecommendOption.configure(font=__BigFont)
RecommendOption.place(relx=0.5, x=-217, y=265,
                      anchor=CENTER, height=50, width=250)
# Box label creation and properties
BoxLabel = Label(__Window, borderwidth=1, relief="ridge", background=__ForegroundColour,
                 fg=__TextColour)
BoxLabel.place(relx=0.5, x=130, y=182, anchor=CENTER, height=215, width=424)
# Box message creation and properties
BoxMessage = Label(__Window, text="Please select an option on the left.",
                   font=__SmallFont, background=__ForegroundColour, fg=__TextColour)
BoxMessage.place(relx=0.5, x=130, y=182, anchor=CENTER, height=115, width=400)
# Error message creation and properties
ErrorMessage = Label(__Window, text="", font=__SmallFont,
                     background=__ForegroundColour, fg=__TextColour)
ErrorMessage.place(relx=0.5, x=130, y=262, anchor=CENTER, height=30, width=400)
# Book title text creation and properties
BookTileText = Label(__Window, text="Book title",
                     background=__EntryColour, fg=__TextColour)
BookTileText.place(relx=0.5, x=-25, y=182, anchor=CENTER, height=30, width=80)
# Book title entry creation and properties
BookTileEntry = Entry(
    __Window, bd=5, background=__EntryColour, fg=__TextColour)
BookTileEntry.place(relx=0.5, x=175, y=182,
                    anchor=CENTER, height=30, width=300)
BookTileEntry.bind("<KeyRelease>", lambda event, arg=(0): PreSearch())
# ID text creation and properties
IDText = Label(__Window, text="ID", background=__EntryColour, fg=__TextColour)
IDText.place(relx=0.5, x=-25, y=142, anchor=CENTER, height=30, width=80)
# ID entry creation and properties
IDEntry = Entry(__Window, bd=5, background=__EntryColour, fg=__TextColour)
IDEntry.place(relx=0.5, x=175, y=142, anchor=CENTER, height=30, width=300)
# Member ID text creation and properties
MemberIDText = Label(__Window, text="Member ID",
                     background=__EntryColour, fg=__TextColour)
MemberIDText.place(relx=0.5, x=-25, y=182, anchor=CENTER, height=30, width=80)
# Member ID entry creation and properties
MemberIDEntry = Entry(
    __Window, bd=5, background=__EntryColour, fg=__TextColour)
MemberIDEntry.place(relx=0.5, x=175, y=182,
                    anchor=CENTER, height=30, width=300)
# Return ID text creation and properties
ReturnIDText = Label(__Window, text="ID",
                     background=__EntryColour, fg=__TextColour)
ReturnIDText.place(relx=0.5, x=-25, y=182, anchor=CENTER, height=30, width=80)
# Return ID entry creation and properties
ReturnIDEntry = Entry(
    __Window, bd=5, background=__EntryColour, fg=__TextColour)
ReturnIDEntry.place(relx=0.5, x=175, y=182,
                    anchor=CENTER, height=30, width=300)
# Cancel button creation and properties
CancelButton = Button(__Window, text='Cancel', command=Cancel, font=__SmallFont,
                      background=__ButtonColour, activebackground=__ButtonHoldColour,
                      fg=__TextColour)
CancelButton.place(relx=0.5, x=30, y=222, anchor=CENTER, height=30, width=190)
# Search button creation and properties
SearchButton = Button(__Window, text='Exact Search', command=ExactSearch, font=__SmallFont,
                      background=__ButtonColour, activebackground=__ButtonHoldColour,
                      fg=__TextColour)
SearchButton.place(relx=0.5, x=230, y=222, anchor=CENTER, height=30, width=190)
# Checkout button creation and properties
CheckoutButton = Button(__Window, text='Checkout', command=Checkout, font=__SmallFont,
                        background=__ButtonColour, activebackground=__ButtonHoldColour,
                        fg=__TextColour)
CheckoutButton.place(relx=0.5, x=230, y=222,
                     anchor=CENTER, height=30, width=190)
# Return button creation and properties
ReturnButton = Button(__Window, text='Return', command=Return, font=__SmallFont,
                      background=__ButtonColour, activebackground=__ButtonHoldColour,
                      fg=__TextColour)
ReturnButton.place(relx=0.5, x=230, y=222, anchor=CENTER, height=30, width=190)
# Recommend button creation and properties
RecommendButton = Button(__Window, text='Recommend', command=Recommend,
                         font=__SmallFont, background=__ButtonColour,
                         activebackground=__ButtonHoldColour,
                         fg=__TextColour)
RecommendButton.place(relx=0.5, x=180, y=222,
                      anchor=CENTER, height=30, width=90)
# Graph button creation and properties
GraphButton = Button(__Window, text='Graph', command=ShowGraph, font=__SmallFont,
                     background=__ButtonColour, activebackground=__ButtonHoldColour,
                     fg=__TextColour)
GraphButton.place(relx=0.5, x=280, y=222, anchor=CENTER, height=30, width=90)
# Big box label creation and properties
BigBoxLabel = Label(__Window, borderwidth=1, relief="ridge",
                    background=__ForegroundColour, fg=__TextColour)
BigBoxLabel.place(relx=0.5, x=0, y=415, anchor=CENTER, height=230, width=684)
# Graph canvas creation and properties
GraphCanvas = FigureCanvasTkAgg(figure(), master=__Window)

# All table cells
__AllCells = []


def CreateCell(EntryData, X, Y, XWidth, YWidth):
    """
    Creates a cell at the specified coordinates with specified demensions and data.

    EntryData = data displayed by this cell (String)
    X = x coordinate of this new cell (int)
    Y = y coordinate of this new cell (int)
    XWidth = width of this new cell (int)
    YWidth = height of this new cell (int)

    Return: Cell (Entry)
    """
    # Creates new cell
    Cell = Entry(__Window, width=20, font=__SmallFont)
    # Checks if entry is an float
    try:
        # If entry is an float then limits it to two decimal places
        float(EntryData)
        EntryData = ("%.2f" % (EntryData))
    except:
        pass
    # Returns true if it is an integer
    # Inserts data into cell
    Cell.insert(END, EntryData)
    # Sets bounds for new cell
    Cell.place(relx=0.5, x=X - 334 + XWidth//2, y=Y + 308 + YWidth//2,
               anchor=CENTER, height=YWidth, width=XWidth)
    # Makes entry read only
    Cell.bind("<Key>", lambda e: "break")
    # Adds cell to list of all cells
    __AllCells.append(Cell)
    # Returns the new cell
    return Cell


def CreateTable(Data):
    """
    Creates a table on the GUI that displays the specified data.

    Adjust the number of colums and rows to match that of the specified data
    bool appended to every entry in data corresponds to whether row is highlighted

    Data = data displayed by the table (list: [([String],bool)])
    """
    # Removes previous table
    ClearTable()
    # Number of columns in the table
    Columns = len(Data[0][0])
    # Number of rows in the table
    Rows = len(Data)
    # Table properties
    TableHeight = 214
    TableWidth = 668
    WidthPointer = 0
    HeightPointer = 0
    # Calculates cell width and height
    CellWidth = TableWidth // Columns
    CellHeight = TableHeight // Rows
    # For all rows and columns but the last ones
    for i in range(Rows - 1):
        for j in range(Columns - 1):
            # Creates cell at specified position pointer with specified data
            e = CreateCell(Data[i][0][j], WidthPointer, HeightPointer,
                           CellWidth, CellHeight)
            # Highlights cell if cell is to be highlighted
            if Data[i][1]:
                e.configure(background=__HighlightColour)
            # Increments width pointer bt the cell width
            WidthPointer += CellWidth
        # Creates cell at last column with width equal to the
        # table width - the width of all the cells of its left
        e = CreateCell(Data[i][0][Columns - 1], WidthPointer, HeightPointer,
                       TableWidth - WidthPointer, CellHeight)
        # Highlights cell if cell is to be highlighted
        if Data[i][1]:
            e.configure(background=__HighlightColour)
        # Resets width pointer to 0 because start of new row
        WidthPointer = 0
        # Increments height pointer bt the cell height
        HeightPointer += CellHeight
    # For all columns but the last one
    for j in range(Columns - 1):
        # Creates cell at last row with height equal to the
        # table height - the height of all the cells above it
        e = CreateCell(Data[Rows-1][0][j], WidthPointer, HeightPointer,
                       CellWidth, TableHeight - HeightPointer)
        # Highlights cell if cell is to be highlighted
        if Data[Rows-1][1]:
            e.configure(background=__HighlightColour)
        # Increments width pointer bt the cell width
        WidthPointer += CellWidth
    # Creates cell at last row and last column with height equal to the
    # table height - the height of all the cells above it and width equal to the
    # table width - the width of all the cells of its left
    e = CreateCell(Data[Rows-1][0][Columns - 1], WidthPointer, HeightPointer,
                   TableWidth - WidthPointer, TableHeight - HeightPointer)
    # Highlights cell if cell is to be highlighted
    if Data[Rows-1][1]:
        e.configure(background=__HighlightColour)


# Hides most GUI components
ClearComponents(True)

# Displays GUI
__Window.mainloop()

# GUI and functions thoroughly tested
# GUI components are correctly located, scale correctly, and function as intended
# Table displays on GUI correctly with rows and columns corrisponding to table data
# Graph displays on GUI correctly with bar chart data
# Buttons have correct functionality
