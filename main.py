#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk, messagebox
import pdb
import docker
import threading


def execute_pulling(app, image):
    app.queuedTasks['images'][image] = 'pulling'
    app.list_local_images()
    app.dockerClient.pull(image)
    del app.queuedTasks['images'][image]
    app.list_local_images()


class App:
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
        tasks = [['{}({}...)'.format(img, self.queuedTasks['images'][img])] for img in self.queuedTasks['images'].keys()]

        self.localImages.set(value=local_images+tasks)

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
            messagebox.showinfo(message="You can't remove an image"
                                " that is being processed")
        else:
            try:
                self.dockerClient.remove_image(img)
                self.list_local_images()
            except:
                messagebox.showerror(message='There was an error removing images')

    def initialize_search_input(self, event):
        self.pattern.set(value="")
        self.searchInput.unbind('<Button-1>')

    def print_image_management(self):
        self.master.title("Dockerhub images management")

        self.master.resizable(width=False, height=False)

        self.quitButton = Button(self.master, text="Quit", command=lambda: self.master.destroy())
        self.quitButton.grid(row=2, column=1, sticky=E, columnspan=2, pady=(5, 10), padx=(0, 5))

        # Local images Frame
        ############
        # Main Frame
        self.localFrame = ttk.Labelframe(self.master, text='Local images')
        self.localFrame.grid(row=1, column=1, padx=(4, 4))
        self.localImages = StringVar(value="")
        self.list_local_images()

        # Local Images Listbox
        self.lImages = Listbox(self.localFrame, listvariable=self.localImages,
                               height=15, width=30, selectmode='extended')
        self.lImages.grid(row=0, column=0, sticky=(N, W, S, E), padx=(4, 0), pady=(30, 0))

        # Scroll y
        self.lImagesScroll = Scrollbar(self.localFrame, orient=VERTICAL, command=self.lImages.yview)
        self.lImagesScroll.grid(row=0, column=1, sticky=(W, N, S), padx=(0, 4), pady=(30, 0))
        self.lImages['yscrollcommand'] = self.lImagesScroll.set

        # Scroll x
        self.lImagesScrollx = Scrollbar(self.localFrame, orient=HORIZONTAL, command=self.lImages.xview)
        self.lImagesScrollx.grid(row=2, column=0, sticky=(W, E, N), padx=(4, 0))
        self.lImages['xscrollcommand'] = self.lImagesScrollx.set

        # Remove Button
        self.removeButton = Button(self.localFrame, text="Remove", command=self.remove_images)
        self.removeButton.grid(row=3, column=0, columnspan=2, padx=(4, 4), pady=(4, 4))
        ############

        # Remote images Frame
        ############
        # Main Frame
        self.remoteFrame = ttk.Labelframe(self.master, text='Remote images')
        self.remoteFrame.grid(row=1, column=0, padx=(4, 4))
        self.remoteImages = StringVar(value="")

        # Remote Images Listbox
        self.rImages = Listbox(self.remoteFrame, listvariable=self.remoteImages, height=15, width=30)
        self.rImages.grid(row=1, column=0, sticky=(N, W, S, E), padx=(4, 0), columnspan=2)

        # Scroll y
        self.rImagesScrolly = Scrollbar(self.remoteFrame, orient=VERTICAL, command=self.rImages.yview)
        self.rImagesScrolly.grid(row=1, column=2, sticky=(W, N, S), padx=(0, 4))
        self.rImages['yscrollcommand'] = self.rImagesScrolly.set

        # Scroll x
        self.rImagesScrollx = Scrollbar(self.remoteFrame, orient=HORIZONTAL, command=self.rImages.xview)
        self.rImagesScrollx.grid(row=2, column=0, columnspan=2, sticky=(W, E, N), padx=(4, 0))
        self.rImages['xscrollcommand'] = self.rImagesScrollx.set

        # Tag Label
        self.tagLabel = Label(self.remoteFrame, text="Tag:")
        self.tagLabel.grid(row=3, column=0, sticky=W)

        # Tag Entry
        self.imageTag = StringVar(value='latest')
        self.tagEntry = Entry(self.remoteFrame, width=17, textvariable=self.imageTag)
        self.tagEntry.grid(row=3, column=0, sticky=E, padx=(4, 0))

        # Pull button
        self.pullButton = Button(self.remoteFrame, text="Pull", command=self.pull_images)
        self.pullButton.grid(row=3, column=1, columnspan=2, padx=(4, 4), pady=(4, 4))

        # Search Entry
        self.pattern = StringVar(value="Enter image name...")
        self.searchInput = Entry(self.remoteFrame, textvariable=self.pattern)
        self.searchInput.grid(row=0, column=0, sticky=W, padx=2)
        self.searchInput.bind('<Return>', self.list_hub_images)
        self.searchInput.bind('<Button-1>', self.initialize_search_input)

        # Search button
        self.searchButton = Button(self.remoteFrame, text="Search", command=lambda: self.list_hub_images(event=None))
        self.searchButton.grid(row=0, column=1, pady=(0, 4), sticky=W)
        ############

    def __init__(self, master):
        self.master = master
        self.dockerClient = docker.from_env()
        self.queuedTasks = {'images': {}, }
        self.print_image_management()


if __name__ == '__main__':
    root = Tk()
    gui = App(root)

    root.mainloop()
