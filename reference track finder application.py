# Ryder Katz
#
# This program uses the track data loaded into the .txt file within the program folder to 
# match audio feature characteristics to possible reference tracks
#
# In order for the program to work, the user must have:
#       tkinter, os, PIL, and time modules
#       'filePath' adjusted to the path on the user's computer to the 'Reference Song Data.txt' file
#       'os.chdir' adjusted to the path on the user's computer to the 'Reference Track Finder Program' folder
#



# this program uses tkinter, os, PIL, and time for the GUI
import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk
import time


# this is the path to the file that has already been loaded with data via reference track data loader
filePath = '/Users/ryderkatz/Documents/Python Projects/Reference Track Finder Program/Reference Song Data.txt'

# this points to a folder containing the image files to be used in the program
os.chdir('/Users/ryderkatz/Documents/Python Projects/Reference Track Finder Program')


# this dictionary is used to convert the integer corresponding to each minor key into its corresponding str value
minorTones = {0:'Am', 1:'A#m', 2:'Bm', 3:'Cm', 4:'C#m',
         5:'Dm', 6:'D#m', 7:'Em', 8:'Fm', 9:'F#m',
         10:'Gm', 11:'G#m'}


# this function converts a text input corresponding to a minor key to its corresponding numerical index
def findMinorKey(key):
    #returns -1 if key is not found
    if key.lower() == 'am':
        toneNum = 0
    elif key.lower() == 'a#m':
        toneNum = 1
    elif key.lower() == 'bm':
        toneNum = 2
    elif key.lower() == 'cm':
        toneNum = 3
    elif key.lower() == 'c#m':
        toneNum = 4
    elif key.lower() == 'dm':
        toneNum = 5
    elif key.lower() == 'd#m':
        toneNum = 6
    elif key.lower() == 'em':
        toneNum = 7
    elif key.lower() == 'fm':
        toneNum = 8
    elif key.lower() == 'f#m':
        toneNum = 9
    elif key.lower() == 'gm':
        toneNum = 10
    elif key.lower() == 'g#m':
        toneNum = 11
    else:
        toneNum = -1
    return toneNum



# this function narrows down the possible tracks by key
def findKeyMatches(possibleTracks):
    global userEntry
    validInput = False
    printToWindow(f'What key is your song in (in minor)?')
    while not validInput:
        userKey = myInput()
        disableInput()
        minorSearch = findMinorKey(userKey)
        if minorSearch >= 0:
            confirmedKey = minorSearch
            validInput = True
        else:
            printToWindow('Please try again. Input only 3 characters (ex: Am or A#m).')

    validInput = False
    printToWindow(f'What is the max number of keys pitched DOWN that would still work?')
    while not validInput:
        userMin = myInput()
        disableInput()
        try:
            if 11 >= int(userMin) >= 0:
                userMin = int(userMin)
                validInput = True
            else:
                printToWindow('Your input must be between 0 and 11.')
        except:
            printToWindow('Please enter a valid input (int between 0 and 11).')
    if 11 >= (confirmedKey - userMin) >= 0:
        keyMin = confirmedKey - userMin
    else:
        keyMin = confirmedKey - userMin + 12
    
    validInput = False
    printToWindow(f'What is the max number of keys pitched UP that would still work?')
    while not validInput:
        userMax = myInput()
        disableInput()
        try:
            if 11 >= int(userMax) >= 0:
                userMax = int(userMax)
                validInput = True
            else:
                printToWindow('Your input must be between 0 and 11.')
        except:
            printToWindow('Please enter a valid input (int between 0 and 11).')
    if 11 >= (confirmedKey + userMax) <= 11:
        keyMax = confirmedKey + userMax
    else:
        keyMax = confirmedKey + userMin - 12

    if confirmedKey >= keyMin:
        if confirmedKey <= keyMax:
            inBetween = True
    else:
        inBetween = False
    
    confirmedTracks = set()
    if inBetween:
        for track in possibleTracks:
            if keyMax >= track[1] >= keyMin:
                confirmedTracks.add(track)
    else:
        for track in possibleTracks:
            if track[1] >= keyMin or track[1] <= keyMax:
                confirmedTracks.add(track)

    return confirmedTracks



