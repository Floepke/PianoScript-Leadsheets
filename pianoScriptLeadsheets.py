#!/usr/local/bin/python
# PianoScript Diagram Creator(PDC) is a tool for creating piano-
# keyboard diagrams. Example chord: [c2 c3 / c e g / x / y ]

import sys, os, platform

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk

    py3 = False
except ImportError:
    import tkinter.ttk as ttk

    py3 = True

from tkinter import END, filedialog, messagebox, scrolledtext
import tkinter.font as font

root = tk.Tk()

# Color management
_bg = 'grey85'  # X11 color: 'gray85'
_fg = '#000000'  # X11 color: 'black'
_compcolor = 'gray85' # X11 color: 'gray85'
_ana1color = 'gray85' # X11 color: 'gray85'
_ana2color = '#ececec' # Closest X11 color: 'gray92'
bgr = "grey"

#########################################################
# Build Graphical Userinterface                         #
#########################################################

def buildGUI():
    root.style = ttk.Style()
    root.style.theme_use('default')  # winnative
    root.style.configure('.', background=_bg)
    root.style.configure('.', foreground=_fg)
    root.style.configure('.', font="TkDefaultFont")
    root.style.map('.', background=
    [('selected', _compcolor), ('active', _ana2color)])
    root.geometry(f"{int(root.winfo_screenwidth())}x{int(root.winfo_screenheight())}+0+0")
    root.resizable(1, 1)
    root.configure(relief="ridge")
    root.configure(highlightcolor="black")
    root.protocol("WM_DELETE_WINDOW", exitRoot)

    root.TPanedwindow1 = ttk.Panedwindow(root, orient="horizontal")
    root.TPanedwindow1.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
    root.TPanedwindow1.configure(takefocus="0")
    root.TPanedwindow1_p1 = ttk.Labelframe(width=500, text='Editor')
    root.TPanedwindow1.add(root.TPanedwindow1_p1, weight=0)
    root.TPanedwindow1_p2 = ttk.Labelframe(text='Preview')
    root.TPanedwindow1.add(root.TPanedwindow1_p2, weight=0)

    root.Texteditor = tk.Text(root.TPanedwindow1_p1)
    root.Texteditor.place(relx=0, rely=0, relheight=1
            , relwidth=1, bordermode='ignore')
    root.Texteditor.configure(background=bgr)
    root.Texteditor.configure(font=("Helvetica", 16))
    root.Texteditor.configure(insertborderwidth="3")
    root.Texteditor.configure(selectbackground="#c4c4c4")
    root.Texteditor.configure(wrap="word", relief='flat', 
                            fg='white', 
                            insertbackground='white')

    root.CanvasPage = tk.Canvas(root.TPanedwindow1_p2)
    root.CanvasPage.place(relx=0, rely=0, relheight=1
            , relwidth=1, bordermode='ignore')
    root.CanvasPage.configure(borderwidth="2")
    root.CanvasPage.configure(relief="flat")
    root.CanvasPage.configure(selectbackground="#f4f4f4")
    root.CanvasPage.configure(takefocus="0", bg=bgr)

    root.menubar = tk.Menu(root,font="TkMenuFont",bg=_bg,fg=_fg)
    root.configure(menu = root.menubar)

    root.sub_menu = tk.Menu(root,tearoff=0)
    root.menubar.add_cascade(menu=root.sub_menu,
            activebackground="#ececec",
            activeforeground="#000000",
            background=_bg,
            font="TkMenuFont",
            foreground="#000000",
            label="File")
    root.sub_menu.add_command(
            activebackground="#ececec",
            activeforeground="#000000",
            background=_bg,
            font="TkMenuFont",
            foreground="#000000",
            label="New", 
            command=newFile)
    root.sub_menu.add_command(
            activebackground="#ececec",
            activeforeground="#000000",
            background=_bg,
            font="TkMenuFont",
            foreground="#000000",
            label="Open", 
            command=openFile)
    root.sub_menu.add_command(
            activebackground="#ececec",
            activeforeground="#000000",
            background=_bg,
            font="TkMenuFont",
            foreground="#000000",
            label="Save", 
            command=saveFile)
    root.sub_menu.add_command(
            activebackground="#ececec",
            activeforeground="#000000",
            background=_bg,
            font="TkMenuFont",
            foreground="#000000",
            label="Save as...", 
            command=saveFileAs)
    root.sub_menu.add_separator(
            background=_bg)
    root.sub_menu.add_command(
            activebackground="#ececec",
            activeforeground="#000000",
            background=_bg,
            font="TkMenuFont",
            foreground="#000000",
            label="Print")
    root.sub_menu.add_command(
            activebackground="#ececec",
            activeforeground="#000000",
            background=_bg,
            font="TkMenuFont",
            foreground="#000000",
            label="Print Pdf", 
            command=exportCanvas)
    root.sub_menu.add_separator(
            background=_bg)
    root.sub_menu.add_command(
            activebackground="#ececec",
            activeforeground="#000000",
            background=_bg,
            font="TkMenuFont",
            foreground="#000000",
            label="Quit", 
            command=exitRoot)
    root.sub_menu1 = tk.Menu(root,tearoff=0)
    

    # edit menu #
    root.menubar.add_cascade(menu=root.sub_menu1,
            activebackground="#ececec",
            activeforeground="#000000",
            background=_bg,
            compound="left",
            font="TkMenuFont",
            foreground="#000000",
            label="Edit")
    root.sub_menu1.add_command(
            activebackground="#ececec",
            activeforeground="#000000",
            background=_bg,
            compound="left",
            font="TkMenuFont",
            foreground="#000000",
            label="Cut")
    root.sub_menu1.add_command(
            activebackground="#ececec",
            activeforeground="#000000",
            background=_bg,
            compound="left",
            font="TkMenuFont",
            foreground="#000000",
            label="Copy")
    root.sub_menu1.add_command(
            activebackground="#ececec",
            activeforeground="#000000",
            background=_bg,
            compound="left",
            font="TkMenuFont",
            foreground="#000000",
            label="Paste")

    # Help Menu #
    root.sub_menu123 = tk.Menu(root,tearoff=0)
    root.menubar.add_cascade(menu=root.sub_menu123,
            activebackground="#ececec",
            activeforeground="#000000",
            background=_bg,
            compound="left",
            font="TkMenuFont",
            foreground="#000000",
            label="Help")
    root.sub_menu123.add_command(
            activebackground="#ececec",
            activeforeground="#000000",
            background=_bg,
            compound="left",
            font="TkMenuFont",
            foreground="#000000",
            label="Tutorial", 
            command=tutorial)
    root.sub_menu123.add_separator(
            background=_bg)
    root.sub_menu123.add_command(
            activebackground="#ececec",
            activeforeground="#000000",
            background=_bg,
            compound="left",
            font="TkMenuFont",
            foreground="#000000",
            label="About")

