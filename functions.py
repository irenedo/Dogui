from tkinter import *


def execute_pulling(app, image):
    app.queuedTasks['images'][image] = 'pulling'
    app.list_local_images()
    app.dockerClient.images.pull(image)
    del app.queuedTasks['images'][image]
    app.list_local_images()


def start_container(app, container_id):
    container = app.dockerClient.containers.list(all=True, filters={'id': container_id})[0]
    container.start()
    app.get_running_containers()


def stop_container(app, container_id):
    container = app.dockerClient.containers.list(all=True, filters={'id': container_id})[0]
    container.stop()
    app.get_running_containers()


def kill_container(app, container_id):
    container = app.dockerClient.containers.list(all=True, filters={'id': container_id})[0]
    container.kill()
    app.get_running_containers()


def restart_container(app, container_id):
    container = app.dockerClient.containers.list(all=True, filters={'id': container_id})[0]
    container.restart()
    app.get_running_containers()


def remove_container(app, container_id):
    container = app.dockerClient.containers.list(all=True, filters={'id': container_id})[0]
    container.remove()
    app.get_running_containers()


def run_container(inst, container):
    tty = False
    privileged = False
    autoRemove = False
    publishAll = False
    readonly = False

    if inst.LaunchInstancetty.get() == 1:
        tty = True

    if inst.LaunchPrivileged.get() == 1:
        privileged = True

    if inst.autoRemove.get() == 1:
        autoRemove = True

    if inst.publishAll.get() == 1:
        publishAll = True

    if inst.readOnly.get() == 1:
        readonly = True

    command = inst.LaunchInstanceCommand.get()

    if container not in inst.localImages.get():
        execute_pulling(inst, container)

    port_bindings = {}
    if not publishAll:
        for ports in inst.launch_portsList.get(0, END):
            port_bindings[ports.split(":")[1]] = ports.split(":")[0]

    mount_points = {}
    for dirs in inst.storage_mountPointsList.get(0, END):
        mount_points[dirs.split(":")[0]] = {'bind': dirs.split(":")[1], 'mode': 'rw'}

    inst.dockerClient.containers.run(container,
                                     command=command,
                                     detach=True, # hay que ver cómo tratarlo
                                     tty=tty,
                                     ports=port_bindings,
                                     privileged=privileged,
                                     remove=autoRemove,
                                     publish_all_ports=publishAll,
                                     volumes=mount_points)


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


class Inspection:
    def __init__(self, topwindow, container, dockerclient):
        window = Toplevel(topwindow)
        window.title('Container ID:' + container)
        data = Listbox(window,
                       font=('monospace', 9, 'bold'),
                       height=40,
                       width=100,
                       relief=FLAT,
                       bg='cornsilk2',
                       selectmode=BROWSE)

        data.grid(column=0, row=0,
                  sticky=W)
        [data.insert(END, line)
         for line in
         pretty_print(dockerclient.containers.list(all=True, filters={'id': container})[0].attrs).split('||')]

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
        Button(window,
               text="Close",
               relief=FLAT,
               bg='gray',
               command=lambda: window.destroy()).grid(row=2, column=0,
                                                      columnspan=2,
                                                      pady=(5, 10), padx=(0, 5))
