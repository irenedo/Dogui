#!/usr/bin/env python3

import docker
from images import *
from launch import *
from tkinter import ttk, messagebox
from tkinter import *


class App(Images, Launch):
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
            if self.dockerClient.containers.list(all=True, filters={'id': container})[0].attrs['State']['Running']:
                messagebox.showerror(message="Can't remove container {} because is running.\n"
                                             "Please kill or stop it before removing".format(container))
            else:
                threading.Thread(target=remove_container, args=(self, container)).start()

    def get_running_containers(self):
        running = []
        for item in self.dockerClient.containers.list(all=True,
                                                      filters={'status':
                                                                   ['created',
                                                                    'restarting',
                                                                    'running',
                                                                    'paused',
                                                                    'exited']}):
            cid = item.attrs['Id'][0:10].center(20)[:20]
            image = item.attrs['Config']['Image'].center(20)[:20]
            cmd = item.attrs['Config']['Cmd']
            if cmd is None:
                cmd = ' ' * 20
            else:
                cmd = ''.join(cmd).center(20)[:20]
            datetime = item.attrs['Created'].split('.')[0].replace('T', ' ').center(25)[:30]
            name = item.attrs['Name'][1:].center(20)[:20]
            ip = item.attrs['NetworkSettings']['Networks']['bridge']['IPAddress'].center(20)[:20]
            status = item.attrs['State']['Status'].center(20)[:20]
            container = cid + image + cmd + datetime + name + ip + status
            running.append(container)

        self.runningContainers.set(value=running)

    def draw_containers_frame(self):
        runningContainersFrame = ttk.Labelframe(self.master,
                                                relief=GROOVE,
                                                text='Running containers')
        runningContainersFrame.grid(column=0, row=1,
                                    padx=(4, 4), pady=(4, 4),
                                    sticky=(S, E, W))
        runningContainersFrame.columnconfigure(0, weight=1)
        self.runningContainers = StringVar()
        Label(runningContainersFrame,
              font=('monospace', 9, 'bold'),
              foreground='gray',
              text='Id'.center(20)
                   + 'Image'.center(20)
                   + 'Command'.center(20)
                   + 'Created'.center(25)
                   + 'Names'.center(20)
                   + 'NetworkSettings'.center(20)
                   + 'Status'.center(20)).grid(column=0, row=0,
                                               padx=(4, 0),
                                               sticky=W)
        self.runningContainersListbox = Listbox(runningContainersFrame,
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
        runningContainersListboxScrolly = Scrollbar(runningContainersFrame,
                                                    orient=VERTICAL,
                                                    bd=0,
                                                    relief=FLAT,
                                                    command=self.runningContainersListbox)
        runningContainersListboxScrolly.grid(row=1, column=1,
                                             pady=(2, 6),
                                             rowspan=6,
                                             sticky=(N, S))
        self.runningContainersListbox['yscrollcommand'] = runningContainersListboxScrolly.set

        # BUTTON START CONTAINER
        Button(runningContainersFrame,
               text="Start",
               width=10,
               height=2,
               relief=FLAT,
               bg='gray',
               command=lambda: self.start_containers()).grid(column=2, row=1,
                                                             sticky=N,
                                                             padx=(2, 2))

        # BUTTON STOP CONTAINER
        Button(runningContainersFrame,
               text="Stop",
               width=10,
               height=2,
               relief=FLAT,
               bg='gray',
               command=lambda: self.stop_containers()).grid(column=2, row=2,
                                                            padx=(2, 2))

        # BUTTON RESTART CONTAINER
        Button(runningContainersFrame,
               text="Restart",
               width=10,
               height=2,
               relief=FLAT,
               bg='gray',
               command=lambda: self.restart_containers()).grid(column=2, row=3,
                                                               padx=(2, 2))

        # BUTTON KILL CONTAINER
        Button(runningContainersFrame,
               text="Kill",
               width=10,
               height=2,
               relief=FLAT,
               bg='gray',
               command=lambda: self.kill_containers()).grid(column=2, row=4,
                                                            padx=(2, 2))

        # BUTTON INSPECT CONTAINER
        Button(runningContainersFrame,
               text="Inspect",
               width=10,
               height=2,
               relief=FLAT,
               bg='gray',
               command=lambda: self.inspect_containers()).grid(column=2, row=5,
                                                               padx=(2, 2))

        # BUTTON REMOVE CONTAINER
        Button(runningContainersFrame,
               text="Remove",
               width=10,
               height=2,
               relief=FLAT,
               bg='gray',
               command=lambda: self.remove_containers()).grid(column=2, row=6,
                                                              padx=(2, 2))

    def __init__(self, master):
        self.master = master
        self.master.title("Dogui")
        self.master.minsize(1000, 600)
        self.master.resizable(width=False, height=False)
        self.master.rowconfigure(0, weight=1)
        self.dockerClient = docker.from_env(version="1.24")

        ##############
        # Main Frame #
        ##############

        self.Notebook = ttk.Notebook(self.master)
        self.Notebook.grid(row=0, column=0,
                           sticky=(N, S, E, W))

        # Draw Launch Container tab
        self.launchContainer = Frame(self.Notebook)
        self.Notebook.add(self.launchContainer, text="Launch Container")
        Launch.__init__(self, self.launchContainer, self.dockerClient)
        #########

        # Draw Advance tab
        self.advanced = Frame(self.Notebook)
        self.advanced.columnconfigure(0, weight=1)
        self.advanced.rowconfigure(0, weight=1)
        self.Notebook.add(self.advanced, text="Advanced")
        labelAdvanced = Label(self.advanced, text="Work In Progress")
        labelAdvanced.grid()
        #########

        # Draw Image Management tab
        self.ImageManagement = Frame(self.Notebook)
        self.ImageManagement.columnconfigure(0, weight=1)
        self.ImageManagement.columnconfigure(1, weight=1)
        self.ImageManagement.rowconfigure(0, weight=1)
        self.Notebook.add(self.ImageManagement, text="Image Management")
        Images.__init__(self, self.ImageManagement, self.dockerClient)
        #########

        # Draw Build Container tab
        self.buildContainer = Frame(self.Notebook)
        self.buildContainer.columnconfigure(0, weight=1)
        self.buildContainer.rowconfigure(0, weight=1)
        self.Notebook.add(self.buildContainer, text="Build Container")
        labelBuildContainer = Label(self.buildContainer, text="Work In Progress")
        labelBuildContainer.grid()
        #########

        # Draw About tab
        self.About = Frame(self.Notebook)
        self.About.columnconfigure(0, weight=1)
        self.About.rowconfigure(0, weight=1)
        self.Notebook.add(self.About, text="About")
        Label(self.About,
              text="Dogui v0.0.1").grid(row=0, column=0,
                                        sticky=(N, S, E, W))
        #########

        # draw containers list
        self.runningContainers = None
        self.runningContainersListbox = None
        self.draw_containers_frame()
        #########

        self.update()


if __name__ == '__main__':
    root = Tk()
    gui = App(root)
    root.mainloop()
