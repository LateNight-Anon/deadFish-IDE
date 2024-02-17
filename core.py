#A visual IDE for deadFish and similare

from tkinter import Tk, Text, Label, Button
from threading import Thread
from time import sleep

app = Tk()
app.resizable(width=False, height=False)
app.geometry("1000x900")
app.title("deadFish IDE")
Label(text="deadFish IDE",font=("Arial",35)).place(x=400,y=20)
programEntry = Text(width=43,height=16,font=("Arial",30),borderwidth=4,relief="solid")
programEntry.place(x=25,y=90)
syntaxErrorLabel = Label(text="program is empty", fg="orange",font=("Arial",25))
syntaxErrorLabel.place(x=20,y=840)

def createErrorMessage() -> None:
    errorLabel.configure(font=("Arial",25))
    sleep(2)
    errorLabel.configure(font=("Arial",0))

def errorChecking() -> None:
    global program
    while True:
        program = programEntry.get('1.0','end-1c')
        if len(programEntry.get('1.0','end-1c')):
            try:
                for i, char in enumerate(program):
                    if not char in ('i','d','s','o'):
                        raise Exception(i + 1)
                syntaxErrorLabel.configure(text="all clear", fg="green")
            except Exception as charIndex:
                syntaxErrorLabel.configure(text="error detected at char " + str(charIndex), fg="red")
        else:
            syntaxErrorLabel.configure(text="program is empty", fg="orange")

def interpret() -> None:
    global accumulator
    outputWindow = Tk()
    outputWindow.title("deadFish interpreter")
    outputWindow.configure(bg="white")
    outputWindow.geometry("100x100")
    outputStr: str = ""
    outputLabel = Label(outputWindow,text="",font=("Arial",60),bg="white")
    outputLabel.place(x=0,y=0)
    for i, char in enumerate(program):
        if char == 'i': accumulator += 1
        elif char == 'd': accumulator -= 1
        elif char == 's': accumulator **= 2
        elif char == 'o':
            if i + 1 != len(program): outputStr += str(accumulator) + ","
            else: outputStr += str(accumulator)
            outputLabel.configure(text=outputStr)
            outputLabel.geometry(str(100 * len(outputStr)) + "x100")
        else:
            print("error in char",i)
            return
        #accumulator overload checks
        if accumulator > 255: accumulator = 0
        elif accumulator < 0: accumulator = 255

def openCode() -> None:
    def createErrorMessage() -> None:
        errorLabel.configure(font=("Arial",25))
        sleep(2)
        errorLabel.configure(font=("Arial",0))
        
    def submit() -> None:
        global program
        try:
            with open(directory, 'r') as file:
                program = file.readline()
        except Exception:
            Thread(target=createErrorMessage).start()
                
    directory: str = None
    selectionWindow = Tk()
    selectionWindow.resizable(width=False,height=False)
    selectionWindow.title("read from file")
    selectionWindow.geometry("500x500")
    Label(text="select file to read",font=("Arial",15)).place(x=180,y=30)

def writeCodeToFile() -> None:
    def submit() -> None:
        try:
            with open(directory,'w') as file:
                file.write(program)
        except Exception:
            Thread(target=createErrorMessage).start()

    directory: str = None
    selectionWindow = Tk()
    selectionWindow.resizable(width=False,height=False)
    selectionWindow.title("write to file")
    selectionWindow.geometry("500x500")
    Label(text="select file to read",font=("Arial",15)).place(x=180,y=30)
    errorLabel = Label(text="invalid file",font=("Arial",0),fg="red")
    errorLabel.place(x=30,y=400)

Button(text="open file",command=openCode,font=("Arial",15),borderwidth=4,relief="solid").place(x=630,y=842)
Button(text="save file",command=writeCodeToFile,font=("Arial",15),borderwidth=4,relief="solid").place(x=750,y=842)
Button(text="execute",command=interpret,font=("Arial",15),borderwidth=4,relief="solid").place(x=870,y=842)

accumulator: int = 0
program: str = ""
Thread(target=errorChecking).start()

app.mainloop()
