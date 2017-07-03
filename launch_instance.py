from tkinter import *
import threading


def run_container(inst, container, command):
    if not inst.dockerClient.images(container):
        inst.dockerClient.pull(container)

    detach = False
    tty = False
    if inst.LaunchInstanceDetached.get() == 1:
        detach = True

    if inst.LaunchInstancetty.get() == 1:
        tty = True

    cid = inst.dockerClient.create_container(container,
                                             command=command,
                                             detach=detach,
                                             tty=tty)['Id']
    inst.dockerClient.start(cid)


class Linstance:
    def launch_container(self):
        image = self.LaunchInstanceName.get()
        tag = self.LaunchInstanceTag.get()
        command = self.LaunchInstanceCommand.get()
        if tag is '':
            tag = 'latest'

        container = '{}:{}'.format(image, tag)
        threading.Thread(target=run_container, args=(self, container, command)).start()

    def __init__(self, master, docker_client):
        self.dockerClient = docker_client
        Label(master, text="Name:").grid(row=0, column=0,
                                         pady=(2, 2),
                                         sticky=W)
        self.LaunchInstanceName = StringVar()
        Entry(master,
              width=17,
              bg='cornsilk2',
              relief=FLAT,
              textvariable=self.LaunchInstanceName).grid(row=0, column=0,
                                                         sticky=W,
                                                         pady=(2, 2),
                                                         padx=(45, 0))
        Label(master, text="Tag:").grid(row=0, column=0,
                                        pady=(2, 2),
                                        sticky=W,
                                        padx=(190, 0))
        self.LaunchInstanceTag = StringVar(value="latest")
        Entry(master,
              width=17,
              bg='cornsilk2',
              relief=FLAT,
              textvariable=self.LaunchInstanceTag).grid(row=0, sticky=W,
                                                        column=0,
                                                        pady=(2, 2),
                                                        padx=(225, 0))
        Label(master, text="Command:").grid(row=1, column=0,
                                            pady=(2, 2),
                                            sticky=W)
        self.LaunchInstanceCommand = StringVar()
        Entry(master,
              width=17,
              bg='cornsilk2',
              relief=FLAT,
              textvariable=self.LaunchInstanceCommand).grid(row=1, sticky=W,
                                                            column=0,
                                                            pady=(2, 2),
                                                            padx=(75, 0))
        self.LaunchInstanceDetached = IntVar()
        Checkbutton(master,
                    relief=FLAT,
                    text="deattached",
                    variable=self.LaunchInstanceDetached).grid(row=2, column=0,
                                                               pady=(2, 2),
                                                               sticky=W)

        self.LaunchInstancetty = IntVar()
        Checkbutton(master,
                    relief=FLAT,
                    text="tty",
                    variable=self.LaunchInstancetty).grid(row=3, column=0,
                                                          pady=(2, 2),
                                                          sticky=W)
        Button(master,
               text="Launch",
               width=10,
               height=2,
               relief=FLAT,
               bg='gray',
               command=lambda: self.launch_container()).grid(row=4, column=0)
