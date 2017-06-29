#!/usr/bin/env python3

from dimages import *
from tkinter import *
from tkinter import ttk
from time import ctime
import docker


def pretty_print(d, off=' '):
    output = ''
    if type(d) is list:
        for item in d:
            if type(item) is list or type(item) is dict:
                output += off + "- " + "||"
                output += pretty_print(item, off=off + '  ')
            else:
                output += off + "- " + str(item) + "||"
    elif type(d) is dict:
        for key in sorted(d.keys()):
            if type(d[key]) is list or type(d[key]) is dict:
                output += off + key + ": " + "||"
                output += pretty_print(d[key], off=off + '  ')
            else:
                output += off + key + ": " + str(d[key]) + "||"
    return output


class App:
    def kill_container(self):
        container_id = self.get_container_id()
        self.dockerClient.kill(container_id)
        self.get_running_containers()

    def restart_container(self):
        container_id = self.get_container_id()
        self.dockerClient.restart(container_id)
        self.get_running_containers()

    def get_container_id(self):
        return self.runningContainersListbox.get(self.runningContainersListbox.curselection())[0:20].replace(' ', '')

    def inspect_container(self):
        if not self.runningContainersListbox.curselection():
            return False

        container_id = self.get_container_id()

        window = Toplevel(self.master)
        window.title('Container ID:' + container_id)
        data = Listbox(window,
                       font=('monospace', 9, 'bold'),
                       height=40,
                       width=100,
                       relief=FLAT,
                       bg='cornsilk2',
                       selectmode=BROWSE)

        data.grid(column=0, row=0,
                  sticky=W)
        [data.insert(END, line) for line in pretty_print(self.dockerClient.inspect_container(container_id)).split('||')]

        # Scroll y
        y_scroll = Scrollbar(window,
                             orient=VERTICAL,
                             bd=0,
                             relief=FLAT,
                             command=data.yview)
        y_scroll.grid(row=0, column=1,
                      sticky=(N, S))
        data['yscrollcommand'] = y_scroll.set

        # Scroll x
        x_scroll = Scrollbar(window,
                             orient=HORIZONTAL,
                             bd=0,
                             relief=FLAT,
                             command=data.xview)
        x_scroll.grid(row=1, column=0,
                      sticky=(W, E))
        data['xscrollcommand'] = x_scroll.set

        # Quit button
        quit_button = Button(window,
                             text="Close",
                             relief=FLAT,
                             bg='SlateGray3',
                             command=lambda: window.destroy())
        quit_button.grid(row=2, column=0,
                         columnspan=2,
                         pady=(5, 10), padx=(0, 5))

    def get_running_containers(self):
        running = []
        for item in self.dockerClient.containers():
            container = item['Id'][0:10].center(20) \
                        + item['Image'].center(20) \
                        + item['Command'].center(20) \
                        + ctime(item['Created']).center(30) \
                        + item['Names'][0][1:].center(20) \
                        + item['NetworkSettings']['Networks']['bridge']['IPAddress'].center(20)
            running.append(container)

        self.runningContainers.set(value=running)

    def __init__(self, master):
        self.master = master
        self.master.title("Dogui")
        self.master.minsize(1000, 600)
        self.master.resizable(width=False, height=False)
        self.master.rowconfigure(0, weight=1)
        self.dockerClient = docker.from_env()
        self.containerManagement = Button(self.master,
                                          text="Launch\nInstance",
                                          width=10,
                                          height=4,
                                          relief=FLAT,
                                          bg='SlateGray3',
                                          command=lambda: messagebox.showinfo(message="Work In Progress"))
        self.containerManagement.grid(column=0, row=0, padx=(10, 10), pady=(10, 10))
        self.imageManagement = Button(self.master,
                                      text="Image \n management",
                                      width=10,
                                      height=4,
                                      relief=FLAT,
                                      bg='SlateGray3',
                                      command=lambda: Dimages(self.master, self.dockerClient))
        self.imageManagement.grid(column=1, row=0, padx=(10, 10), pady=(10, 10))
        self.buttonQuit = Button(self.master,
                                 text="Quit",
                                 width=10,
                                 height=4,
                                 relief=FLAT,
                                 bg='SlateGray3',
                                 command=lambda:
                                 self.master.destroy())
        self.buttonQuit.grid(column=2, row=0, padx=(10, 10), pady=(10, 10))
        self.runningContainersFrame = ttk.Labelframe(self.master,
                                                     relief=GROOVE,
                                                     text='Running containers')
        self.runningContainersFrame.grid(column=0, row=1,
                                         padx=(4, 4), pady=(4, 4),
                                         sticky=(S, E, W),
                                         columnspan=3)
        self.runningContainersFrame.columnconfigure(0, weight=1)
        self.runningContainers = StringVar()
        self.runningContainersLabel = Label(self.runningContainersFrame,
                                            font=('monospace', 9, 'bold'),
                                            foreground='blue',
                                            text='Id'.center(20)
                                                 + 'Image'.center(20)
                                                 + 'Command'.center(20)
                                                 + 'Created'.center(30)
                                                 + 'Names'.center(20)
                                                 + 'NetworkSettings'.center(20))
        self.runningContainersLabel.grid(column=0, row=0,
                                         padx=(4, 0),
                                         sticky=W)
        self.runningContainersListbox = Listbox(self.runningContainersFrame,
                                                listvariable=self.runningContainers,
                                                height=25,
                                                width=140,
                                                relief=FLAT,
                                                font=('monospace', 8),
                                                bg='cornsilk2',
                                                exportselection=False)
        self.runningContainersListbox.grid(column=0, row=1,
                                           rowspan=4,
                                           padx=(4, 0),
                                           sticky=(N, E, W))
        # Scroll y
        self.runningContainersListboxScrolly = Scrollbar(self.runningContainersFrame,
                                                         orient=VERTICAL,
                                                         bd=0,
                                                         relief=FLAT,
                                                         command=self.runningContainersListbox)
        self.runningContainersListboxScrolly.grid(row=1, column=2,
                                                  rowspan=4,
                                                  sticky=(N, S))
        self.runningContainersListbox['yscrollcommand'] = self.runningContainersListboxScrolly.set

        self.buttonKillContainer = Button(self.runningContainersFrame,
                                          text="Kill",
                                          width=10,
                                          height=4,
                                          relief=FLAT,
                                          bg='SlateGray3',
                                          command=lambda: self.kill_container())
        self.buttonKillContainer.grid(column=4, row=1, padx=(10, 10), pady=(10, 10))
        self.buttonHaltContainer = Button(self.runningContainersFrame,
                                          text="Halt",
                                          width=10,
                                          height=4,
                                          relief=FLAT,
                                          bg='SlateGray3',
                                          command=lambda: messagebox.showinfo(message="Work In Progress"))
        self.buttonHaltContainer.grid(column=4, row=2, padx=(10, 10), pady=(10, 10))
        self.buttonRestartContainer = Button(self.runningContainersFrame,
                                             text="Restart",
                                             width=10,
                                             height=4,
                                             relief=FLAT,
                                             bg='SlateGray3',
                                             command=lambda: self.restart_container())
        self.buttonRestartContainer.grid(column=4, row=3, padx=(10, 10), pady=(10, 10))
        self.buttonInspectContainer = Button(self.runningContainersFrame,
                                             text="Inspect",
                                             width=10,
                                             height=4,
                                             relief=FLAT,
                                             bg='SlateGray3',
                                             command=lambda: self.inspect_container())
        self.buttonInspectContainer.grid(column=4, row=4, padx=(10, 10), pady=(10, 10))
        self.get_running_containers()


if __name__ == '__main__':
    root = Tk()
    gui = App(root)
    root.mainloop()
