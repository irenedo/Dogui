from tkinter import *


def execute_launch_container(inst):
    pass


class Linstance:

    def launch_container(self):
        pass

    def __init__(self, master):

        Label(master, text="Name :").grid(row=0, column=0, sticky=W)
        self.LaunchInstanceName = StringVar()
        Entry(master,
              width=17,
              bg='cornsilk2',
              relief=FLAT,
              textvariable=self.LaunchInstanceName).grid(row=0, column=0,
                                                         sticky=W,
                                                         padx=(40, 0))
        Button(master,
               text="Launch",
               width=10,
               height=2,
               relief=FLAT,
               bg='gray',
               command=lambda: self.launch_container()).grid(row=1, column=0)
