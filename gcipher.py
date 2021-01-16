from encryption import *
from stegano import *
from audiostegano import *
import os
import tkinter as tk
import tkinter.filedialog as fd 
import uuid

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
    filepath.insert(tk.END, fabspath)

def enc_and_embed():
    fabspath = filepath.get()
    key = keyentry.get()
    ifabspath = ifilepath.get()
    ifileinfo = os.path.basename(ifabspath).split('.')
    ofilename = ifileinfo[0]+'_'+str(uuid.uuid4())
    fabspath = filepath.get()
    statuslabel.set('Encrypting File')
    encryptfile(key, fabspath, fabspath)
    statuslabel.set('Embedding Encrypted File')
    if ifileinfo[1].lower() in ['jpg', 'jpeg', 'gif', 'png']:
        ofilename += '.png'
        embed_data_from_file(ifabspath, fabspath, ofilename)
    else:
        ofilename += '.wav'
        embed_file_to_wave(ifabspath, fabspath, ofilename)
    os.remove(fabspath)
    statuslabel.set('Embedding and Encrypted Done!')
    filepath.delete(0, tk.END)
    ifilepath.delete(0, tk.END)

def extract_and_decrypt():
    key = keyentry.get()
    ifabspath = ifilepath.get()
    ifileinfo = os.path.basename(ifabspath).split('.')
    f = fd.asksaveasfile('wb')
    statuslabel.set('Extracting Data...')
    if ifileinfo[1].lower() == 'wav':
        data = extract_data_from_wave(ifabspath)
    else:
        data = extract_data_from_image(ifabspath)
        
    statuslabel.set('Decrypting Data...')
    data = decrypt(key, data)
    f.write(data)
    f.close()
    os.remove(ifabspath)
    statuslabel.set('Extraction and Decryption Done!')
    ifilepath.delete(0, tk.END)


def show_entry_fields():
    print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))

master = tk.Tk()
master.title('C1ph3r T00lz')
statuslabel = tk.StringVar()
width = 400
height = 200
screen_width = master.winfo_screenwidth()
screen_height = master.winfo_screenheight()
x = (screen_width//2) - (width//2)
y = (screen_height//2) - (height//2)
master.geometry(f'{width}x{height}+{x}+{y}')
tk.Label(master, text="Image/Audio File").grid(row=0)
tk.Label(master, text="Data File").grid(row=1)
tk.Label(master, text="Encryption Key").grid(row=2)
tk.Label(master, textvariable=statuslabel).grid(row=3, column = 1, sticky=tk.W)

ifilepath = tk.Entry(master)
filepath = tk.Entry(master)
keyentry = tk.Entry(master)

ifilepath.grid(row=0, column=1)
filepath.grid(row=1, column=1)
keyentry.grid(row=2, column=1)

tk.Button(master, text = 'Browse', command = openembedfile).grid(row=0, column =2)
tk.Button(master, text = 'Browse', command = opendatafile).grid(row=1, column =2)
tk.Button(master, bg = 'red', text='Encrypt and Embed', command=enc_and_embed).grid(row=5, column=0, sticky=tk.W, pady=4)
tk.Button(master, bg = 'green', text='Extract and Decrypt', command=extract_and_decrypt).grid(row=5, column=1, sticky=tk.W, pady=4)
tk.Button(master, text='Quit', command=master.quit).grid(row=5, column=2, sticky=tk.W, pady=4)

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