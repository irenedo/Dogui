import threading
from functions import *
from tkinter import *
from tkinter import ttk, messagebox


class Launch:
    def launch_container(self):
        try:
            image = self.launch_Images.get(self.launch_Images.curselection())
        except:
            return False

        tag = self.launch_imageTag.get()
        if not tag:
            tag = 'latest'
        container = '{}:{}'.format(image, tag)
        threading.Thread(target=run_container, args=(self, container)).start()

    def list_launch_hub_images(self, event):
        image = self.launch_pattern.get()
        if image != "Enter image name...":
            try:
                hub_images = [x['name'] for x in self.dockerClient.images.search(image) if x['name'] != []]
                self.launch_remoteImages.set(value=hub_images)
            except:
                messagebox.showerror(message='There was an error getting docker hub images')
        else:
            pass

    def initialize_launch_search_input(self, event):
        self.launch_pattern.set(value="")
        self.launch_searchInput.unbind('<Button-1>')

    def add_ports_to_list(self):
        host_port = self.launch_hostPort.get()
        container_port = self.launch_containerPort.get()
        if host_port == '' or container_port == '':
            return False
        try:
            host_port = int(host_port)
            container_port = int(container_port)
        except ValueError:
            messagebox.showinfo(message="Ports must be numbers between 1 and 65535")
            return False

        if host_port < 1 or host_port > 65535 or container_port < 1 or container_port > 65535:
            messagebox.showinfo(message="Ports must be numbers between 1 and 65535")
            return False
        else:
            self.launch_portsList.insert(END, "{}:{}".format(host_port, container_port))

    def remove_ports_from_list(self):
        [self.launch_portsList.delete(x) for x in self.launch_portsList.curselection()]

    def add_dirs_to_list(self):
        host_dir = self.storage_localDir.get()
        container_dir = self.storage_ContainerDir.get()
        if host_dir == '' or container_dir == '':
            return False

        self.storage_mountPointsList.insert(END, "{}:{}".format(host_dir, container_dir))

    def remove_dirs_from_list(self):
        [self.storage_mountPointsList.delete(x) for x in self.storage_mountPointsList.curselection()]

    def draw_images_frame(self, parent):
        # Search Entry
        parent.columnconfigure(0, weight=1)
        self.launch_pattern = StringVar(value="Enter image name...")
        self.launch_searchInput = Entry(parent,
                                        bg='cornsilk2',
                                        width=20,
                                        relief=FLAT,
                                        textvariable=self.launch_pattern)
        self.launch_searchInput.grid(row=0, column=0,
                                     padx=2)
        self.launch_searchInput.bind('<Return>', self.list_launch_hub_images)
        self.launch_searchInput.bind('<Button-1>', self.initialize_launch_search_input)

        # Search button
        Button(parent,
               text="Search",
               relief=FLAT,
               bg='SlateGray3',
               command=lambda:
               self.list_launch_hub_images(event=None)).grid(row=1, column=0,
                                                             pady=(0, 6))
        self.launch_remoteImages = StringVar(value="")

        listimages_frame = ttk.Frame(parent)
        listimages_frame.grid(row=2, column=0,
                              sticky=W,
                              columnspan=2)
        # Remote Images Listbox
        self.launch_Images = Listbox(listimages_frame,
                                     listvariable=self.launch_remoteImages,
                                     relief=FLAT,
                                     bg='cornsilk2',
                                     exportselection=False)
        self.launch_Images.grid(row=0, column=0,
                                sticky=(N, W, E, S),
                                padx=(4, 0))

        # Scroll y
        rImagesScrolly = Scrollbar(listimages_frame,
                                   orient=VERTICAL,
                                   bd=0,
                                   relief=FLAT,
                                   command=self.launch_Images.yview)
        rImagesScrolly.grid(row=0, column=1,
                            sticky=(N, S),
                            padx=(0, 4))
        self.launch_Images['yscrollcommand'] = rImagesScrolly.set

        # Scroll x
        rImagesScrollx = Scrollbar(listimages_frame,
                                   orient=HORIZONTAL,
                                   bd=0,
                                   relief=FLAT,
                                   command=self.launch_Images.xview)
        rImagesScrollx.grid(row=1, column=0,
                            sticky=(W, E),
                            padx=(4, 0))
        self.launch_Images['xscrollcommand'] = rImagesScrollx.set

        # Tag Label
        Label(parent,
              text="Tag:").grid(row=4, column=0,
                                padx=(2, 0),
                                pady=(4, 4),
                                sticky=W)

        # Tag Entry
        self.launch_imageTag = StringVar(value='latest')
        self.launch_tagEntry = Entry(parent,
                                     width=17,
                                     bg='cornsilk2',
                                     relief=FLAT,
                                     textvariable=self.launch_imageTag)
        self.launch_tagEntry.grid(row=4, column=0,
                                  padx=(30, 0),
                                  pady=(4, 4),
                                  sticky=W)

    def draw_options_frame(self, parent):
        parent.columnconfigure(1, weight=1)
        Label(parent, text="Override Command:").grid(row=0, column=0,
                                                     pady=(2, 2),
                                                     sticky=W)
        self.LaunchInstanceCommand = StringVar()
        Entry(parent,
              bg='cornsilk2',
              relief=FLAT,
              textvariable=self.LaunchInstanceCommand).grid(row=0, column=1,
                                                            sticky=(E, W),
                                                            pady=(2, 2),
                                                            padx=(4, 4))

        self.LaunchInstancetty = IntVar()
        Checkbutton(parent,
                    relief=FLAT,
                    text="tty",
                    variable=self.LaunchInstancetty).grid(row=1, column=0,
                                                          pady=(2, 2),
                                                          sticky=W)
        self.LaunchPrivileged = IntVar()
        Checkbutton(parent,
                    relief=FLAT,
                    text="Privileged",
                    variable=self.LaunchPrivileged).grid(row=2, column=0,
                                                         pady=(2, 2),
                                                         sticky=W)
        self.autoRemove = IntVar()
        Checkbutton(parent,
                    relief=FLAT,
                    text="Auto Remove",
                    variable=self.autoRemove).grid(row=3, column=0,
                                                   pady=(2, 2),
                                                   sticky=W)
        self.readOnly = IntVar()
        Checkbutton(parent,
                    relief=FLAT,
                    text="Mount Read Only",
                    variable=self.readOnly).grid(row=4, column=0,
                                                 pady=(2, 2),
                                                 sticky=W)

    def draw_network_frame(self, parent):
        # Se ha de poner un checkbutton para publish all
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)

        Label(parent, text="Host port").grid(row=0, column=0,
                                             pady=(2, 2),
                                             padx=(2, 2))
        Label(parent, text="Container port").grid(row=0, column=1,
                                                  pady=(2, 2),
                                                  padx=(2, 2))

        self.launch_hostPort = StringVar()
        Entry(parent,
              bg='cornsilk2',
              relief=FLAT,
              textvariable=self.launch_hostPort).grid(row=1, column=0,
                                                      sticky=(E, W),
                                                      pady=(2, 2),
                                                      padx=(4, 4))

        self.launch_containerPort = StringVar()
        Entry(parent,
              bg='cornsilk2',
              relief=FLAT,
              textvariable=self.launch_containerPort).grid(row=1, column=1,
                                                           sticky=(E, W),
                                                           pady=(2, 2),
                                                           padx=(4, 4))

        Button(parent,
               text="Add",
               relief=FLAT,
               bg='SlateGray3',
               command=self.add_ports_to_list).grid(row=2, column=0,
                                                    columnspan=2,
                                                    pady=(2, 2))
        ports_list = ttk.Frame(parent)
        ports_list.grid(row=3, column=0, columnspan=2)
        self.launch_ports = StringVar()
        self.launch_portsList = Listbox(ports_list,
                                        listvariable=self.launch_ports,
                                        relief=FLAT,
                                        height=5,
                                        width=25,
                                        bg='cornsilk2',
                                        exportselection=False)
        self.launch_portsList.grid(row=0, column=0)
        # Scroll y
        launch_portsListy = Scrollbar(ports_list,
                                      orient=VERTICAL,
                                      bd=0,
                                      relief=FLAT,
                                      command=self.launch_portsList.yview)
        launch_portsListy.grid(row=0, column=1,
                               sticky=(N, S, E),
                               padx=(0, 4))
        self.launch_portsList['yscrollcommand'] = launch_portsListy.set

        Button(parent,
               text="Remove",
               relief=FLAT,
               bg='SlateGray3',
               command=self.remove_ports_from_list).grid(row=4, column=0,
                                                         columnspan=2,
                                                         pady=(2, 2))
        self.publishAll = IntVar()
        Checkbutton(parent,
                    relief=FLAT,
                    text="Publish All Ports",
                    variable=self.publishAll).grid(row=5, column=0,
                                                   pady=(2, 2),
                                                   sticky=W)

    def draw_storage_frame(self, parent):
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)

        Label(parent, text="Host directory").grid(row=0, column=0,
                                                  pady=(2, 2),
                                                  padx=(2, 2))
        Label(parent, text="Mount Point").grid(row=0, column=1,
                                               pady=(2, 2),
                                               padx=(2, 2))
        self.storage_localDir = StringVar()
        Entry(parent,
              bg='cornsilk2',
              relief=FLAT,
              textvariable=self.storage_localDir).grid(row=1, column=0,
                                                       sticky=(E, W),
                                                       pady=(2, 2),
                                                       padx=(4, 4))

        self.storage_ContainerDir = StringVar()
        Entry(parent,
              bg='cornsilk2',
              relief=FLAT,
              textvariable=self.storage_ContainerDir).grid(row=1, column=1,
                                                           sticky=(E, W),
                                                           pady=(2, 2),
                                                           padx=(4, 4))
        Button(parent,
               text="Add",
               relief=FLAT,
               bg='SlateGray3',
               command=self.add_dirs_to_list).grid(row=2, column=0,
                                                   columnspan=2,
                                                   pady=(2, 2))
        dir_list = ttk.Frame(parent)
        dir_list.grid(row=3, column=0, columnspan=2)
        self.storage_mountPoints = StringVar()
        self.storage_mountPointsList = Listbox(dir_list,
                                               listvariable=self.storage_mountPoints,
                                               relief=FLAT,
                                               height=5,
                                               width=25,
                                               bg='cornsilk2',
                                               exportselection=False)
        self.storage_mountPointsList.grid(row=0, column=0)
        # Scroll y
        storage_mountPointsy = Scrollbar(dir_list,
                                         orient=VERTICAL,
                                         bd=0,
                                         relief=FLAT,
                                         command=self.storage_mountPointsList.yview)
        storage_mountPointsy.grid(row=0, column=1,
                                  sticky=(N, S, E),
                                  padx=(0, 4))
        self.storage_mountPointsList['yscrollcommand'] = storage_mountPointsy.set

        Button(parent,
               text="Remove",
               relief=FLAT,
               bg='SlateGray3',
               command=self.remove_dirs_from_list).grid(row=4, column=0,
                                                        columnspan=2,
                                                        pady=(2, 2))

    def draw_launch_container_frame(self):
        self.launch_frame.columnconfigure(0, weight=1)
        self.launch_frame.columnconfigure(1, weight=1)
        self.launch_frame.columnconfigure(2, weight=1)
        self.launch_frame.columnconfigure(3, weight=1)
        self.launch_frame.columnconfigure(4, weight=1)
        self.launch_frame.rowconfigure(0, weight=1)

        # Images Frame
        #########
        images_frame = ttk.Labelframe(self.launch_frame,
                                      relief=GROOVE,
                                      text='Images')
        images_frame.grid(row=0, column=0,
                          sticky=(N, S, W, E))
        self.draw_images_frame(images_frame)
        #########

        # Options Frame
        #########
        options_frame = ttk.Labelframe(self.launch_frame,
                                       relief=GROOVE,
                                       text='Options')
        options_frame.grid(row=0, column=1,
                           sticky=(N, S, W, E))
        self.draw_options_frame(options_frame)
        #########

        # Network Options Frame
        #########
        network_frame = ttk.Labelframe(self.launch_frame,
                                       relief=GROOVE,
                                       text='Network')
        network_frame.grid(row=0, column=2,
                           sticky=(N, S, W, E))
        self.draw_network_frame(network_frame)
        #########

        # Storage Options Frame
        #########
        storage_frame = ttk.Labelframe(self.launch_frame,
                                       relief=GROOVE,
                                       text='Storage')
        storage_frame.grid(row=0, column=3,
                           sticky=(N, S, W, E))
        self.draw_storage_frame(storage_frame)
        #########

        Button(self.launch_frame,
               text="Launch",
               relief=FLAT,
               bg='dark olive green',
               command=lambda: self.launch_container()).grid(row=0, column=4,
                                                             sticky=(N, S))

    def __init__(self, master, docker_client):
        self.launch_frame = master
        self.dockerClient = docker_client
        self.LaunchInstanceCommand = None
        self.LaunchInstanceDetached = None
        self.LaunchInstancetty = None
        self.launch_remoteImages = None
        self.launch_Images = None
        self.launch_imageTag = None
        self.launch_tagEntry = None
        self.launch_pattern = None
        self.launch_searchInput = None
        self.launch_hostPort = None
        self.launch_containerPort = None
        self.launch_portsList = None
        self.launch_ports = None
        self.storage_localDir = None
        self.storage_ContainerDir = None
        self.storage_mountPointsList = None
        self.storage_mountPoints = None
        self.LaunchPrivileged = None
        self.autoRemove = None
        self.publishAll = None
        self.readOnly = None
        self.draw_launch_container_frame()
