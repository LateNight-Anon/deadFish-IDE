#A GUI IDE for the esoteric programming languahe DeadFish

from tkinter import Tk, Text, Label, Button, END
from tkinter.filedialog import askopenfilename
from threading import Thread
from time import sleep
from csv import reader

app = Tk()
app.resizable(width=False, height=False)
app.geometry("1000x900")
app.title("deadFish IDE")
Label(text="deadFish IDE",font=("Arial",35)).place(x=400,y=20)
programEntry = Text(width=43,height=16,font=("Arial",30),borderwidth=4,relief="solid")
programEntry.place(x=25,y=90)
syntaxErrorLabel = Label(text="program is empty", fg="orange",font=("Arial",25))
syntaxErrorLabel.place(x=20,y=840)

def createErrorMessage(message: str) -> None:
    errorLabel.place(x=50,y=30)
    errorLabel.configure(text=message)
    sleep(2)
    errorLabel.place(x=999,y=999)

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
    accumulator: int = 0
    for command in program:
        if command == 'i': accumulator += 1
        elif command == 'd': accumulator -= 1
        elif command == 's': accumulator **= 2
        elif command == 'o': print(accumulator, end=' ')
        else:
            print("\nerror detected")
            return
        if accumulator > 255: accumulator = 0
        if accumulator < 0: accumulator = 255

def openCode() -> None:
    directory: str = askopenfilename()
    try:
        if directory[-4] + directory[-3] + directory[-2] + directory[-1] == "dead": file = open(directory,'r')
        else: Thread(target=createErrorMessage,args=("invalid file extension",)).start()
    except Exception: Thread(target=createErrorMessage,args=("invalid file",)).start()
    else:
        with file:
            fileData = next(reader(file))
            print(fileData)
            programEntry.delete('1.0', END)
            programEntry.insert(END,fileData)

def writeCodeToFile() -> None:
    directory: str = askopenfilename()
    try:
        if directory[-4] + directory[-3] + directory[-2] + directory[-1] == "dead": file = open(directory,'w')
        else: Thread(target=createErrorMessage,args=("invalid file extension",)).start()
    except Exception: Thread(target=createErrorMessage,args=("invalid file",)).start()
    else:
        with file: file.write(programEntry.get('1.0','end-1c'))

def liveAccumulator() -> None:
    while True:
        accumulator: int = 0
        for command in program:
            if command == 'i': accumulator += 1
            elif command == 'd': accumulator -= 1
            elif command == 's': accumulator **= 2
            if accumulator > 255: accumulator = 0
            elif accumulator < 0: accumulator = 255
        accumulatorLabel.configure(text=accumulator)

Button(text="open file",command=openCode,font=("Arial",15),borderwidth=4,relief="solid").place(x=630,y=842)
Button(text="save file",command=writeCodeToFile,font=("Arial",15),borderwidth=4,relief="solid").place(x=750,y=842)
Button(text="execute",command=interpret,font=("Arial",15),borderwidth=4,relief="solid").place(x=870,y=842)
errorLabel = Label(text="",font=("Arial",25),fg="red")
errorLabel.place(x=999,y=999)
accumulatorLabel = Label(text="accumulator = 0",font=("Arial",25))
accumulatorLabel.place(x=400,y=845)

program: str = ""
Thread(target=errorChecking).start()
Thread(target=liveAccumulator).start()

app.mainloop()
