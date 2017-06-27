#!/usr/bin/env python3

from dimages import *
import docker


class App:

    def __init__(self, master):
        self.master = master
        self.master.title("Dockerhub images management")

        self.master.resizable(width=False, height=False)
        self.dockerClient = docker.from_env()
        Dimages(self.master, self.dockerClient)


if __name__ == '__main__':
    root = Tk()
    gui = App(root)

    root.mainloop()