####################################################
# Diagram Function
####################################################

# Diagram Layout Settings
fgaLineWidth = 2.4
cdLineWidth = 1
linesStartPoint = 20
linesEndPoint = 40
diagramColor = 'black'
diagramBackgroundColor = 'grey'
diagramborderColor = 'black'
diagramborderWidth = 0.5
diagramNoteWidth = 2
diagramStemWidth = 2

# Page Layout Settings
paperformat = [210, 297] # a4 210x297 | LxW in mm
paperorientation = 1 # 1 = portrait, 0 = landscape
leftmargin = 0
rightmargin = leftmargin
topmargin = 0
bottommargin = topmargin
titlemargin = 150 # space from topmargin to titlemargin

musicleftmargin = leftmargin
musicrightmargin = rightmargin
musictopmargin = topmargin + titlemargin
musicbottommargin = bottommargin


# Conversion table music-text to piano-key-numbers
musicConversionTable = {
    '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    '11': 11, '12': 12, '13': 13, '14': 14, '15': 15, '16': 16, '17': 17, '18': 18, '19': 19, '20': 20,
    '21': 21, '22': 22, '23': 23, '24': 24, '25': 25, '26': 26, '27': 27, '28': 28, '29': 29, '30': 30,
    '31': 31, '32': 32, '33': 33, '34': 34, '35': 35, '36': 36, '37': 37, '38': 38, '39': 39, '40': 40,
    '41': 41, '42': 42, '43': 43, '44': 44, '45': 45, '46': 46, '47': 47, '48': 48, '49': 49, '50': 50,
    '51': 51, '52': 52, '53': 53, '54': 54, '55': 55, '56': 56, '57': 57, '58': 58, '59': 59, '60': 60,
    '61': 61, '62': 62, '63': 63, '64': 64, '65': 65, '66': 66, '67': 67, '68': 68, '69': 69, '70': 70,
    '71': 71, '72': 72, '73': 73, '74': 74, '75': 75, '76': 76, '77': 77, '78': 78, '79': 79, '80': 80,
    '81': 81, '82': 82, '83': 83, '84': 84, '85': 85, '86': 86, '87': 87, '88': 88,

    'a0': 1,
    'a+0': 2, 'b-0': 2, 'A0': 2, 'z0': 2, 'as0': 2, 'bf0': 2,
    'b0': 3,

    'c1': 4,
    'c+1': 5, 'd-1': 5, 'C1': 5, 'cs1': 5, 'df1': 5, 'q1': 5, 'c#1': 5, 'db1': 5,
    'd1': 6,
    'd+1': 7, 'e-1': 7, 'D1': 7, 'ds1': 7, 'ef1': 7, 'w1': 7, 'd#1': 7, 'eb1': 7,
    'e1': 8,
    'f1': 9,
    'f+1': 10, 'g-1': 10, 'F1': 10, 'fs1': 10, 'gf1': 10, 'x1': 10, 'f#1': 10, 'gb1': 10,
    'g1': 11,
    'g+1': 12, 'a-1': 12, 'G1': 12, 'gs1': 12, 'af1': 14, 'y1': 12, 'g#1': 12, 'ab1': 12,
    'a1': 13,
    'a+1': 14, 'b-1': 14, 'A1': 14, 'as1': 14, 'bf1': 14, 'z1': 14, 'a#1': 14, 'bb1': 14,
    'b1': 15,

    'c2': 16,
    'c+2': 17, 'd-2': 17, 'C2': 17, 'cs2': 17, 'df2': 17, 'q2': 17, 'c#2': 17, 'db2': 17,
    'd2': 18,
    'd+2': 19, 'e-2': 19, 'D2': 19, 'ds2': 19, 'ef2': 19, 'w2': 19, 'd#2': 19, 'eb2': 19,
    'e2': 20,
    'f2': 21,
    'f+2': 22, 'g-2': 22, 'F2': 22, 'fs2': 22, 'gf2': 22, 'x2': 22, 'f#2': 22, 'gb2': 22,
    'g2': 23,
    'g+2': 24, 'a-2': 24, 'G2': 24, 'gs2': 24, 'af2': 24, 'y2': 24, 'g#2': 24, 'ab2': 24,
    'a2': 25,
    'a+2': 26, 'b-2': 26, 'A2': 26, 'as2': 26, 'bf2': 26, 'z2': 26, 'a#2': 26, 'bb2': 26,
    'b2': 27,

    'c3': 28,
    'c+3': 29, 'd-3': 29, 'C3': 29, 'cs3': 29, 'df3': 29, 'q3': 29, 'c#3': 29, 'db3': 29,
    'd3': 30,
    'd+3': 31, 'e-3': 31, 'D3': 31, 'ds3': 31, 'ef3': 31, 'w3': 31, 'd#3': 31, 'eb3': 31,
    'e3': 32,
    'f3': 33,
    'f+3': 34, 'g-3': 34, 'F3': 34, 'fs3': 34, 'gf3': 34, 'x3': 34, 'f#3': 34, 'gb3': 34,
    'g3': 35,
    'g+3': 36, 'a-3': 36, 'G3': 36, 'gs3': 36, 'af3': 36, 'y3': 36, 'g#3': 36, 'ab3': 36,
    'a3': 37,
    'a+3': 38, 'b-3': 38, 'A3': 38, 'as3': 38, 'bf3': 38, 'z3': 38, 'a#3': 38, 'bb3': 38,
    'b3': 39,

    'c4': 40, 'c': 40,
    'c+4': 41, 'd-4': 41, 'C4': 41, 'cs4': 41, 'df4': 41, 'q4': 41, 'c+': 41, 'd-': 41, 'C': 41, 'cs': 41,
    'df': 41, 'q': 41, 'c#': 41, 'db': 41, 'c#4': 41, 'db4': 41,
    'd4': 42, 'd': 42,
    'd+4': 43, 'e-4': 43, 'D4': 43, 'ds4': 43, 'ef4': 43, 'w4': 43, 'd+': 43, 'e-': 43, 'D': 43, 'ds': 43,
    'ef': 43, 'w': 43, 'd#': 43, 'eb': 43, 'd#4': 43, 'eb4': 43,
    'e4': 44, 'e': 44,
    'f4': 45, 'f': 45,
    'f+4': 46, 'g-4': 46, 'F4': 46, 'fs4': 46, 'gf4': 46, 'x4': 46, 'f+': 46, 'g-': 46, 'F': 46, 'fs': 46,
    'gf': 46, 'x': 46, 'f#': 46, 'gb': 46, 'f#4': 46, 'gb4': 46,
    'g4': 47, 'g': 47,
    'g+4': 48, 'a-4': 48, 'G4': 48, 'gs4': 48, 'af4': 48, 'y4': 48, 'g+': 48, 'a-': 48, 'G': 48, 'gs': 48,
    'af': 48, 'y': 48, 'g#': 48, 'ab': 48, 'g#4': 48, 'ab4': 48,
    'a4': 49, 'a': 49,
    'a+4': 50, 'b-4': 50, 'A4': 50, 'as4': 50, 'bf4': 50, 'z4': 50, 'a+': 50, 'b-': 50, 'A': 50, 'as': 50,
    'bf': 50, 'z': 50, 'a#': 50, 'bb': 50, 'a#4': 50, 'bb4': 50,
    'b4': 51, 'b': 51,

    'c5': 52,
    'c+5': 53, 'd-5': 53, 'C5': 53, 'cs5': 53, 'df5': 53, 'q5': 53, 'c#5': 53, 'db5': 53,
    'd5': 54,
    'd+5': 55, 'e-5': 55, 'D5': 55, 'ds5': 55, 'ef5': 55, 'w5': 55, 'd#5': 55, 'eb5': 55,
    'e5': 56,
    'f5': 57,
    'f+5': 58, 'g-5': 58, 'F5': 58, 'fs5': 58, 'gf5': 58, 'x5': 58, 'f#5': 58, 'gb5': 58,
    'g5': 59,
    'g+5': 60, 'a-5': 60, 'G5': 60, 'gs5': 60, 'af5': 60, 'y5': 60, 'g#5': 60, 'ab5': 60,
    'a5': 61,
    'a+5': 62, 'b-5': 62, 'A5': 62, 'as5': 62, 'bf5': 62, 'z5': 62, 'a#5': 62, 'bb5': 62,
    'b5': 63,

    'c6': 64,
    'c+6': 65, 'd-6': 65, 'C6': 65, 'cs6': 65, 'df6': 65, 'q6': 65, 'c#6': 65, 'db6': 65,
    'd6': 66,
    'd+6': 67, 'e-6': 67, 'D6': 67, 'ds6': 67, 'ef6': 67, 'w6': 67, 'd#6': 67, 'eb6': 67,
    'e6': 68,
    'f6': 69,
    'f+6': 70, 'g-6': 70, 'F6': 70, 'fs6': 70, 'gf6': 70, 'x6': 70, 'f#6': 70, 'gb6': 70,
    'g6': 71,
    'g+6': 72, 'a-6': 72, 'G6': 72, 'gs6': 72, 'af6': 72, 'y6': 72, 'g#6': 72, 'ab6': 72,
    'a6': 73,
    'a+6': 74, 'b-6': 74, 'A6': 74, 'as6': 74, 'bf6': 74, 'z6': 74, 'a#6': 74, 'bb6': 74,
    'b6': 75,

    'c7': 76,
    'c+7': 77, 'd-7': 77, 'C7': 77, 'cs7': 77, 'df7': 77, 'q7': 77, 'c#7': 77, 'db7': 77,
    'd7': 78,
    'd+7': 79, 'e-7': 79, 'D7': 79, 'ds7': 79, 'ef7': 79, 'w7': 79, 'd#7': 79, 'eb7': 79,
    'e7': 80,
    'f7': 81,
    'f+7': 82, 'g-7': 82, 'F7': 82, 'fs7': 82, 'gf7': 82, 'x7': 82, 'f#7': 82, 'gb7': 82,
    'g7': 83,
    'g+7': 84, 'a-7': 84, 'G7': 84, 'gs7': 84, 'af7': 84, 'y7': 84, 'g#7': 84, 'ab7': 84,
    'a7': 85,
    'a+7': 86, 'b-7': 86, 'A7': 86, 'as7': 86, 'bf7': 86, 'z7': 86, 'a#7': 86, 'bb7': 86,
    'b7': 87,
    'c8': 88, '':None, ' ':None
}

