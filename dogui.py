#!/usr/bin/env python3

from dimages import *
from inspection import *
from tkinter import *
from tkinter import ttk, messagebox
from time import ctime
import docker


def start_container(app, container_id):
    app.dockerClient.start(container_id)
    app.get_running_containers()


def stop_container(app, container_id):
    app.dockerClient.stop(container_id)
    app.get_running_containers()


def kill_container(app, container_id):
    app.dockerClient.kill(container_id)
    app.get_running_containers()


def restart_container(app, container_id):
    app.dockerClient.restart(container_id)
    app.get_running_containers()


def remove_container(app, container_id):
    app.dockerClient.remove_container(container_id)
    app.get_running_containers()


class App:
    def update(self):
        self.get_running_containers()
        self.master.after(1000, self.update)

    def get_container_id(self):
        clist = []
        for cid in self.runningContainersListbox.curselection():
            clist.append(self.runningContainersListbox.get(cid)[:20].replace(' ', ''))

        return clist

    def start_containers(self):
        if not self.runningContainersListbox.curselection():
            return False
        container_id = self.get_container_id()
        [threading.Thread(target=start_container, args=(self, container)).start() for container in container_id]

    def stop_containers(self):
        if not self.runningContainersListbox.curselection():
            return False
        container_id = self.get_container_id()
        [threading.Thread(target=stop_container, args=(self, container)).start() for container in container_id]

    def restart_containers(self):
        if not self.runningContainersListbox.curselection():
            return False
        container_id = self.get_container_id()
        [threading.Thread(target=restart_container, args=(self, container)).start() for container in container_id]

    def kill_containers(self):
        if not self.runningContainersListbox.curselection():
            return False
        container_id = self.get_container_id()
        [threading.Thread(target=kill_container, args=(self, container)).start() for container in container_id]

    def inspect_containers(self):
        if not self.runningContainersListbox.curselection():
            return False
        container_id = self.get_container_id()
        for container in container_id:
            Inspection(topwindow=self.master, container=container, dockerclient=self.dockerClient)

    @property
    def remove_containers(self):
        if not self.runningContainersListbox.curselection():
            return False
        container_id = self.get_container_id()
        for container in container_id:
            if self.dockerClient.inspect_container(container)['State']['Running']:
                messagebox.showerror(message="Can't remove container {} because is running.\n"
                                             "Please kill or stop it before removing".format(container))
            else:
                threading.Thread(target=remove_container, args=(self, container)).start()

    def get_running_containers(self):
        running = []
        for item in self.dockerClient.containers(all=True):
            container = item['Id'][0:10].center(20)[:20] \
                        + item['Image'].center(20)[:20] \
                        + item['Command'].center(20)[:20] \
                        + ctime(item['Created']).center(30)[:30] \
                        + item['Names'][0][1:].center(20)[:20] \
                        + item['NetworkSettings']['Networks']['bridge']['IPAddress'].center(20)[:20] \
                        + item['Status'].center(20)[:20]
            running.append(container)

        self.runningContainers.set(value=running)

    def __init__(self, master):
        self.master = master
        self.master.title("Dogui")
        self.master.minsize(1000, 600)
        self.master.resizable(width=False, height=False)
        self.master.rowconfigure(0, weight=1)
        self.dockerClient = docker.from_env()

        # LAUNCH CONTAINER BUTTON
        self.containerManagement = Button(self.master,
                                          text="Launch\nContainer",
                                          width=30,
                                          height=4,
                                          relief=FLAT,
                                          bg='gray',
                                          command=lambda: messagebox.showinfo(message="Work In Progress"))
        self.containerManagement.grid(column=0, row=0, padx=(10, 10), pady=(10, 10))

        # IMAGE MANAGEMENT BUTTON
        self.imageManagement = Button(self.master,
                                      text="Image \n management",
                                      width=30,
                                      height=4,
                                      relief=FLAT,
                                      bg='gray',
                                      command=lambda: Dimages(self.master, self.dockerClient))
        self.imageManagement.grid(column=1, row=0, padx=(10, 10), pady=(10, 10))

        # BUILD CONTAINER BUTTON
        self.buttonBuild = Button(self.master,
                                  text="Build Container",
                                  width=30,
                                  height=4,
                                  relief=FLAT,
                                  bg='gray',
                                  command=lambda: messagebox.showinfo(message="Work In Progress"))
        self.buttonBuild.grid(column=0, row=1, padx=(10, 10), pady=(10, 10))

        # QUIT BUTTON
        self.buttonQuit = Button(self.master,
                                 text="Quit",
                                 width=30,
                                 height=4,
                                 relief=FLAT,
                                 bg='gray',
                                 command=lambda:
                                 self.master.destroy())
        self.buttonQuit.grid(column=1, row=1, padx=(10, 10), pady=(10, 10))

        # CONTAINERS FRAME
        self.runningContainersFrame = ttk.Labelframe(self.master,
                                                     relief=GROOVE,
                                                     text='Running containers')
        self.runningContainersFrame.grid(column=0, row=2,
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
                                                 + 'NetworkSettings'.center(20)
                                                 + 'Status'.center(20))
        self.runningContainersLabel.grid(column=0, row=0,
                                         padx=(4, 0),
                                         sticky=W)
        self.runningContainersListbox = Listbox(self.runningContainersFrame,
                                                listvariable=self.runningContainers,
                                                height=25,
                                                width=140,
                                                relief=FLAT,
                                                selectmode='extended',
                                                font=('monospace', 8),
                                                bg='cornsilk2',
                                                exportselection=False)
        self.runningContainersListbox.grid(column=0, row=1,
                                           rowspan=6,
                                           padx=(4, 0),
                                           sticky=(N, E, W))
        # Scroll y
        self.runningContainersListboxScrolly = Scrollbar(self.runningContainersFrame,
                                                         orient=VERTICAL,
                                                         bd=0,
                                                         relief=FLAT,
                                                         command=self.runningContainersListbox)
        self.runningContainersListboxScrolly.grid(row=1, column=2,
                                                  rowspan=5,
                                                  sticky=(N, S))
        self.runningContainersListbox['yscrollcommand'] = self.runningContainersListboxScrolly.set

        # BUTTON START CONTAINER
        self.buttonStartContainer = Button(self.runningContainersFrame,
                                           text="Start",
                                           width=10,
                                           height=2,
                                           relief=FLAT,
                                           bg='gray',
                                           command=lambda: self.start_containers())
        self.buttonStartContainer.grid(column=4, row=1, padx=(2, 2))

        # BUTTON STOP CONTAINER
        self.buttonHaltContainer = Button(self.runningContainersFrame,
                                          text="Stop",
                                          width=10,
                                          height=2,
                                          relief=FLAT,
                                          bg='gray',
                                          command=lambda: self.stop_containers())
        self.buttonHaltContainer.grid(column=4, row=2, padx=(2, 2))

        # BUTTON RESTART CONTAINER
        self.buttonRestartContainer = Button(self.runningContainersFrame,
                                             text="Restart",
                                             width=10,
                                             height=2,
                                             relief=FLAT,
                                             bg='gray',
                                             command=lambda: self.restart_containers())
        self.buttonRestartContainer.grid(column=4, row=3, padx=(2, 2))

        # BUTTON KILL CONTAINER
        self.buttonKillContainer = Button(self.runningContainersFrame,
                                          text="Kill",
                                          width=10,
                                          height=2,
                                          relief=FLAT,
                                          bg='gray',
                                          command=lambda: self.kill_containers())
        self.buttonKillContainer.grid(column=4, row=4, padx=(2, 2))

        # BUTTON INSPECT CONTAINER
        self.buttonInspectContainer = Button(self.runningContainersFrame,
                                             text="Inspect",
                                             width=10,
                                             height=2,
                                             relief=FLAT,
                                             bg='gray',
                                             command=lambda: self.inspect_containers())
        self.buttonInspectContainer.grid(column=4, row=5, padx=(2, 2))

        # BUTTON REMOVE CONTAINER
        self.buttonInspectContainer = Button(self.runningContainersFrame,
                                             text="Remove",
                                             width=10,
                                             height=2,
                                             relief=FLAT,
                                             bg='gray',
                                             command=lambda: self.remove_containers)
        self.buttonInspectContainer.grid(column=4, row=6, padx=(2, 2))

        self.update()


if __name__ == '__main__':
    root = Tk()
    gui = App(root)
    root.mainloop()
