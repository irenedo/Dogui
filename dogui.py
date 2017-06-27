#!/usr/bin/env python3

from dimages import *
from tkinter import *
import docker


class App:

    def __init__(self, master):
        self.master = master
        self.master.title("Dockerhub images management")
        self.dockerClient = docker.from_env()
        self.imageManagement = Button(self.master,
                                      text="Image management",
                                      width=15,
                                      height=15,
                                      relief=FLAT,
                                      bg='SlateGray3',
                                      command=lambda: Dimages(self.master, self.dockerClient))
        self.imageManagement.grid(column=0, row=0)
        self.buttonQuit = Button(self.master,
                                 text="Quit",
                                 width=15,
                                 height=15,
                                 relief=FLAT,
                                 command=lambda:
                                 self.master.destroy())
        self.buttonQuit.grid(column=1, row=0)


if __name__ == '__main__':
    root = Tk()
    gui = App(root)
    root.mainloop()