prevchordwidth = []
pageymemory = []
def drawD(leftright, s):
    # left entry #
    
    try: x = int(leftright[3]) + musicleftmargin
    except ValueError: x = 0
    left_hand_numbers = []  # numberInputLeft
    for leftPitch in leftright[0].split(' '):
        left_hand_numbers.append(musicConversionTable[leftPitch])
    # remove Nonetype from numberlist
    left_hand_numbers = [x for x in left_hand_numbers if x is not None]
    
    # right entry #
    
    # try: y = int(leftright[4]) * 5 + musictopmargin
    # except ValueError:
    #     y = 50 + idd * 40
    right_hand_numbers = []  # numberInputRight
    for rightPitch in leftright[1].split(' '):
        right_hand_numbers.append(musicConversionTable[rightPitch])
    # remove Nonetype from numberlist
    right_hand_numbers = [x for x in right_hand_numbers if x is not None]

    all_notes = left_hand_numbers + right_hand_numbers


    # system for automatic placement
    y = 175
    if not prevchordwidth:
        x = x - ((min(all_notes) * 5))+100

    else:
        if (paperformat[0]*root.winfo_fpixels('1m')-leftmargin-rightmargin) > sum(prevchordwidth)+s+75:# if current chord fits on paper
            if leftright[3] == '~' or leftright[3] == ' ~':# if offset == '~': place chord on next line in the document
                prevchordwidth.clear()
                x = x - ((min(all_notes) * 5)) + sum(prevchordwidth) + 100
                pageymemory.append(90)
                y = sum(pageymemory) + 25
            else:
                x = x - ((min(all_notes) * 5) - 100) + sum(prevchordwidth)
                y = sum(pageymemory) + 25
        else:# place chord on next line in the document
            prevchordwidth.clear()
            x = x - ((min(all_notes) * 5) - 100) + sum(prevchordwidth)
            pageymemory.append(90)
            y = sum(pageymemory) + 25

    if leftright[3] == '^' or leftright[3] == ' ^':# If you write '^' in the last entry the chord will be in one measure with the previous one.
        x = x -5




    def write_chord_name():
        root.CanvasPage.create_text(x+((min(left_hand_numbers) * 5)-25),y,fill="black",font=("Times", "15"),text=leftright[2], anchor=tk.W)


    # Drawing diagram lines
    def write_diagram_lines():
        if all_notes:
            if min(all_notes) <= 3:
                root.CanvasPage.create_line(20 + x, linesStartPoint + y, 20 + x, linesEndPoint + y, width=fgaLineWidth,
                                               fill=diagramColor)
            if min(all_notes) <= 8:
                root.CanvasPage.create_line(35 + x, linesStartPoint + y, 35 + x, linesEndPoint + y, width=cdLineWidth,
                                               fill=diagramColor)
                root.CanvasPage.create_line(45 + x, linesStartPoint + y, 45 + x, linesEndPoint + y, width=cdLineWidth,
                                               fill=diagramColor)
            if min(all_notes) <= 15:
                root.CanvasPage.create_line(60 + x, linesStartPoint + y, 60 + x, linesEndPoint + y, width=fgaLineWidth,
                                               fill=diagramColor)
                root.CanvasPage.create_line(70 + x, linesStartPoint + y, 70 + x, linesEndPoint + y, width=fgaLineWidth,
                                               fill=diagramColor)
                root.CanvasPage.create_line(80 + x, linesStartPoint + y, 80 + x, linesEndPoint + y, width=fgaLineWidth,
                                               fill=diagramColor)
            if min(all_notes) <= 20:
                root.CanvasPage.create_line(95 + x, linesStartPoint + y, 95 + x, linesEndPoint + y, width=cdLineWidth,
                                               fill=diagramColor)
                root.CanvasPage.create_line(105 + x, linesStartPoint + y, 105 + x, linesEndPoint + y, width=cdLineWidth,
                                               fill=diagramColor)
            if min(all_notes) <= 27:
                root.CanvasPage.create_line(120 + x, linesStartPoint + y, 120 + x, linesEndPoint + y, width=fgaLineWidth,
                                               fill=diagramColor)
                root.CanvasPage.create_line(130 + x, linesStartPoint + y, 130 + x, linesEndPoint + y, width=fgaLineWidth,
                                               fill=diagramColor)
                root.CanvasPage.create_line(140 + x, linesStartPoint + y, 140 + x, linesEndPoint + y, width=fgaLineWidth,
                                               fill=diagramColor)
            if min(all_notes) <= 32:
                root.CanvasPage.create_line(155 + x, linesStartPoint + y, 155 + x, linesEndPoint + y, width=cdLineWidth,
                                               fill=diagramColor)
                root.CanvasPage.create_line(165 + x, linesStartPoint + y, 165 + x, linesEndPoint + y, width=cdLineWidth,
                                               fill=diagramColor)
            if min(all_notes) <= 39:
                root.CanvasPage.create_line(180 + x, linesStartPoint + y, 180 + x, linesEndPoint + y, width=fgaLineWidth,
                                               fill=diagramColor)
                root.CanvasPage.create_line(190 + x, linesStartPoint + y, 190 + x, linesEndPoint + y, width=fgaLineWidth,
                                               fill=diagramColor)
                root.CanvasPage.create_line(200 + x, linesStartPoint + y, 200 + x, linesEndPoint + y, width=fgaLineWidth,
                                               fill=diagramColor)
            root.CanvasPage.create_line(215 + x, linesStartPoint + y, 215 + x, linesEndPoint + y, width=cdLineWidth, dash=(4, 3),
                                           fill=diagramColor)
            root.CanvasPage.create_line(225 + x, linesStartPoint + y, 225 + x, linesEndPoint + y, width=cdLineWidth, dash=(4, 3),
                                           fill=diagramColor)
            if max(all_notes) >= 45:
                root.CanvasPage.create_line(240 + x, linesStartPoint + y, 240 + x, linesEndPoint + y, width=fgaLineWidth,
                                               fill=diagramColor)
                root.CanvasPage.create_line(250 + x, linesStartPoint + y, 250 + x, linesEndPoint + y, width=fgaLineWidth,
                                               fill=diagramColor)
                root.CanvasPage.create_line(260 + x, linesStartPoint + y, 260 + x, linesEndPoint + y, width=fgaLineWidth,
                                               fill=diagramColor)
            if max(all_notes) >= 52:
                root.CanvasPage.create_line(275 + x, linesStartPoint + y, 275 + x, linesEndPoint + y, width=cdLineWidth,
                                               fill=diagramColor)
                root.CanvasPage.create_line(285 + x, linesStartPoint + y, 285 + x, linesEndPoint + y, width=cdLineWidth,
                                               fill=diagramColor)
            if max(all_notes) >= 57:
                root.CanvasPage.create_line(300 + x, linesStartPoint + y, 300 + x, linesEndPoint + y, width=fgaLineWidth,
                                               fill=diagramColor)
                root.CanvasPage.create_line(310 + x, linesStartPoint + y, 310 + x, linesEndPoint + y, width=fgaLineWidth,
                                               fill=diagramColor)
                root.CanvasPage.create_line(320 + x, linesStartPoint + y, 320 + x, linesEndPoint + y, width=fgaLineWidth,
                                               fill=diagramColor)
            if max(all_notes) >= 64:
                root.CanvasPage.create_line(335 + x, linesStartPoint + y, 335 + x, linesEndPoint + y, width=cdLineWidth,
                                               fill=diagramColor)
                root.CanvasPage.create_line(345 + x, linesStartPoint + y, 345 + x, linesEndPoint + y, width=cdLineWidth,
                                               fill=diagramColor)
            if max(all_notes) >= 69:
                root.CanvasPage.create_line(360 + x, linesStartPoint + y, 360 + x, linesEndPoint + y, width=fgaLineWidth,
                                               fill=diagramColor)
                root.CanvasPage.create_line(370 + x, linesStartPoint + y, 370 + x, linesEndPoint + y, width=fgaLineWidth,
                                               fill=diagramColor)
                root.CanvasPage.create_line(380 + x, linesStartPoint + y, 380 + x, linesEndPoint + y, width=fgaLineWidth,
                                               fill=diagramColor)
            if max(all_notes) >= 76:
                root.CanvasPage.create_line(395 + x, linesStartPoint + y, 395 + x, linesEndPoint + y, width=cdLineWidth,
                                               fill=diagramColor)
                root.CanvasPage.create_line(405 + x, linesStartPoint + y, 405 + x, linesEndPoint + y, width=cdLineWidth,
                                               fill=diagramColor)
            if max(all_notes) >= 81:
                root.CanvasPage.create_line(420 + x, linesStartPoint + y, 420 + x, linesEndPoint + y, width=fgaLineWidth,
                                               fill=diagramColor)
                root.CanvasPage.create_line(430 + x, linesStartPoint + y, 430 + x, linesEndPoint + y, width=fgaLineWidth,
                                               fill=diagramColor)
                root.CanvasPage.create_line(440 + x, linesStartPoint + y, 440 + x, linesEndPoint + y, width=fgaLineWidth,
                                               fill=diagramColor)

    # Drawing the notes on the diagram
    def write_all_notes():  # this function writes all notes from rightNotes and leftNotes on the diagram.
        def black_key(x, y, r, canvasName):  # center coordinates, radius
            x0 = x - r
            y0 = y - r
            x1 = x + r
            y1 = y + r
            return canvasName.create_oval(x0, y0, x1, y1, outline=diagramColor, fill=diagramColor,
                                          width=(diagramNoteWidth - 1.5))

        def white_key(x, y, r, canvasName):  # center coordinates, radius
            x0 = x - r
            y0 = y - r
            x1 = x + r
            y1 = y + r
            return canvasName.create_oval(x0, y0, x1, y1, outline=diagramColor, width=diagramNoteWidth)

        def small_white_key(x, y):
            x0 = x
            y0 = y
            return root.CanvasPage.create_oval(x0, y0, (x0 + 8), (y0 + 10), outline=diagramColor, width=diagramNoteWidth)

        ######################################### Octave 0
        # A0
        if 1 in all_notes:
            white_key(15+x, 25+y, 5, root.CanvasPage)
        # a0
        if 2 in all_notes:
            black_key(20+x, 15+y, 5, root.CanvasPage)
        # B0
        if 3 in all_notes and 4 in all_notes:
            small_white_key(20+x, 20+y)
        if 3 in all_notes and 4 not in all_notes:
            white_key(25+x, 25+y, 5, root.CanvasPage)
        ######################################### Octave 1
        # C1
        if 4 in all_notes and 3 in all_notes:
            small_white_key(27.5+x, 20+y)
        if 4 in all_notes and 3 not in all_notes:
            white_key(30+x, 25+y, 5, root.CanvasPage)
        # c1
        if 5 in all_notes:
            black_key(35+x, 15+y, 5, root.CanvasPage)
        # D1
        if 6 in all_notes:
            white_key(40+x, 25+y, 5, root.CanvasPage)
        # d1
        if 7 in all_notes:
            black_key(45+x, 15+y, 5, root.CanvasPage)
        # E1
        if 8 in all_notes and 9 in all_notes:
            small_white_key(45+x, 20+y)
        if 8 in all_notes and 9 not in all_notes:
            white_key(50+x, 25+y, 5, root.CanvasPage)
        # F1
        if 9 in all_notes and 8 in all_notes:
            small_white_key(52.5+x, 20+y)
        if 9 in all_notes and 8 not in all_notes:
            white_key(55+x, 25+y, 5, root.CanvasPage)
        # f1
        if 10 in all_notes:
            black_key(60+x, 15+y, 5, root.CanvasPage)
        # G1
        if 11 in all_notes:
            white_key(65+x, 25+y, 5, root.CanvasPage)
        # g1
        if 12 in all_notes:
            black_key(70+x, 15+y, 5, root.CanvasPage)
        # A1
        if 13 in all_notes:
            white_key(75+x, 25+y, 5, root.CanvasPage)
        # a1
        if 14 in all_notes:
            black_key(80+x, 15+y, 5, root.CanvasPage)
        # B1
        if 15 in all_notes and 16 in all_notes:
            small_white_key(80+x, 20+y)
        if 15 in all_notes and 16 not in all_notes:
            white_key(85+x, 25+y, 5, root.CanvasPage)
        ######################################### Octave 2
        # C2
        if 16 in all_notes and 15 in all_notes:
            small_white_key(87.5+x, 20+y)
        if 16 in all_notes and 15 not in all_notes:
            white_key(90+x, 25+y, 5, root.CanvasPage)
        # c2
        if 17 in all_notes:
            black_key(95+x, 15+y, 5, root.CanvasPage)
        # D2
        if 18 in all_notes:
            white_key(100+x, 25+y, 5, root.CanvasPage)
        # d2
        if 19 in all_notes:
            black_key(105+x, 15+y, 5, root.CanvasPage)
        # E2
        if 20 in all_notes and 21 in all_notes:
            small_white_key(105+x, 20+y)
        if 20 in all_notes and 21 not in all_notes:
            white_key(110+x, 25+y, 5, root.CanvasPage)
        # F2
        if 21 in all_notes and 20 in all_notes:
            small_white_key(112.5+x, 20+y)
        if 21 in all_notes and 20 not in all_notes:
            white_key(115+x, 25+y, 5, root.CanvasPage)
        # f2
        if 22 in all_notes:
            black_key(120+x, 15+y, 5, root.CanvasPage)
        # G2
        if 23 in all_notes:
            white_key(125+x, 25+y, 5, root.CanvasPage)
        # g2
        if 24 in all_notes:
            black_key(130+x, 15+y, 5, root.CanvasPage)
        # A2
        if 25 in all_notes:
            white_key(135+x, 25+y, 5, root.CanvasPage)
        # a2
        if 26 in all_notes:
            black_key(140+x, 15+y, 5, root.CanvasPage)
        # B2
        if 27 in all_notes and 28 in all_notes:
            small_white_key(140+x, 20+y)
        if 27 in all_notes and 28 not in all_notes:
            white_key(145+x, 25+y, 5, root.CanvasPage)
        ##################################### Octave 3
        # C3
        if 28 in all_notes and 27 in all_notes:
            small_white_key(147.5+x, 20+y)
        if 28 in all_notes and 27 not in all_notes:
            white_key(150+x, 25+y, 5, root.CanvasPage)
        # c3
        if 29 in all_notes:
            black_key(155+x, 15+y, 5, root.CanvasPage)
        # D3
        if 30 in all_notes:
            white_key(160+x, 25+y, 5, root.CanvasPage)
        # d3
        if 31 in all_notes:
            black_key(165+x, 15+y, 5, root.CanvasPage)
        # E3
        if 32 in all_notes and 33 in all_notes:
            small_white_key(165+x, 20+y)
        if 32 in all_notes and 33 not in all_notes:
            white_key(170+x, 25+y, 5, root.CanvasPage)
        # F3
        if 33 in all_notes and 32 in all_notes:
            small_white_key(172.5+x, 20+y)
        if 33 in all_notes and 32 not in all_notes:
            white_key(175+x, 25+y, 5, root.CanvasPage)
        # f3
        if 34 in all_notes:
            black_key(180+x, 15+y, 5, root.CanvasPage)
        # G3
        if 35 in all_notes:
            white_key(185+x, 25+y, 5, root.CanvasPage)
        # g3
        if 36 in all_notes:
            black_key(190+x, 15+y, 5, root.CanvasPage)
        # A3
        if 37 in all_notes:
            white_key(195+x, 25+y, 5, root.CanvasPage)
        # a3
        if 38 in all_notes:
            black_key(200+x, 15+y, 5, root.CanvasPage)
        # B3
        if 39 in all_notes and 40 in all_notes:
            small_white_key(200+x, 20+y)
        if 39 in all_notes and 40 not in all_notes:
            white_key(205+x, 25+y, 5, root.CanvasPage)

        ##################################### Octave 4
        # C4
        if 40 in all_notes and 39 in all_notes:
            small_white_key(207.5+x, 20+y)
        if 40 in all_notes and 39 not in all_notes:
            white_key(210+x, 25+y, 5, root.CanvasPage)
        # c4
        if 41 in all_notes:
            black_key(215+x, 15+y, 5, root.CanvasPage)
        # D4
        if 42 in all_notes:
            white_key(220+x, 25+y, 5, root.CanvasPage)
        # d4
        if 43 in all_notes:
            black_key(225+x, 15+y, 5, root.CanvasPage)
        # E4
        if 44 in all_notes and 45 in all_notes:
            small_white_key(225+x, 20+y)
        if 44 in all_notes and 45 not in all_notes:
            white_key(230+x, 25+y, 5, root.CanvasPage)
        # F4
        if 45 in all_notes and 44 in all_notes:
            small_white_key(232.5+x, 20+y)
        if 45 in all_notes and 44 not in all_notes:
            white_key(235+x, 25+y, 5, root.CanvasPage)
        # f4
        if 46 in all_notes:
            black_key(240+x, 15+y, 5, root.CanvasPage)
        # G4
        if 47 in all_notes:
            white_key(245+x, 25+y, 5, root.CanvasPage)
        # g4
        if 48 in all_notes:
            black_key(250+x, 15+y, 5, root.CanvasPage)
        # A4
        if 49 in all_notes:
            white_key(255+x, 25+y, 5, root.CanvasPage)
        # a4
        if 50 in all_notes:
            black_key(260+x, 15+y, 5, root.CanvasPage)
        # B4
        if 51 in all_notes and 52 in all_notes:
            small_white_key(260+x, 20+y)
        if 51 in all_notes and 52 not in all_notes:
            white_key(265+x, 25+y, 5, root.CanvasPage)

        ##################################### Octave 5
        # C5
        if 52 in all_notes and 51 in all_notes:
            small_white_key(267.5+x, 20+y)
        if 52 in all_notes and 51 not in all_notes:
            white_key(270+x, 25+y, 5, root.CanvasPage)
        # c5
        if 53 in all_notes:
            black_key(275+x, 15+y, 5, root.CanvasPage)
        # D5
        if 54 in all_notes:
            white_key(280+x, 25+y, 5, root.CanvasPage)
        # d5
        if 55 in all_notes:
            black_key(285+x, 15+y, 5, root.CanvasPage)
        # E5
        if 56 in all_notes and 57 in all_notes:
            small_white_key(285+x, 20+y)
        if 56 in all_notes and 57 not in all_notes:
            white_key(290+x, 25+y, 5, root.CanvasPage)
        # F5
        if 57 in all_notes and 56 in all_notes:
            small_white_key(292.5+x, 20+y)
        if 57 in all_notes and 56 not in all_notes:
            white_key(295+x, 25+y, 5, root.CanvasPage)
        # f5
        if 58 in all_notes:
            black_key(300+x, 15+y, 5, root.CanvasPage)
        # G5
        if 59 in all_notes:
            white_key(305+x, 25+y, 5, root.CanvasPage)
        # g5
        if 60 in all_notes:
            black_key(310+x, 15+y, 5, root.CanvasPage)
        # A5
        if 61 in all_notes:
            white_key(315+x, 25+y, 5, root.CanvasPage)
        # a5
        if 62 in all_notes:
            black_key(320+x, 15+y, 5, root.CanvasPage)
        # B5
        if 63 in all_notes and 64 in all_notes:
            small_white_key(320+x, 20+y)
        if 63 in all_notes and 64 not in all_notes:
            white_key(325+x, 25+y, 5, root.CanvasPage)

        ##################################### Octave 6
        # C6
        if 64 in all_notes and 63 in all_notes:
            small_white_key(327.5+x, 20+y)
        if 64 in all_notes and 63 not in all_notes:
            white_key(330+x, 25+y, 5, root.CanvasPage)
        # c6
        if 65 in all_notes:
            black_key(335+x, 15+y, 5, root.CanvasPage)
        # D6
        if 66 in all_notes:
            white_key(340+x, 25+y, 5, root.CanvasPage)
        # d6
        if 67 in all_notes:
            black_key(345+x, 15+y, 5, root.CanvasPage)
        # E6
        if 68 in all_notes and 69 in all_notes:
            small_white_key(345+x, 20+y)
        if 68 in all_notes and 69 not in all_notes:
            white_key(350+x, 25+y, 5, root.CanvasPage)
        # F6
        if 69 in all_notes and 68 in all_notes:
            small_white_key(352.5+x, 20+y)
        if 69 in all_notes and 68 not in all_notes:
            white_key(355+x, 25+y, 5, root.CanvasPage)
        # f6
        if 70 in all_notes:
            black_key(360+x, 15+y, 5, root.CanvasPage)
        # G6
        if 71 in all_notes:
            white_key(365+x, 25+y, 5, root.CanvasPage)
        # g6
        if 72 in all_notes:
            black_key(370+x, 15+y, 5, root.CanvasPage)
        # A6
        if 73 in all_notes:
            white_key(375+x, 25+y, 5, root.CanvasPage)
        # a6
        if 74 in all_notes:
            black_key(380+x, 15+y, 5, root.CanvasPage)
        # B6
        if 75 in all_notes and 76 in all_notes:
            small_white_key(380+x, 20+y)
        if 75 in all_notes and 76 not in all_notes:
            white_key(385+x, 25+y, 5, root.CanvasPage)

        ##################################### Octave 7
        # C7
        if 76 in all_notes and 75 in all_notes:
            small_white_key(387.5+x, 20+y)
        if 76 in all_notes and 75 not in all_notes:
            white_key(390+x, 25+y, 5, root.CanvasPage)
        # c7
        if 77 in all_notes:
            black_key(395+x, 15+y, 5, root.CanvasPage)
        # D7
        if 78 in all_notes:
            white_key(400+x, 25+y, 5, root.CanvasPage)
        # d7
        if 79 in all_notes:
            black_key(405+x, 15+y, 5, root.CanvasPage)
        # E7
        if 80 in all_notes and 81 in all_notes:
            small_white_key(405+x, 20+y)
        if 80 in all_notes and 81 not in all_notes:
            white_key(410+x, 25+y, 5, root.CanvasPage)
        # F7
        if 81 in all_notes and 80 in all_notes:
            small_white_key(412.5+x, 20+y)
        if 81 in all_notes and 80 not in all_notes:
            white_key(415+x, 25+y, 5, root.CanvasPage)
        # f7
        if 82 in all_notes:
            black_key(420+x, 15+y, 5, root.CanvasPage)
        # G7
        if 83 in all_notes:
            white_key(425+x, 25+y, 5, root.CanvasPage)
        # g7
        if 84 in all_notes:
            black_key(430+x, 15+y, 5, root.CanvasPage)
        # A7
        if 85 in all_notes:
            white_key(435+x, 25+y, 5, root.CanvasPage)
        # a7
        if 86 in all_notes:
            black_key(440+x, 15+y, 5, root.CanvasPage)
        # B7
        if 87 in all_notes and 88 in all_notes:
            small_white_key(440+x, 20+y)
        if 87 in all_notes and 88 not in all_notes:
            white_key(445+x, 25+y, 5, root.CanvasPage)
        # C8
        if 88 in all_notes and 87 in all_notes:
            small_white_key(447.5+x, 20+y)
        if 88 in all_notes and 87 not in all_notes:
            white_key(450+x, 25+y, 5, root.CanvasPage)

    # Drawing diagram right and left hand lines
    def write_stems():
        if right_hand_numbers:
            right_stem_start = (40 + max(right_hand_numbers) * 5)
            right_stem_end = (10 + min(right_hand_numbers) * 5)
            root.CanvasPage.create_line(right_stem_start+x, 20+y, right_stem_end+x, 20+y, width=diagramStemWidth,
                                           fill=diagramColor)  # right stem
        if left_hand_numbers:
            left_stem_start = (-20 + min(left_hand_numbers) * 5)
            left_stem_end = (10 + max(left_hand_numbers) * 5)
            root.CanvasPage.create_line(left_stem_start+x, 20+y, left_stem_end+x, 20+y, width=diagramStemWidth,
                                           fill=diagramColor)  # left stem
        # return left_stem_start+x, right_stem_end+x

    # If crosshands write dot inside right hand
    def write_cross_hands():
        def right_hand_point_white(x, y, r, canvasName):  # center coordinates, radius
            x0 = x - r
            y0 = y - r
            x1 = x + r
            y1 = y + r
            return canvasName.create_oval(x0, y0, x1, y1, outline=diagramColor, fill=diagramColor,
                                          width=(diagramNoteWidth - 1.5))

        def right_hand_point(x, y, r, canvasName):  # center coordinates, radius
            x0 = x - r
            y0 = y - r
            x1 = x + r
            y1 = y + r
            return canvasName.create_oval(x0, y0, x1, y1, outline='white', fill='white',
                                          width=(diagramNoteWidth - 1.5))

        dotYposition = {'1': 20, '2': 10, '3': 20, '4': 20, '5': 10, '6': 20, '7': 10, '8': 20, '9': 20, '10': 10,
                        '11': 20, '12': 10, '13': 20, '14': 10, '15': 20, '16': 20, '17': 10, '18': 20, '19': 10,
                        '20': 20,
                        '21': 20, '22': 10, '23': 20, '24': 10, '25': 20, '26': 10, '27': 20, '28': 20, '29': 10,
                        '30': 20,
                        '31': 10, '32': 20, '33': 20, '34': 10, '35': 20, '36': 10, '37': 20, '38': 10, '39': 20,
                        '40': 20,
                        '41': 10, '42': 20, '43': 10, '44': 20, '45': 20, '46': 10, '47': 20, '48': 10, '49': 20,
                        '50': 10,
                        '51': 20, '52': 20, '53': 10, '54': 20, '55': 10, '56': 20, '57': 20, '58': 10, '59': 20,
                        '60': 10,
                        '61': 20, '62': 10, '63': 20, '64': 20, '65': 10, '66': 20, '67': 10, '68': 20, '69': 20,
                        '70': 10,
                        '71': 20, '72': 10, '73': 20, '74': 10, '75': 20, '76': 20, '77': 10, '78': 20, '79': 10,
                        '80': 20,
                        '81': 20, '82': 10, '83': 20, '84': 10, '85': 20, '86': 10, '87': 20, '88': 20}
        if right_hand_numbers and left_hand_numbers:
            if max(left_hand_numbers) >= min(right_hand_numbers) - 1:
                for rightdotposition in right_hand_numbers:
                    right_hand_point_white(10 + rightdotposition * 5 +x, dotYposition[str(rightdotposition)] + 5 + y, 2,
                                           root.CanvasPage)
                    right_hand_point(10 + rightdotposition * 5 + x, dotYposition[str(rightdotposition)] + 5 + y, 1,
                                     root.CanvasPage)

    # A border around the diagram so it looks more like a pianokeyboard
    def write_keyboard_border():
        # right fix
        r = []
        if not right_hand_numbers:
            r.append(44)
        else:
            r = right_hand_numbers
        
        # left fix
        l = []
        if not left_hand_numbers:
            l.append(40)
        else:
            l = left_hand_numbers

        # main function
        leftborderx = (-30 + min(l) * 5)
        rightborderx = (50 + max(r) * 5)
        if left_hand_numbers or right_hand_numbers:
            if leftright[3] == '^' or leftright[3] == ' ^':# If you write '^' in the last entry the chord will be in one measure with the previous one.
                root.CanvasPage.create_line(leftborderx+x, 20+y, leftborderx+x, 50+y, width=diagramborderWidth, fill=diagramborderColor)
                root.CanvasPage.create_line(rightborderx+x, 20+y, rightborderx+x, 50+y, width=diagramborderWidth, fill=diagramborderColor)
                root.CanvasPage.create_line(leftborderx+x, 50+y, rightborderx+x, 50+y, width=diagramborderWidth, fill=diagramborderColor)
            else:
                root.CanvasPage.create_line(leftborderx+x, 20+y, leftborderx+x, 50+y, width=diagramborderWidth, fill=diagramborderColor)
                root.CanvasPage.create_line(rightborderx+x, 20+y, rightborderx+x, 50+y, width=diagramborderWidth, fill=diagramborderColor)
                root.CanvasPage.create_line(leftborderx+x, 50+y, rightborderx+x, 50+y, width=diagramborderWidth, fill=diagramborderColor)
        else:
            print('')

    # Run functions
    write_diagram_lines()
    write_all_notes()
    write_stems()
    write_cross_hands()
    write_keyboard_border()
    write_chord_name()
    return prevchordwidth.insert(0, s)

