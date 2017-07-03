from tkinter import *
from tkinter import ttk, messagebox
import threading


def execute_pulling(app, image):
    app.queuedTasks['images'][image] = 'pulling'
    app.list_local_images()
    app.dockerClient.pull(image)
    del app.queuedTasks['images'][image]
    app.list_local_images()


class Dimages:
    def list_hub_images(self, event):
        image = self.pattern.get()
        if image != "Enter image name...":
            try:
                hub_images = [x['name'] for x in self.dockerClient.search(image) if x['name'] != []]
                self.remoteImages.set(value=hub_images)
            except:
                messagebox.showerror(message='There was an error getting docker hub images')
        else:
            pass

    def list_local_images(self):
        local_images = [x['RepoTags'] for x in self.dockerClient.images()
                        if x['RepoTags'] != ['<none>:<none>'] and
                        x['RepoTags'] is not None]
        tasks = [['{}({}...)'.format(img, self.queuedTasks['images'][img])]
                 for img in self.queuedTasks['images'].keys()]
        self.localImages.set(value=local_images + tasks)

    def pull_images(self):
        if self.rImages.curselection():
            try:
                idx = self.rImages.get(self.rImages.curselection())
                tag = self.tagEntry.get()
                image = '{}:{}'.format(idx, tag)
                if image not in self.localImages.get():
                    threading.Thread(target=execute_pulling, args=(self, image)).start()
                else:
                    messagebox.showerror(message='Image already pulled')
            except:
                messagebox.showerror(message='There was an error removing images')

    def remove_images(self):
        img = self.lImages.get(self.lImages.curselection())[0]
        if img.split('(')[0] in self.queuedTasks['images'].keys():
            messagebox.showinfo(message="Can't remove an image that is being processed")
        else:
            try:
                self.dockerClient.remove_image(img)
                self.list_local_images()
            except:
                messagebox.showerror(message='There was an error removing images')

    def initialize_search_input(self, event):
        self.pattern.set(value="")
        self.searchInput.unbind('<Button-1>')

    def __init__(self, master, docker_client):

        self.queuedTasks = {'images': {}, }
        self.dockerClient = docker_client

        # Remote images Frame
        ############
        remoteFrame = ttk.Labelframe(master,
                                     relief=GROOVE,
                                     text='Remote images')
        remoteFrame.grid(row=0, column=0,
                         pady=(4, 4),
                         padx=(4, 4),
                         sticky=E)
        self.remoteImages = StringVar(value="")

        # Remote Images Listbox
        self.rImages = Listbox(remoteFrame,
                               listvariable=self.remoteImages,
                               height=10,
                               width=60,
                               relief=FLAT,
                               bg='cornsilk2',
                               exportselection=False)
        self.rImages.grid(row=1, column=0,
                          padx=(4, 0))

        # Scroll y
        rImagesScrolly = Scrollbar(remoteFrame,
                                   orient=VERTICAL,
                                   bd=0,
                                   relief=FLAT,
                                   command=self.rImages.yview)
        rImagesScrolly.grid(row=1, column=2,
                            sticky=(W, N, S),
                            padx=(0, 4))
        self.rImages['yscrollcommand'] = rImagesScrolly.set

        # Scroll x
        rImagesScrollx = Scrollbar(remoteFrame,
                                   orient=HORIZONTAL,
                                   bd=0,
                                   relief=FLAT,
                                   command=self.rImages.xview)
        rImagesScrollx.grid(row=2, column=0,
                            sticky=(W, E, N),
                            padx=(4, 0))
        self.rImages['xscrollcommand'] = rImagesScrollx.set

        # Tag Label
        Label(remoteFrame,
              text="Tag:").grid(row=3, column=0,
                                padx=(2, 0),
                                sticky=W)

        # Tag Entry
        self.imageTag = StringVar(value='latest')
        self.tagEntry = Entry(remoteFrame,
                              width=17,
                              bg='cornsilk2',
                              relief=FLAT,
                              textvariable=self.imageTag)
        self.tagEntry.grid(row=3, column=0,
                           padx=(30, 0),
                           sticky=W)

        # Pull button
        Button(remoteFrame,
               text="Pull",
               relief=FLAT,
               bg='SlateGray3',
               command=self.pull_images).grid(row=3, column=0,
                                              padx=(180, 4),
                                              pady=(0, 6),
                                              sticky=W)

        # Search Entry
        self.pattern = StringVar(value="Enter image name...")
        self.searchInput = Entry(remoteFrame,
                                 bg='cornsilk2',
                                 relief=FLAT,
                                 textvariable=self.pattern)
        self.searchInput.grid(row=0, column=0,
                              sticky=W,
                              padx=2)
        self.searchInput.bind('<Return>', self.list_hub_images)
        self.searchInput.bind('<Button-1>', self.initialize_search_input)

        # Search button
        Button(remoteFrame,
               text="Search",
               relief=FLAT,
               bg='SlateGray3',
               command=lambda:
               self.list_hub_images(event=None)).grid(row=0, column=0,
                                                      padx=(180, 0),
                                                      pady=(0, 6),
                                                      sticky=W)
        ############

        # Local images Frame
        ############
        # Main Frame
        localFrame = ttk.Labelframe(master,
                                    relief=GROOVE,
                                    text='Local images')
        localFrame.grid(row=0, column=1,
                        padx=(4, 4),
                        pady=(4, 4),
                        sticky=W)
        self.localImages = StringVar(value="")
        self.list_local_images()

        # Local Images Listbox
        self.lImages = Listbox(localFrame,
                               listvariable=self.localImages,
                               height=10,
                               width=60,
                               relief=FLAT,
                               bg='cornsilk2',
                               borderwidth=0,
                               selectmode='extended',
                               exportselection=False)
        self.lImages.grid(row=0, column=0,
                          sticky=(N, W, S, E),
                          padx=(4, 0), pady=(37, 0))

        # Scroll y
        self.lImagesScroll = Scrollbar(localFrame,
                                       orient=VERTICAL,
                                       bd=0,
                                       relief=FLAT,
                                       command=self.lImages.yview)
        self.lImagesScroll.grid(row=0, column=1,
                                sticky=(W, N, S),
                                padx=(0, 4), pady=(30, 0))
        self.lImages['yscrollcommand'] = self.lImagesScroll.set

        # Scroll x
        lImagesScrollx = Scrollbar(localFrame,
                                   orient=HORIZONTAL,
                                   bd=0,
                                   relief=FLAT,
                                   command=self.lImages.xview)
        lImagesScrollx.grid(row=2, column=0,
                            sticky=(W, E, N),
                            padx=(4, 0))
        self.lImages['xscrollcommand'] = lImagesScrollx.set

        # Remove Button
        Button(localFrame,
               text="Remove",
               relief=FLAT,
               bg='SlateGray3',
               command=self.remove_images).grid(row=3, column=0,
                                                padx=(4, 4), pady=(0, 4))
        ############
