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
                hub_images = [x['name'] for x in self.dockerClient.search(image) if x['name'] != []]
                self.launch_remoteImages.set(value=hub_images)
            except:
                messagebox.showerror(message='There was an error getting docker hub images')
        else:
            pass

    def initialize_launch_search_input(self, event):
        self.launch_pattern.set(value="")
        self.launch_searchInput.unbind('<Button-1>')

    def draw_images_frame(self, parent):
        # Search Entry
        self.launch_pattern = StringVar(value="Enter image name...")
        self.launch_searchInput = Entry(parent,
                                        bg='cornsilk2',
                                        relief=FLAT,
                                        textvariable=self.launch_pattern)
        self.launch_searchInput.grid(row=0, column=0,
                                     sticky=W,
                                     padx=2)
        self.launch_searchInput.bind('<Return>', self.list_launch_hub_images)
        self.launch_searchInput.bind('<Button-1>', self.initialize_launch_search_input)

        # Search button
        Button(parent,
               text="Search",
               relief=FLAT,
               bg='SlateGray3',
               command=lambda:
               self.list_launch_hub_images(event=None)).grid(row=0, column=0,
                                                             padx=(180, 0),
                                                             pady=(0, 6),
                                                             sticky=W)
        self.launch_remoteImages = StringVar(value="")

        # Remote Images Listbox
        self.launch_Images = Listbox(parent,
                                     listvariable=self.launch_remoteImages,
                                     width=40,
                                     relief=FLAT,
                                     bg='cornsilk2',
                                     exportselection=False)
        self.launch_Images.grid(row=1, column=0,
                                padx=(4, 0))

        # Scroll y
        rImagesScrolly = Scrollbar(parent,
                                   orient=VERTICAL,
                                   bd=0,
                                   relief=FLAT,
                                   command=self.launch_Images.yview)
        rImagesScrolly.grid(row=1, column=2,
                            sticky=(W, N, S),
                            padx=(0, 4))
        self.launch_Images['yscrollcommand'] = rImagesScrolly.set

        # Scroll x
        rImagesScrollx = Scrollbar(parent,
                                   orient=HORIZONTAL,
                                   bd=0,
                                   relief=FLAT,
                                   command=self.launch_Images.xview)
        rImagesScrollx.grid(row=2, column=0,
                            sticky=(W, E, N),
                            padx=(4, 0))
        self.launch_Images['xscrollcommand'] = rImagesScrollx.set

        # Tag Label
        Label(parent,
              text="Tag:").grid(row=3, column=0,
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
        self.launch_tagEntry.grid(row=3, column=0,
                                  padx=(30, 0),
                                  pady=(4, 4),
                                  sticky=W)

    def draw_network_frame(self, parent):
        Label(parent, text="Work In Progress").grid(row=0, column=0,
                                                    pady=(2, 2),
                                                    sticky=W)

    def draw_storage_frame(self, parent):
        Label(parent, text="Work In Progress").grid(row=0, column=0,
                                                    pady=(2, 2),
                                                    sticky=W)

    def draw_options_frame(self, parent):
        Label(parent, text="Override Command:").grid(row=0, column=0,
                                                     pady=(2, 2),
                                                     sticky=W)
        self.LaunchInstanceCommand = StringVar()
        Entry(parent,
              width=17,
              bg='cornsilk2',
              relief=FLAT,
              textvariable=self.LaunchInstanceCommand).grid(row=0, sticky=W,
                                                            column=1,
                                                            pady=(2, 2),
                                                            padx=(75, 0))
        self.LaunchInstanceDetached = IntVar()
        Checkbutton(parent,
                    relief=FLAT,
                    text="deattached",
                    variable=self.LaunchInstanceDetached).grid(row=1, column=0,
                                                               pady=(2, 2),
                                                               sticky=W)

        self.LaunchInstancetty = IntVar()
        Checkbutton(parent,
                    relief=FLAT,
                    text="tty",
                    variable=self.LaunchInstancetty).grid(row=2, column=0,
                                                          pady=(2, 2),
                                                          sticky=W)

    def draw_launch_container_frame(self):
        self.launch_frame.columnconfigure(0, weight=1)
        self.launch_frame.columnconfigure(1, weight=1)
        self.launch_frame.columnconfigure(2, weight=1)
        self.launch_frame.rowconfigure(0, weight=1)

        images_frame = ttk.Labelframe(self.launch_frame,
                                      relief=GROOVE,
                                      text='Images')
        images_frame.grid(row=0, column=0,
                          sticky=(N, S, W, E))
        self.draw_images_frame(images_frame)

        options_frame = ttk.Labelframe(self.launch_frame,
                                       relief=GROOVE,
                                       text='Options')
        options_frame.grid(row=0, column=1,
                           sticky=(N, S, W, E))
        self.draw_options_frame(options_frame)

        network_frame = ttk.Labelframe(self.launch_frame,
                                       relief=GROOVE,
                                       text='Network')
        network_frame.grid(row=0, column=2,
                           sticky=(N, S, W, E))
        self.draw_network_frame(network_frame)

        storage_frame = ttk.Labelframe(self.launch_frame,
                                       relief=GROOVE,
                                       text='Storage')
        storage_frame.grid(row=0, column=3,
                           sticky=(N, S, W, E))
        self.draw_storage_frame(storage_frame)

        Button(self.launch_frame,
               text="Launch",
               width=10,
               height=2,
               relief=FLAT,
               bg='gray',
               command=lambda: self.launch_container()).grid(row=0, column=4,
                                                             sticky=W)

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
        self.draw_launch_container_frame()