#########################################################
# sourceFile functions (openFile, saveFile, saveFileAs) #
#########################################################

filepath = []

def readFile():# Working
    return root.Texteditor.get('1.0', END + '-1c')


def newFile():# Working
    # Check if current file is empty, empty means nothing to save
    if readFile() > "":
        saveffileQ = messagebox.askyesno("Save current file?", "Do you wish to save the current project?")
        if saveffileQ:
            saveFile()
    filepath.clear()
    filepath.insert(1, 'New Project')
    root.title("PianoScript® Leadsheets - " + str(filepath[0]))
    root.Texteditor.delete("1.0", END)
    root.Texteditor.insert("1.0", '''\\New leadsheet
\\composer
\\copyright notice

\\music:
;;;

_________________________________________
notes''')
    tryEngrave('.')

    
def openFile():# Working
    # Check if current file is changed
    if readFile() > "":
        saveffileQ = messagebox.askyesno("Save current file?", "Do you wish to save the current project?")
        if saveffileQ:
            saveFile()

    # run basic functionality
    file = filedialog.askopenfile(parent=root, 
                                  mode='rb', 
                                  title='Open a PianoScript® Leadsheet project', 
                                  filetypes=[("Piano-Script-Leadsheet","*.psl"), ("Text Files", "*.txt")])
    if file is not None:
        root.Texteditor.delete("1.0", END)
        root.Texteditor.insert('1.0', file.read())
        file.close()
        return filepath.clear(), filepath.insert(1, file.name), root.title("PianoScript® Leadsheets - " + str(filepath[0])), tryEngrave('.')