# this function narrows down the possible tracks by tempo
def findTempoMatches(possibleTracks):
    validInput = False
    printToWindow(f'What tempo is your song in?')
    while not validInput:
        userTempo = myInput()
        disableInput()
        try:
            if 200 >= int(userTempo) >= 0:
                confirmedTempo = int(userTempo)
                validInput = True
            else:
                printToWindow('Your input must be between 0 and 200.')
        except: 
            printToWindow('Please try again. Input only numeric characters.')

    validInput = False
    printToWindow(f'What is the max bpm SLOWER that would still work?')
    while not validInput:
        userMin = myInput()
        disableInput()
        try:
            if int(userMin) >= 0 and confirmedTempo - int(userMin) >= 0:
                tempoMin = confirmedTempo - int(userMin)
                validInput = True
            else:
                printToWindow(f'Your input must be less than {confirmedTempo}.')
        except:
            printToWindow(f'Please enter a valid input (int less than {confirmedTempo}).')

    validInput = False
    printToWindow(f'What is the max bpm FASTER that would still work?')
    while not validInput:
        userMax = myInput()
        disableInput()
        try:
            if int(userMax) <= 200 and 200 - confirmedTempo >= 0:
                tempoMax = confirmedTempo + int(userMax)
                validInput = True
            else:
                printToWindow(f'Your input must be less than {200 - confirmedTempo}.')
        except:
            printToWindow(f'Please enter a valid input (int less than {200 - confirmedTempo}).')

    confirmedTracks = set()
    for track in possibleTracks:
        if tempoMin <= round(track[2]) <= tempoMax:
            confirmedTracks.add(track)

    return confirmedTracks



# this function displays the resulting tracks and their data to the tkinter treeview widget
def displayToTree(trackData):
    organizedData = set()
    for track in trackData:
        decAdjust = []
        for i in range(3,7):
            decAdjust.append(f'{track[i]:.2f}')
        rearranged = (track[0],track[7],minorTones[track[1]],round(track[2]),decAdjust[0],decAdjust[1],decAdjust[2],decAdjust[3])
        organizedData.add(rearranged)
    for track in organizedData:
        refOutput.insert('', 'end', values =track)



# this function reads and organizes the data from the file 
# it then launches the key and tempo specificer functions
# it then triggers the displayToTree function to display the results
def referencesFromFile(filePath):
    with open(filePath,'r') as file:
        data = file.readlines()
    trackFeatures = set()
    for line in data:
        lineParts = line.split(',,')
        trackData = []
        for part in lineParts:
            trackData.append(part)
        trackData[1] = int(trackData[1])
        for i in range(2,7):
            trackData[i] = float(trackData[i])
        trackData = tuple(trackData)
        trackFeatures.add(trackData)
    songFeats = findTempoMatches(findKeyMatches(trackFeatures))
    printToWindow('possible references loading')
    displayToTree(songFeats)




# these global variables will be used in the tkinter programming
programRunning = True
windowRun = True
textOutput = ''
textInput = ''


#
# the following functions integrate the main program functions with the tkinter gui
# this makes future use easier and more accessible than using the terminal
#

def refFromFile():
    try: 
        disableInput()
        refButton.destroy()
        global refNumber
        global refOutData
        if refNumber > 1:
            refOutput.delete(*refOutput.get_children())
        referencesFromFile(filePath)
        makeRefButton()
    except:
        pass


def quitWindow():
    global windowRun
    windowRun = False
    root.destroy()


def myPrint(x):
    textStr = ''
    for char in x:
        textStr = f"{textStr}{char}"
        textOut.config(text=textStr)
        textOut.update()
        time.sleep(.005)


