import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self,root):
        root.title("Kashir")
        height=1080
        width=1920
        screenheight=root.winfo_screenheight()
        screenwidth=root.winfo_screenwidth()
        alignstr="%dx%xd+%d+%d"%(width,height,(screenwidth-width/2),(screenheight-height)/2)
        root.geometry(alignstr)
        root.resizable(width=True,height=True)
        
if __name__=="__main__":
    root=tk.Tk()
    app=App(root)
    root.mainloop()