def saveFile():# Working
    if filepath[0] == 'New Project': # is it a new file or a opened file?
        saveFileAs()
        print('saveFileAs')
    else:
        #this saves the already opened file
        open(filepath[0], 'w').write(readFile())
        print('saveFile', filepath[0])
        


def saveFileAs():# Working
    file = filedialog.asksaveasfile(mode='w', parent=root, 
        filetypes=[("Piano-Script-Leadsheet","*.psl")])

    if file is not None:
        data = root.Texteditor.get('1.0', END + '-1c')
        file.write(data)
        file.close()
        filepath.clear()
        filepath.insert(1, file.name)
        root.title("PianoScript® Leadsheets - " + str(filepath[0]))


def exitRoot():# Working
    if readFile() > "":
        if messagebox.askyesno("Save current file?", "Do you wish to save the current project?"):
            saveFile()
    root.destroy()


def tutorial():# Working
    # This Function opens the Tutorial.
    if readFile() > "":
        saveffileQ = messagebox.askyesno("Save current file?", "Do you wish to save the current project?")
        if saveffileQ:
            saveFile()
    filepath.clear()
    filepath.insert(1, 'New Project')
    root.title("PianoScript® Leadsheets - " + str(filepath[0]))
    root.Texteditor.delete("1.0", END)
    root.Texteditor.insert("1.0", '''\\Tutorial
\\PianoScript
\\copyright PianoScript 2020

\\music:
1;88;Full sized keyboard (You can use piano-key-numbers 1-88);

c e;g c5;C (writing '~' behind the chord will move it to the next line);~

f3 e-;a- c5;Fm7 (x offset 350p);350

28 35 42;38 43 47;Cm9 (crosshand: the dotted notes are for the right hand);~

q3 b3;q f y;Q7 (qw xyz notation: use these names because every key should have their own name);~

c3 g3;b3 e g;Cmaj7 (Final chord);~

c e;g c5;The tutorial sequense: [4/4];~
f3 e-;a- c5;;-5
28 35 42;38 43 47;...measure 2;
q3 b3;q f y;[2/4];
c3 g3;b3 e g;[4/4];



_________________________________________
notes

Things we hoped you to learn:
* Every chord must be written on a new line. 
* The chord format is: (newline)
lefthand;righthand;chordname;offsetx or ~(write on new line)
* There are several ways of writing down the pitch. look in the Tutorial for more info.
* In the last entry you can offset the x position or you can print it to the next line.
* When two chords are written against each other they are in the same measure.
* The title, composer and copyright headers are on top of the file, seperated by backslashes.'''
)
    tryEngrave('.')
    