def textOutputUpdate():
    global textOutput
    global textOut
    global windowRun
    if windowRun:
        myPrint(textOutput)


def printToWindow(text):
    global textOutput
    textOutput = text
    if windowRun:
        textOutputUpdate()


def clearBox():
    textBox.delete(0,tk.END)


userEntry = False
def onEnter(event):
    global userEntry
    global textInput
    text = textBox.get()
    textBox.delete(0,tk.END)
    textInput = text


def onClosing():
    global programRunning
    global windowRun
    programRunning = False
    windowRun = False
    root.destroy()


def disableInput():
    textBox.config(state='disabled')


def waitForInput():
    global windowRun
    global textInput
    global programRunning
    while programRunning:
        while windowRun:
            root.update_idletasks()
            root.update()
            if textInput:
                return textInput
            time.sleep(0.1)


def myInput():
    global textInput
    textBox.config(state='normal')
    textBox.focus_set()
    waitForInput()
    userInput = textInput
    textInput = ''
    return userInput



# 
# the following program segments create and organize the tkinter gui
# the tkinter elements are mapped to trigger the functions above that were created for use with tkinter 
#


root = tk.Tk()
root.title('Reference Track Finder')
root.minsize(width=root.winfo_width(), height=400)


textOut = ttk.Label(root, text=' ')
textOut.grid(row=11, column=0, columnspan=4, rowspan=1)
textOut.configure(font=("San Francisco", 15))


refButton = ttk.Button(root, text='find a reference track from file', command=refFromFile)
refButton.grid(row=15, column=0, columnspan=2, rowspan=1)
refNumber = 1
def makeRefButton():
    global refNumber
    refButton = ttk.Button(root, text='find another reference track from file', command=refFromFile)
    refButton.grid(row=15, column=0, columnspan=2, rowspan=1)
    refNumber += 1


programImage = 'referenceTrackFinderGraphic.png'
programImagePath = os.path.join(os.getcwd(), programImage)
logo = Image.open(programImagePath)
logo = logo.resize((500, 200))
logoDisplay = ImageTk.PhotoImage(logo)
logoFrame = tk.Label(root, image=logoDisplay)
logoFrame.grid(row=0, column=0, columnspan=2, rowspan=10, sticky='N')


textBox = ttk.Entry(root,
    background="white",
    width=20,
)
textBox.grid(row=12, column=0, columnspan=2, rowspan=2)
textBox.configure(font=("San Francisco", 15))
textBox.bind("<Return>", onEnter)
disableInput()


refOutData = []
refOutputFrame = tk.Frame(root, background='white')
refOutput = ttk.Treeview(refOutputFrame, columns = ('Song Title','Artist','Key','Tempo','Loudness',
                                          'Energy','Danceability','Valence'), show = 'headings', height=20)
refOutput.heading('Song Title',text='Song Title')
refOutput.heading('Artist',text='Artist')
refOutput.heading('Key',text='Key')
refOutput.heading('Tempo',text='Tempo')
refOutput.heading('Loudness',text='Loudness')
refOutput.heading('Energy',text='Energy')
refOutput.heading('Danceability',text='Danceability')
refOutput.heading('Valence',text='Valence')
columnWidths = (150,150,100,100,100,100,100,100)
for col, width in enumerate(columnWidths):
    refOutput.column(col, width=width)


def makeRefOutput():
    refOutput.grid(row=0,rowspan=20, column= 4,columnspan=8)
    refOutputFrame.grid(row=0,rowspan=20, column=4,columnspan=8, sticky='N')
makeRefOutput()


scrollBar = tk.Scrollbar(root, command=refOutput.yview)
refOutput.configure(yscrollcommand=scrollBar.set)
scrollBar.grid(column=12, row=0, rowspan= 20, sticky=('N','S'))


root.protocol("WM_DELETE_WINDOW", onClosing)

root.mainloop()