from encryption import *
import os
from passgen import *
import configparser
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd 

def new_password():
    passlen = passlene.get()
    if passlen == '':
        passlen = 16
    else:
        passlen = int(passlen)
    passexclude = passexe.get()
    password = generate_password(passlen, passexclude)
    passentry.delete(0, tk.END)
    passentry.insert(tk.END, password)

def add_cred():
    section = secentry.get()
    username = userentry.get()
    password = passentry.get()
    fabspath = filepath.get()
    config = configparser.ConfigParser()
    config.read(fabspath)
    if not section in config.sections():
        config.add_section(section)
    config[section][username] = password
    with open(fabspath, 'w') as f:
        config.write(f)
    _readfile(fabspath)
    secentry.delete(0, tk.END)
    userentry.delete(0, tk.END)
    passentry.delete(0, tk.END)

def openembedfile():
    ifilepath.delete(0, tk.END)
    ifabspath = fd.askopenfilename(
            filetypes = [
                ('Accepted Formats', '.wav .jpg .jpeg .gif .png'),
                ],
            title = 'Please choose Image/Audio File'
            )
    ifilepath.insert(tk.END, ifabspath)

def opendatafile():
    filepath.delete(0, tk.END)
    fabspath = fd.askopenfilename(title = 'Please choose Data File')
    _readfile(fabspath)
    filepath.insert(tk.END, fabspath)

def _readfile(fabspath):
    mylist.delete(0, tk.END)
    f = open(fabspath, 'rb')
    c = f.read()
    f.close()
    mylist.insert(tk.END, *c.splitlines())
    #filecontent.set(c)

def enc():
    fabspath = filepath.get()
    key = keyentry.get()
    statuslabel.set('Encrypting File')
    encryptfile(key, fabspath, fabspath)
    statuslabel.set('Encrypted!')
    _readfile(fabspath)
    #filepath.delete(0, tk.END)

def dec():
    key = keyentry.get()
    fabspath = filepath.get()
    statuslabel.set('Decrypting File...')
    decryptfile(key, fabspath, fabspath)
    statuslabel.set('Decrypted!')
    _readfile(fabspath)
    #filepath.delete(0, tk.END)


master = tk.Tk()
master.title('3ncryp710n T00lz')
statuslabel = tk.StringVar()
#filecontent = tk.StringVar()
width = 600
height = 500
screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()
x = (screen_width//2) - (width//2)
y = (screen_height//2) - (height//2)
master.geometry(f'{width}x{height}+{x}+{y}')
tk.Label(master, text="Data File").grid(row=0)
tk.Label(master, text="Encryption Key").grid(row=1)
tk.Label(master, textvariable=statuslabel).grid(row=2, column = 1, sticky=tk.W)
myscroll = tk.Scrollbar(master)
myscroll.grid(row=3, column = 2, sticky='nw')
#myscroll.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
mylist = tk.Listbox(master, yscrollcommand = myscroll.set, width = 50)
mylist.grid(row=3, column = 1, columnspan=3, sticky=tk.W)
#mylist.pack(side = tk.LEFT, fill = Y, expand = False)
myscroll.config( command = mylist.yview )

#tk.Label(master, textvariable=filecontent, height = 10, wraplength = 300, justify = 'left').grid(row=2, column = 1)
#mycanvas = tk.Canvas(master)
#myframe = tk.Frame(mycanvas)
#mycanvas.configure(yscrollcommand=myscroll.set)
#mycanvas.create_window(0, 0, window=myframe, anchor='nw')
#mycanvas.grid(row = 3, column = 1)
#myframe.grid()
#myscroll.grid(row=0, column = 1)
#mylabel.grid(row=0, column = 0)
#myframe = tk.Frame(canvas)
#myentry = tk.Entry(canvas, justify = 'left')
#myscroll.pack(side = 'right', fill = 'y')
#canvas.pack(side="left", fill="both", expand=True)
#tk.Label(master, textvariable=filecontent, height = 7, wraplength = 300, justify = 'left').grid(row=3, column = 1)

tk.Label(master, text="Credential").grid(row=15)
tk.Label(master, text="Section").grid(row=14, column = 1, sticky=tk.W)
tk.Label(master, text="Username").grid(row=14, column = 2, sticky=tk.W)
tk.Label(master, text="Password").grid(row=19)#, column = 0, sticky=tk.W)
tk.Label(master, text="Password Length").grid(row=17, column = 0)
tk.Label(master, text="Password Exclude").grid(row=18, column = 0)
filepath = tk.Entry(master)
keyentry = tk.Entry(master)
secentry = tk.Entry(master)
userentry = tk.Entry(master)
passentry = tk.Entry(master, width = 40)
passlene = tk.Entry(master)
passexe = tk.Entry(master)

filepath.grid(row=0, column=1, sticky=tk.W)
keyentry.grid(row=1, column=1, sticky=tk.W)
secentry.grid(row=15, column = 1, sticky=tk.W)
userentry.grid(row=15, column = 2, sticky=tk.W)
passentry.grid(row=19, column = 1, sticky=tk.W, columnspan = 2)
passlene.grid(row = 17, column = 1, sticky=tk.W)
passexe.grid(row = 18, column = 1, sticky=tk.W)
passlene.insert(tk.END, '16')
passexe.insert(tk.END, '%')

tk.Button(master, text = 'Generate Password', command = new_password).grid(row=16, column =1, sticky=tk.W, pady = 4)
tk.Button(master, text = 'Add Password', command = add_cred).grid(row=16, column =2, sticky=tk.W, pady = 4)

tk.Button(master, text = 'Browse', command = opendatafile, bd = 7).grid(row=0, column =2, sticky=tk.W)
tk.Button(master, bg = 'red', text='Encrypt', command=enc).grid(row=10, column=1, sticky=tk.W, pady=4)
tk.Button(master, bg = 'green', text='Decrypt', command=dec).grid(row=10, column=2, sticky=tk.W, pady=4)
tk.Button(master, text='Quit', command=master.quit).grid(row=20, column=0, sticky=tk.W, pady=4)
master.grid_columnconfigure(5, weight = 2)
master.grid_columnconfigure(4, weight = 2)

tk.mainloop()