#########################################################
# Engraver                                              #
#########################################################
def engrave():
    root.CanvasPage.delete("all")
    file = root.Texteditor.get('1.0', END)

    # Print Paper
    o = paperorientation
    if o == True:
        h = paperformat[1] * (root.winfo_fpixels('1m'))
        w = paperformat[0] * (root.winfo_fpixels('1m'))
    else:
        h = paperformat[0] * (root.winfo_fpixels('1m'))
        w = paperformat[1] * (root.winfo_fpixels('1m'))
    root.CanvasPage.create_rectangle(55, 55, w + 5, h + 5, fill='black'), root.CanvasPage.create_rectangle(50, 50, w, h, fill='white', outline='white')


    # Clear lists for every new render.
    prevchordwidth.clear()
    pageymemory.clear()
    pageymemory.append(150)

    def chordSize(leftright):# gives the size of the chord as return.
        left_hand_numbers = []
        for leftPitch in leftright[0].split(' '):
            left_hand_numbers.append(musicConversionTable[leftPitch])
        left_hand_numbers = [x for x in left_hand_numbers if x is not None]

        right_hand_numbers = []
        for rightPitch in leftright[1].split(' '):
            right_hand_numbers.append(musicConversionTable[rightPitch])
        right_hand_numbers = [x for x in right_hand_numbers if x is not None]
        all_notes = right_hand_numbers + left_hand_numbers

        size = (max(all_notes) - min(all_notes)) * 5 + 85
        return size

    # File read system stufff...
    file = readFile()
    file = file.split('\\')
    try: music = file[4].split('\n')
    except: return
    del music[0]

    # Printing Titles... #

    # Title
    root.CanvasPage.create_text(70,125,fill="black",font=("Times", "28"),text=file[1], anchor=tk.W)
    # Composer
    root.CanvasPage.create_text(750,125,fill="black",font=("Times", "16"),text=file[2], anchor=tk.E)
    # Line
    root.CanvasPage.create_line(50,140,w,140,width=2)
    # Copyright
    print(file[3])
    root.CanvasPage.create_text(750,1100,fill="black",font=("Times", "12", "italic"),text=file[3], anchor=tk.E)
    
    print('music:', music)
    music = [s.split(';') for s in music]
    music = [x for x in music if x != ['']]
    if len(music) > 0:
        for i in range(len(music)):
            try: drawD(music[i], chordSize(music[i]))
            except IndexError:
                return print("IndexError")

