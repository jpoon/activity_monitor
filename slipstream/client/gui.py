#!/usr/bin/python

import Tkinter
 
class App:
   def __init__(self, master):
      button = Tkinter.Button(master, text="I'm a Button.")
      button.pack()
 
if __name__ == '__main__':
   root = Tkinter.Tk()
   app = App(root)
   root.mainloop()


