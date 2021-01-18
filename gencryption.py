from encryption import *
import os
from passgen import *
import configparser
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd 

def new_password():
    password = generate_password(16)
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
    f = open(fabspath, 'rb')
    c = f.read()
    f.close()
    filecontent.set(c)

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
filecontent = tk.StringVar()
width = 900
height = 500
screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()
x = (screen_width//2) - (width//2)
y = (screen_height//2) - (height//2)
master.geometry(f'{width}x{height}+{x}+{y}')
tk.Label(master, text="Data File").grid(row=0)
tk.Label(master, text="Encryption Key").grid(row=1)
tk.Label(master, textvariable=statuslabel).grid(row=2, column = 1, sticky=tk.W)
tk.Label(master, textvariable=filecontent, height = 10, wraplength = 300, justify = 'left').grid(row=2, column = 1)
#mycanvas = tk.Canvas(master)
#myframe = tk.Frame(mycanvas)
#myscroll = tk.Scrollbar(myframe, orient='vertical', command=mycanvas.yview)
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
tk.Label(master, text="Section").grid(row=14, column = 1)
tk.Label(master, text="Username").grid(row=14, column = 2)
tk.Label(master, text="Password").grid(row=14, column = 3)
filepath = tk.Entry(master)
keyentry = tk.Entry(master)
secentry = tk.Entry(master)
userentry = tk.Entry(master)
passentry = tk.Entry(master)

filepath.grid(row=0, column=1)
keyentry.grid(row=1, column=1)
secentry.grid(row=15, column = 1)
userentry.grid(row=15, column = 2)
passentry.grid(row=15, column = 3)

tk.Button(master, text = 'Generate Password', command = new_password).grid(row=16, column =0)
tk.Button(master, text = 'Add Password', command = add_cred).grid(row=16, column =1)

tk.Button(master, text = 'Browse', command = opendatafile).grid(row=0, column =2)
tk.Button(master, bg = 'red', text='Encrypt', command=enc).grid(row=10, column=1, sticky=tk.W, pady=4)
tk.Button(master, bg = 'green', text='Decrypt', command=dec).grid(row=10, column=2, sticky=tk.W, pady=4)
tk.Button(master, text='Quit', command=master.quit).grid(row=17, column=0, sticky=tk.W, pady=4)

tk.mainloop()

#def main():
#    while True:
#        print('-'*60)
#        print('''
#        1. Encrypt File and Embed Data
#        2. Extract Data and Decrypt
#        3. Exit
#        ''')
#        choice = input(' What Would you like to do? : ')
#        if choice == '3':
#            break
#        print('-'*60)
##        print('Please choose Image/Audio File')
##        ifabspath = askopenfilename()
#        
#        Tk().withdraw()
#        ifabspath = askopenfilename(
#                filetypes = [
#                    ('Accepted Formats', '.wav .jpg, .jpeg .gif .png'),
#                    ],
#                title = 'Please choose Image/Audio File',
#                )
#        ifilename = os.path.basename(ifabspath)
#        ifiledir = os.path.dirname(ifabspath)
#        ifileinfo = ifilename.split('.')
#        randsuffix = str(uuid.uuid4())
#        Tk().destroy()
#        if ifileinfo[1].lower() in ['jpg', 'jpeg', 'gif', 'png']:
#            fileext = '.png'
#            fformat = 'i'
#        elif ifileinfo[1].lower() not in ['wav']:
#            print('Invalid file chosen')
#            continue
#        else:
#            fileext = '.wav'
#            fformat = 'a'
#
#        ofilename = ifileinfo[0]+'_'+randsuffix+fileext
#            
#        key = input('Please enter your encryption key : ')
#        
#        print('-'*60)
#        if choice == '1':
#            #print('Please choose Data File')
#            #fabspath = askopenfilename()
#            Tk().withdraw()
#            fabspath=askopenfilename(title='Please choose Data File')
#            Tk().destroy()
#            encryptfile(key, fabspath, fabspath)
#            if fformat == 'i':
#                embed_data_from_file(ifabspath, fabspath, ofilename)
#            elif fformat == 'a':
#                embed_file_to_wave(ifabspath, fabspath, ofilename)
#            os.remove(fabspath)
#
#        elif choice == '2':
#            while True:
#                filename = input('Please enter filename for your extracted file : ')
#                fabspath = os.path.join(ifiledir, filename)
#                if os.path.isfile(fabspath):
#                    rmfile = input('File Already Exists, Would you like to override it? (Y/n) : ')
#                    if rmfile in ['', 'Y', 'y']:
#                        os.remove(fabspath)
#                        break
#                    else:
#                        print('Please choose a different file name')
#                        continue
#                else:
#                    break
#
#            if fformat == 'i':
#                extract_data_from_file(ifabspath, filename)
#            elif fformat == 'a':
#                extract_file_from_wave(ifabspath, filename)
#            decryptfile(key, fabspath, fabspath)
#            os.remove(ifabspath)
#
#if __name__ == '__main__':
#    main()
