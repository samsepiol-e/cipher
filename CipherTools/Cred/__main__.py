from CipherLib.encryption import *
from CipherLib.passgen import *
import configparser
import tkinter as tk
import tkinter.filedialog as fd
import os


class CredGui():
    def __init__(self):
        self.master = tk.Tk()
        self.master.title('3ncryp710n T00lz')
        self.statuslabel = tk.StringVar()
        self.width = 600
        self.height = 500
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width//2) - (self.width//2)
        y = (screen_height//2) - (self.height//2)
        self.master.geometry(f'{self.width}x{self.height}+{x}+{y}')
        tk.Label(self.master, text="Data File").grid(row=0)
        tk.Label(self.master, text="Encryption Key").grid(row=1)
        tk.Label(self.master, textvariable=self.statuslabel).grid(row=2, column = 1, sticky=tk.W)
        self.myscroll = tk.Scrollbar(self.master)
        self.myscroll.grid(row=3, column = 2, sticky='nw')
        #myscroll.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        self.mylist = tk.Listbox(self.master, yscrollcommand = self.myscroll.set, width = 50)
        self.mylist.grid(row=3, column = 1, columnspan=3, sticky=tk.W)
        #self.mylist.pack(side = tk.LEFT, fill = Y, expand = False)
        self.myscroll.config( command = self.mylist.yview )

        #tk.Label(self.master, textvariable=filecontent, height = 10, wraplength = 300, justify = 'left').grid(row=2, column = 1)
        #mycanvas = tk.Canvas(self.master)
        #myframe = tk.Frame(mycanvas)
        #mycanvas.configure(yscrollcommand=self.myscroll.set)
        #mycanvas.create_window(0, 0, window=myframe, anchor='nw')
        #mycanvas.grid(row = 3, column = 1)
        #myframe.grid()
        #self.myscroll.grid(row=0, column = 1)
        #mylabel.grid(row=0, column = 0)
        #myframe = tk.Frame(canvas)
        #myentry = tk.Entry(canvas, justify = 'left')
        #self.myscroll.pack(side = 'right', fill = 'y')
        #canvas.pack(side="left", fill="both", expand=True)
        #tk.Label(self.master, textvariable=filecontent, height = 7, wraplength = 300, justify = 'left').grid(row=3, column = 1)

        tk.Label(self.master, text="Credential").grid(row=15)
        tk.Label(self.master, text="Section").grid(row=14, column = 1, sticky=tk.W)
        tk.Label(self.master, text="Username").grid(row=14, column = 2, sticky=tk.W)
        tk.Label(self.master, text="Password").grid(row=19)#, column = 0, sticky=tk.W)
        tk.Label(self.master, text="Password Length").grid(row=17, column = 0)
        tk.Label(self.master, text="Password Exclude").grid(row=18, column = 0)
        self.filepath = tk.Entry(self.master)
        self.keyentry = tk.Entry(self.master)
        self.secentry = tk.Entry(self.master)
        self.userentry = tk.Entry(self.master)
        self.passentry = tk.Entry(self.master, width = 40)
        self.passlene = tk.Entry(self.master)
        self.passexe = tk.Entry(self.master)

        self.filepath.grid(row=0, column=1, sticky=tk.W)
        self.keyentry.grid(row=1, column=1, sticky=tk.W)
        self.secentry.grid(row=15, column = 1, sticky=tk.W)
        self.userentry.grid(row=15, column = 2, sticky=tk.W)
        self.passentry.grid(row=19, column = 1, sticky=tk.W, columnspan = 2)
        self.passlene.grid(row = 17, column = 1, sticky=tk.W)
        self.passexe.grid(row = 18, column = 1, sticky=tk.W)
        self.passlene.insert(tk.END, '16')
        self.passexe.insert(tk.END, '%')

        tk.Button(self.master, text = 'Generate Password', command = self.new_password).grid(row=16, column =1, sticky=tk.W, pady = 4)
        tk.Button(self.master, text = 'Add Password', command = self.add_cred).grid(row=16, column =2, sticky=tk.W, pady = 4)

        tk.Button(self.master, text = 'Browse', command = self.opendatafile, bd = 7).grid(row=0, column =2, sticky=tk.W)
        tk.Button(self.master, bg = 'red', text='Encrypt', command=self.enc).grid(row=10, column=1, sticky=tk.W, pady=4)
        tk.Button(self.master, bg = 'green', text='Decrypt', command=self.dec).grid(row=10, column=2, sticky=tk.W, pady=4)
        tk.Button(self.master, text='Quit', command=self.master.quit).grid(row=20, column=0, sticky=tk.W, pady=4)
        self.master.grid_columnconfigure(5, weight = 2)
        self.master.grid_columnconfigure(4, weight = 2)

        tk.mainloop()

    def new_password(self):
        passlen = self.passlene.get()
        if passlen == '':
            passlen = 16
        else:
            passlen = int(passlen)
        passexclude = self.passexe.get()
        password = generate_password(passlen, passexclude)
        self.passentry.delete(0, tk.END)
        self.passentry.insert(tk.END, password)

    def add_cred(self):
        section = self.secentry.get()
        username = self.userentry.get()
        password = self.passentry.get()
        fabspath = self.filepath.get()
        config = configparser.ConfigParser()
        config.read(fabspath)
        if not section in config.sections():
            config.add_section(section)
        config[section][username] = password
        with open(fabspath, 'w') as f:
            config.write(f)
        self._readfile(fabspath)
        self.secentry.delete(0, tk.END)
        self.userentry.delete(0, tk.END)
        self.passentry.delete(0, tk.END)

    def openembedfile(self):
        iself.filepath.delete(0, tk.END)
        ifabspath = fd.askopenfilename(
                filetypes = [
                    ('Accepted Formats', '.wav .jpg .jpeg .gif .png'),
                    ],
                title = 'Please choose Image/Audio File'
                )
        iself.filepath.insert(tk.END, ifabspath)

    def opendatafile(self):
        self.filepath.delete(0, tk.END)
        fabspath = fd.askopenfilename(title = 'Please choose Data File')
        self._readfile(fabspath)
        self.filepath.insert(tk.END, fabspath)

    def _readfile(self, fabspath):
        self.mylist.delete(0, tk.END)
        f = open(fabspath, 'rb')
        c = f.read()
        f.close()
        self.mylist.insert(tk.END, *c.splitlines())
        #filecontent.set(c)

    def enc(self):
        fabspath = self.filepath.get()
        key = self.keyentry.get()
        self.statuslabel.set('Encrypting File')
        encryptfile(key, fabspath, fabspath)
        self.statuslabel.set('Encrypted!')
        self._readfile(fabspath)
        #self.filepath.delete(0, tk.END)

    def dec(self):
        key = self.keyentry.get()
        fabspath = self.filepath.get()
        self.statuslabel.set('Decrypting File...')
        decryptfile(key, fabspath, fabspath)
        self.statuslabel.set('Decrypted!')
        self._readfile(fabspath)
        #self.filepath.delete(0, tk.END)

def main():
    gui = CredGui()
