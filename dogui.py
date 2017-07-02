#!/usr/bin/env python3

from dimages import *
from launch_instance import *
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

    def remove_containers(self):
        if not self.runningContainersListbox.curselection():
            pass
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

    def show_about(self, master):
        self.aboutLabel = Label(master, text="Dogui v0.0.1")
        self.aboutLabel.grid(row=0, column=0,
                             sticky=(N, S, E, W))

    def draw_containers_frame(self):
        self.runningContainersFrame = ttk.Labelframe(self.master,
                                                     relief=GROOVE,
                                                     text='Running containers')
        self.runningContainersFrame.grid(column=0, row=1,
                                         padx=(4, 4), pady=(4, 4),
                                         sticky=(S, E, W))
        self.runningContainersFrame.columnconfigure(0, weight=1)
        self.runningContainers = StringVar()
        Label(self.runningContainersFrame,
              font=('monospace', 9, 'bold'),
              foreground='blue',
              text='Id'.center(20)
                   + 'Image'.center(20)
                   + 'Command'.center(20)
                   + 'Created'.center(30)
                   + 'Names'.center(20)
                   + 'NetworkSettings'.center(20)
                   + 'Status'.center(20)).grid(column=0, row=0,
                                               padx=(4, 0),
                                               sticky=W)
        self.runningContainersListbox = Listbox(self.runningContainersFrame,
                                                listvariable=self.runningContainers,
                                                height=20,
                                                width=140,
                                                relief=FLAT,
                                                selectmode='extended',
                                                font=('monospace', 8),
                                                bg='cornsilk2',
                                                exportselection=False)
        self.runningContainersListbox.grid(column=0, row=1,
                                           rowspan=6,
                                           padx=(4, 0),
                                           pady=(2, 6),
                                           sticky=(N, E, W))
        # Scroll y
        self.runningContainersListboxScrolly = Scrollbar(self.runningContainersFrame,
                                                         orient=VERTICAL,
                                                         bd=0,
                                                         relief=FLAT,
                                                         command=self.runningContainersListbox)
        self.runningContainersListboxScrolly.grid(row=1, column=1,
                                                  pady=(2, 6),
                                                  rowspan=6,
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
        self.buttonStartContainer.grid(column=2, row=1,
                                       sticky=N,
                                       padx=(2, 2))

        # BUTTON STOP CONTAINER
        self.buttonStopContainer = Button(self.runningContainersFrame,
                                          text="Stop",
                                          width=10,
                                          height=2,
                                          relief=FLAT,
                                          bg='gray',
                                          command=lambda: self.stop_containers())
        self.buttonStopContainer.grid(column=2, row=2, padx=(2, 2))

        # BUTTON RESTART CONTAINER
        self.buttonRestartContainer = Button(self.runningContainersFrame,
                                             text="Restart",
                                             width=10,
                                             height=2,
                                             relief=FLAT,
                                             bg='gray',
                                             command=lambda: self.restart_containers())
        self.buttonRestartContainer.grid(column=2, row=3, padx=(2, 2))

        # BUTTON KILL CONTAINER
        self.buttonKillContainer = Button(self.runningContainersFrame,
                                          text="Kill",
                                          width=10,
                                          height=2,
                                          relief=FLAT,
                                          bg='gray',
                                          command=lambda: self.kill_containers())
        self.buttonKillContainer.grid(column=2, row=4, padx=(2, 2))

        # BUTTON INSPECT CONTAINER
        self.buttonInspectContainer = Button(self.runningContainersFrame,
                                             text="Inspect",
                                             width=10,
                                             height=2,
                                             relief=FLAT,
                                             bg='gray',
                                             command=lambda: self.inspect_containers())
        self.buttonInspectContainer.grid(column=2, row=5, padx=(2, 2))

        # BUTTON REMOVE CONTAINER
        self.buttonRemoveContainer = Button(self.runningContainersFrame,
                                            text="Remove",
                                            width=10,
                                            height=2,
                                            relief=FLAT,
                                            bg='gray',
                                            command=lambda: self.remove_containers())
        self.buttonRemoveContainer.grid(column=2, row=6, padx=(2, 2))

    def __init__(self, master):
        self.master = master
        self.master.title("Dogui")
        self.master.minsize(1000, 600)
        self.master.resizable(width=False, height=False)
        self.master.rowconfigure(0, weight=1)
        self.dockerClient = docker.from_env()

        ##############
        # Main Frame #
        ##############

        self.Notebook = ttk.Notebook(self.master)
        self.Notebook.grid(row=0, column=0,
                           sticky=(N, S, E, W))

        # Draw Launch Container tab
        self.launchContainer = Frame(self.Notebook)
        self.Notebook.add(self.launchContainer, text="Launch Container")
        Linstance(self.launchContainer)
        #########

        # Draw Advance tab
        self.advanced = Frame(self.Notebook)
        self.advanced.columnconfigure(0, weight=1)
        self.advanced.rowconfigure(0, weight=1)
        self.Notebook.add(self.advanced, text="Advanced")
        self.labelAdvanced = Label(self.advanced, text="Work In Progress")
        self.labelAdvanced.grid()
        #########

        # Draw Image Management tab
        self.ImageManagement = Frame(self.Notebook)
        self.ImageManagement.columnconfigure(0, weight=1)
        self.ImageManagement.rowconfigure(0, weight=1)
        self.Notebook.add(self.ImageManagement, text="Image Management")
        Dimages(master=self.ImageManagement, docker_client=self.dockerClient)
        #########

        # Draw Build Container tab
        self.buildContainer = Frame(self.Notebook)
        self.buildContainer.columnconfigure(0, weight=1)
        self.buildContainer.rowconfigure(0, weight=1)
        self.Notebook.add(self.buildContainer, text="Build Container")
        self.labelBuildContainer = Label(self.buildContainer, text="Work In Progress")
        self.labelBuildContainer.grid()
        #########

        # Draw About tab
        self.About = Frame(self.Notebook)
        self.About.columnconfigure(0, weight=1)
        self.About.rowconfigure(0, weight=1)
        self.Notebook.add(self.About, text="About")
        self.aboutLabel = None
        self.show_about(self.About)
        #########

        # draw containers list
        self.runningContainersFrame = None
        self.runningContainers = None
        self.runningContainersListbox = None
        self.runningContainersListboxScrolly = None
        self.buttonStartContainer = None
        self.buttonStopContainer = None
        self.buttonRestartContainer = None
        self.buttonKillContainer = None
        self.buttonInspectContainer = None
        self.buttonRemoveContainer = None
        self.draw_containers_frame()
        #########

        self.update()


if __name__ == '__main__':
    root = Tk()
    gui = App(root)
    root.mainloop()
