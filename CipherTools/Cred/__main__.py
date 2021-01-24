from CipherLib.encryption import *
from CipherLib.passgen import *
import configparser
import tkinter as tk
import tkinter.filedialog as fd
import os
import pyperclip
import re
import io


class CredGui():
    def __init__(self):
        self.master = tk.Tk()
        self.master.title('3ncryp710n T00lz')
        self.statuslabel = tk.StringVar()
        self.width = 600
        self.height = 530
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width//2) - (self.width//2)
        y = (screen_height//2) - (self.height//2)
        self.master.geometry(f'{self.width}x{self.height}+{x}+{y}')
        tk.Label(self.master, text="Data File").grid(row=0)
        tk.Label(self.master, text="Decryption Key").grid(row=1)
        self.filepath = tk.Entry(self.master)
        self.keyentry = tk.Entry(self.master)
        self.filepath.grid(row=0, column=1, sticky=tk.W)
        self.keyentry.grid(row=1, column=1, sticky=tk.W)

        tk.Button(self.master, text = 'Browse', command = self.opendatafile, bd = 7).grid(row=0, column =2, sticky=tk.W)
        self.status = tk.Label(self.master, textvariable=self.statuslabel)
        self.status.grid(row=2, column = 1, sticky=tk.W)
        tk.Label(self.master, text='Search').grid(row=3)
        self.searchvar = tk.StringVar()
        self.searchentry = tk.Entry(self.master, width = 40, textvariable=self.searchvar)
        self.searchentry.grid(row=3, column = 1, sticky=tk.W, columnspan = 2)
        self.searchvar.trace('w', self.search)
        self.myscroll = tk.Scrollbar(self.master)
        self.myscroll.grid(row=4, column = 2, sticky='nw')
        self.mylist = tk.Listbox(self.master, yscrollcommand = self.myscroll.set, width = 50)
        self.mylist.grid(row=4, column = 1, columnspan=3, sticky=tk.W)
        self.myscroll.config( command = self.mylist.yview )

        tk.Button(self.master, text='Encrypt', command=self.enc).grid(row=10, column=1, sticky=tk.W, pady=4)
        tk.Button(self.master, text='Decrypt', command=self.dec).grid(row=10, column=2, sticky=tk.W, pady=4)

        self.master.grid_columnconfigure(5, weight = 2)
        self.master.grid_columnconfigure(4, weight = 2)

        tk.Label(self.master, text="Credential").grid(row=15)
        tk.Label(self.master, text="Section").grid(row=16, column = 1, sticky=tk.W)
        tk.Label(self.master, text="Username").grid(row=16, column = 2, sticky=tk.W)
        self.secentry = tk.Entry(self.master)
        self.userentry = tk.Entry(self.master)
        self.secentry.grid(row=17, column = 1, sticky=tk.W)
        self.userentry.grid(row=17, column = 2, sticky=tk.W)
        tk.Button(self.master, text = 'Copy Password', command = self.copy_passwd).grid(row=17, column =3, sticky=tk.W)


        tk.Label(self.master, text="Password").grid(row=18)#, column = 0, sticky=tk.W)
        self.passvar = tk.StringVar()
        self.passentry = tk.Entry(self.master, width = 40, textvariable=self.passvar)
        self.passentry.grid(row=18, column = 1, sticky=tk.W, columnspan = 2)
        self.passvar.trace('w', self.check_passwd_strength)

        tk.Label(self.master, text="Password Length").grid(row=19, column = 1)
        tk.Label(self.master, text="Password Exclude").grid(row=19, column = 2)
        self.passlene = tk.Entry(self.master)
        self.passexe = tk.Entry(self.master)
        self.passlene.grid(row = 20, column = 1, sticky=tk.W)
        self.passexe.grid(row = 20, column = 2, sticky=tk.W)
        self.passlene.insert(tk.END, '32')
        self.passexe.insert(tk.END, r'%\()|{}[]:";' + "'" + '<>,./?')
        tk.Button(self.master, text = 'Generate Password', command = self.new_password).grid(row=21, column =1, sticky=tk.W, pady = 4)
        tk.Button(self.master, text = 'Add Password', command = self.add_cred).grid(row=21, column =2, sticky=tk.W, pady = 4)

        tk.Button(self.master, text='Encrypt and Quit', command=self.encrypt_and_quit).grid(row=22, column=3, sticky=tk.W, pady=4)

        self.master.bind('<Control-o>', lambda event: self.opendatafile())
        self.master.bind('<Control-e>', lambda event: self.enc())
        self.master.bind('<Control-d>', lambda event: self.dec())
        self.keyentry.bind('<Return>', lambda event: self.dec())
        self.master.bind('<Control-c>', lambda event: self.copy_passwd())
        self.master.bind('<Control-v>', lambda event: self.paste_passwd())
        self.master.bind('<Control-g>', lambda event: self.new_password())
        self.master.bind('<Control-a>', lambda event: self.add_cred())
        self.master.bind('<Control-q>', lambda event: self.encrypt_and_quit())
        self.master.bind('<Control-l>', lambda event: self.clear())
        self.master.bind('<Control-r>', lambda event: self.del_cred())
        self.master.bind('<Control-f>', lambda event: self.searchentry.focus_set())
        self.master.bind('<Control-s>', lambda event: self.secentry.focus_set())
        self.master.bind('<Control-u>', lambda event: self.userentry.focus_set())
        self.master.bind('<Control-k>', lambda event: self.keyentry.focus_set())
        #self.searchentry.bind('<Key>', self.search)
        #self.searchentry.bind('<FocusIn>', self.search)
        self.master.bind('<<ListboxSelect>>', self.lbselect)
        self.mylist.bind('<Up>', self.lbselect)
        self.mylist.bind('<Down>', self.lbselect)

        tk.mainloop()
    
    def encrypt_and_quit(self):
        self.enc()
        self.master.quit()


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

    def check_passwd_strength(self, *args):
        password = self.passentry.get()
        if isinstance(password, bytes):
            password = password.decode('utf-8')
        if password == '':
            self.passentry.config(bg = 'white')
        else:
            passstr = get_pass_strength(password)
            if passstr == 3:
                self.passentry.config(bg = 'deep sky blue')
            elif passstr == 2:
                self.passentry.config(bg = 'pale green')
            elif passstr == 1:
                self.passentry.config(bg = 'yellow')
            elif passstr == 0:
                self.passentry.config(bg = 'orange')
            else:
                self.passentry.config(bg = 'red')

    def add_cred(self):
        section = self.secentry.get()
        username = self.userentry.get()
        password = self.passentry.get()
        fabspath = self.filepath.get()
        config = configparser.ConfigParser()
        config.read(fabspath)
        if not section in config.sections():
            config.add_section(section)
        if username == '':
            self.statuslabel.set('Username empty, please fillin.')
            self.status.config(bg = 'red')
        else:
            config[section][username] = password
            with open(fabspath, 'w') as f:
                config.write(f)
            self.statuslabel.set('Credential added')
            self.status.config(bg = 'green')
            self._readfile(fabspath)
            self.userentry.delete(0, tk.END)
            self.passentry.delete(0, tk.END)
            self.search(None)

    def lbselect(self, event):
        def _bytes_to_str(b):
            if isinstance(b, bytes):
                b = b.decode('utf-8')
            return b

        idx_t = self.mylist.curselection()
        if len(idx_t)>0:
            idx = idx_t[0]
            kv = self.mylist.get(idx_t)
            kv = _bytes_to_str(kv)
            self.secentry.delete(0, tk.END)
            self.userentry.delete(0, tk.END)
            self.passentry.delete(0, tk.END)
            if kv != '':
                if kv[0] == '[':
                    self.secentry.insert(tk.END, kv[1:-1])
                else:
                    kv_l = kv.split('=', 1)
                    key = kv_l[0].replace(' ', '')
                    val = kv_l[1].replace(' ', '')
                    while True:
                        idx -= 1
                        s = self.mylist.get((idx,))
                        s = _bytes_to_str(s)
                        if s[0] == '[':
                            self.secentry.insert(tk.END, s[1:-1])
                            self.userentry.insert(tk.END, key)
                            self.passentry.insert(tk.END, val)
                            break

    def del_cred(self):
        section = self.secentry.get()
        username = self.userentry.get()
        fabspath = self.filepath.get()
        config = configparser.ConfigParser()
        config.read(fabspath)
        if not section in config.sections():
            self.statuslabel.set('No Credential Found')
            self.status.config(bg = 'red')
        else:
            if username == '':
                config.remove_section(section)
            else:
                config.remove_option(section, username)
        with open(fabspath, 'w') as f:
            config.write(f)
        self.statuslabel.set('Credential Removed')
        self.status.config(bg = 'green')
        self._readfile(fabspath)
        self.secentry.delete(0, tk.END)
        self.userentry.delete(0, tk.END)
        self.passentry.delete(0, tk.END)
        self.search(None)

    def clear(self):
        focus = self.master.focus_get()
        if isinstance(focus, tk.Entry):
            focus.delete(0, tk.END)

    def search(self, *args):
        config = configparser.ConfigParser()
        fabspath = self.filepath.get()
        try:
            config.read(fabspath)
        except:
            self.statuslabel.set('File not in searchable format.')
            self.status.config(bg='red')
        else:
            self.mylist.delete(0, tk.END)
            buf = io.StringIO()
            searchkey = self.searchentry.get()
            p = re.compile(searchkey)
            #if searchkey == '':
            #    self.config = configparser.ConfigParser()
            #    fabspath = self.filepath.get()
            #    self.config.read(fabspath)
            #    self.config.write(buf)
            searchres = configparser.ConfigParser()
            for section in config.sections():
                res = p.search(section)
                if res is not None:
                    if not section in searchres.sections():
                        searchres.add_section(section)
                    for k, v in config.items(section):
                        searchres[section][k] = v
                else:
                    for k, v in config.items(section):
                        res = p.search(k)
                        if res is not None:
                            if not section in searchres.sections():
                                searchres.add_section(section)
                            searchres[section][k]=v
            searchres.write(buf)
            c = buf.getvalue()
            self.mylist.insert(tk.END, *c.splitlines())
            buf.close()


    def paste_passwd(self):
        passwd = pyperclip.paste()
        self.passentry.delete(0, tk.END)
        self.passentry.insert(tk.END, passwd)
        self.status.config(bg='green')
        self.statuslabel.set('Password Pasted From Clipboard')

    def copy_passwd(self):
        password = self.passentry.get()
        pyperclip.copy(password)
        self.status.config(bg='green')
        self.statuslabel.set('Password Copied to Clipboard')
        #section = self.secentry.get()
        #username = self.userentry.get()
        #fabspath = self.filepath.get()
        #config = configparser.ConfigParser()
        #config.read(fabspath)
        #if not section in config.sections():
        #    self.statuslabel.set('Section Not Found')
        #    self.label.config(bg='red')
        #else:
        #    if not config.has_option(section, username):
        #        self.statuslabel.set('Username Not Found')
        #        self.label.config(bg='red')
        #    else:
        #        password = config[section][username]
        #        pyperclip.copy(password)
        #        self.statuslabel.set('Password Copied to Clipboard')
        #        self.status.config(bg = 'green')
        #        self._readfile(fabspath)
        #        self.passentry.delete(0, tk.END)
        #        self.passentry.insert(tk.END, password)

        

    def opendatafile(self):
        self.filepath.delete(0, tk.END)
        fabspath = fd.askopenfilename(title = 'Please choose Data File')
        self._readfile(fabspath)
        self.filepath.insert(tk.END, fabspath)
        self.keyentry.focus_set()

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
        self.status.config(bg = 'red')
        encryptfile(key, fabspath, fabspath)
        self.statuslabel.set('Encrypted!')
        self.status.config(bg = 'green')
        self._readfile(fabspath)
        #self.filepath.delete(0, tk.END)

    def dec(self):
        key = self.keyentry.get()
        fabspath = self.filepath.get()
        self.statuslabel.set('Decrypting File...')
        self.status.config(bg = 'red')
        try:
            decryptfile(key, fabspath, fabspath)
            self.statuslabel.set('Decrypted!')
            self.status.config(bg = 'green')
            self._readfile(fabspath)
        except:
            self.statuslabel.set('Wrong Key!')
            self.status.config(bg = 'Red')

        #self.statuslabel.set('Decrypted!')
        #self.status.config(bg = 'green')
        #self._readfile(fabspath)
        #self.filepath.delete(0, tk.END)

def main():
    gui = CredGui()

if __name__ == '__main__':
    main()