def tryEngrave(self):
    try: engrave()
    except: return

#########################################################
# Print and export as pdf functions                     #
#########################################################

def exportCanvas():
    print('exportCanvas')
    xi = 0
    o = paperorientation
    if o == True:
        h = paperformat[1] * (root.winfo_fpixels('1m')+xi)
        w = paperformat[0] * (root.winfo_fpixels('1m')+xi)
    else:
        h = paperformat[0] * (root.winfo_fpixels('1m')+xi)
        w = paperformat[1] * (root.winfo_fpixels('1m')+xi)
    root.CanvasPage.postscript(file="~/Desktop/test.eps", width=w, height=h, x=50, y=50)
    



# helpfunction; remove when publishing.
def autoOpen():
    root.Texteditor.delete('1.0', END)
    file = open("/mnt/dataDrive/MEGA/Program/PianoDiagramLeadsheets/For the starting pianist.psl", "r")
    root.Texteditor.insert('1.0', file.read())

#########################################################
# Program running order                                 #
#########################################################
buildGUI()# builds the graphical user interface
newFile()# creates a new file (inside the textwidget)
# autoOpen()
tryEngrave('.')

# Update the canvas(run 'run_pianoscript_diagram()') on every keypress
root.bind('<Key>', tryEngrave)
root.mainloop()
