from tkinter import *


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
        [data.insert(END, line) for line in pretty_print(dockerclient.inspect_container(container)).split('||')]

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
        quit_button = Button(window,
                             text="Close",
                             relief=FLAT,
                             bg='gray',
                             command=lambda: window.destroy())
        quit_button.grid(row=2, column=0,
                         columnspan=2,
                         pady=(5, 10), padx=(0, 5))