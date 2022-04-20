from tkinter import *
from languages import *
import random

class FastFingers:
    def __init__(self,parent):
        self.parent = parent
        self.time = 30
        self.dTime = self.time
        self.wpm = 0
        self.score = 0
        self.words = []
        self.isStarted = False

        self.initUI()

    def initUI(self):
        self.setWordFrame()
        self.setEntryFrame()
        self.checkEntry()

    def setWordFrame(self):
        self.wordFrame = Frame(self.parent,highlightbackground="gray",highlightthickness=1,height=40,bg="white")
        self.wordFrame.pack(expand=True,fill=BOTH)

        self.setWords()

    def setEntryFrame(self):
        self.entryFrame = Frame(self.parent,bg=BGCOLOR)
        self.entryFrame.pack(expand=True,fill=BOTH,padx=80)

        self.restart = Button(self.entryFrame,text="Restart",width=7,command=self.restart)
        self.restart.pack(pady=5,side=LEFT,padx=5)

        self.newTextBtn = Button(self.entryFrame,text="New Text",width=7,command=self.newText)
        self.newTextBtn.pack(pady=5,side=LEFT,padx=5)
        
        self.entry = Entry(self.entryFrame,width=30,font="Arial 15")
        self.entry.pack(side=LEFT)
        
        self.entry.focus()
        self.parent.bind("<space>",self.isTrue)

        self.timeLabel = Label(self.entryFrame,text=self.time,font="arial 15",bg=BGCOLOR)
        self.timeLabel.pack(side=LEFT,padx=15)

    def newText(self):
        self.words = []
        self.wpm = 0
        
        for widget in self.wordFrame.winfo_children():
            widget.destroy()

        self.setWords()

    def setWords(self):
        for i in range(4):
            for j in range(9):
                w = random.choice(language)
                
                words = Label(self.wordFrame,text=w, 
                        font="Consolas 10",bg="white")
                words.place(x=10+j * 75, y=10+i * 30)

                self.words.append([words, i, j])

    def checkEntry(self):
        if (self.wpm % 36 == 0) and (self.wpm != 0):self.newText()

        label = self.words[self.wpm][0]

        if self.entry.get() == " ":self.entry.delete(0,END)
        entry = self.entry.get()

        if not self.isStarted:  
            if len(entry) > 0:
                self.isStarted = True
                self.setTime()

        if not entry == label.cget('text')[0:len(entry)]:label.config(bg="red")
        else:self.words[self.wpm][0].config(bg="lightgrey")

        self.parent.after(50, self.checkEntry)

    def isTrue(self,event):
        entry = event.widget.get().strip()
        if len(entry) > 0:

            word = self.words[self.wpm][0].cget('text').strip()
            label = self.words[self.wpm][0]

            if entry == word:
                self.score += len(word)
                label.config(fg="green",bg='white')

            else:
                label.config(fg="red",bg='white')
                for i in range(len(word)):
                    try:
                        if event.widget[i] == self.words[self.wpm][0][i]:
                            self.score += 1
                    except:
                        pass

            self.wpm += 1
            event.widget.delete(0,END)

    def setTime(self):
        if self.time > 0:
            self.time -= 1
            self.timeLabel.config(text=self.time)

            self.interval = self.timeLabel.after(1000,self.setTime)
        else:
            self.showScore()

    def restart(self):
        try:
            self.timeLabel.after_cancel(self.interval)
        except:
            pass

        for widget in self.parent.winfo_children():
            widget.destroy()

        a = FastFingers(self.parent)

    def showScore(self):
        self.scoreLabel = Label(self.parent,text=f"{int(int(self.score / 4.7) * (60 / self.dTime))}WPM",bg=BGCOLOR,font="arial 18 bold")
        self.scoreLabel.pack()

BGCOLOR = "azure2"
WIDTH = 700
HEIGHT = 300

language = tr

def main():
    root = Tk()

    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.title("Fast Fingers")
    root.config(bg=BGCOLOR)
    root.resizable(False, False)

    a1 = FastFingers(root)

    root.mainloop()


if __name__ == '__main__':
    main()