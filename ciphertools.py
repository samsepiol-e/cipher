from encryption import *
from stegano import *
from audiostegano import *
import configparser
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import uuid

def choosefile(prompt):
    print(prompt)
    root = Tk()
    root.withdraw()
    filepath = askopenfilename()
    root.destroy()
    return filepath


def main():
    while True:
        print('-'*60)
        print('''
        1. Encrypt File and Embed Data
        2. Extract Data and Decrypt
        3. Exit
        ''')
        choice = input(' What Would you like to do? : ')
        if choice == '3':
            break
        print('-'*60)
        print('-'*60)
#        print('Please choose Image/Audio File')
#        ifabspath = askopenfilename()
        
        Tk().withdraw()
        ifabspath = askopenfilename(
                filetypes = [
                    ('Accepted Formats', '.wav .jpg, .jpeg .gif .png'),
                    ],
                title = 'Please choose Image/Audio File',
                )
        ifilename = os.path.basename(ifabspath)
        ifiledir = os.path.dirname(ifabspath)
        ifileinfo = ifilename.split('.')
        randsuffix = str(uuid.uuid4())
        #Tk().destroy()
        if ifileinfo[1].lower() in ['jpg', 'jpeg', 'gif', 'png']:
            fileext = '.png'
            fformat = 'i'
        elif ifileinfo[1].lower() not in ['wav']:
            print('Invalid file chosen')
            continue
        else:
            fileext = '.wav'
            fformat = 'a'

        ofilename = ifileinfo[0]+'_'+randsuffix+fileext
            
        key = input('Please enter your encryption key : ')
        
        print('-'*60)
        if choice == '1':
            #print('Please choose Data File')
            #fabspath = askopenfilename()
            Tk().withdraw()
            fabspath=askopenfilename(title='Please choose Data File')
            Tk().destroy()
            encryptfile(key, fabspath, fabspath)
            if fformat == 'i':
                embed_data_from_file(ifabspath, fabspath, ofilename)
            elif fformat == 'a':
                embed_file_to_wave(ifabspath, fabspath, ofilename)
            os.remove(fabspath)

        elif choice == '2':
            while True:
                filename = input('Please enter filename for your extracted file : ')
                fabspath = os.path.join(ifiledir, filename)
                if os.path.isfile(fabspath):
                    rmfile = input('File Already Exists, Would you like to override it? (Y/n) : ')
                    if rmfile in ['', 'Y', 'y']:
                        os.remove(fabspath)
                        break
                    else:
                        print('Please choose a different file name')
                        continue
                else:
                    break

            if fformat == 'i':
                extract_data_from_file(ifabspath, filename)
            elif fformat == 'a':
                extract_file_from_wave(ifabspath, filename)
            decryptfile(key, fabspath, fabspath)
            os.remove(ifabspath)

if __name__ == '__main__':
    main()
