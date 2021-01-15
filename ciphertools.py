from encryption import *
from stegano import *
from audiostegano import *
import configparser
import os

def main():
    fdir = input('Please enter your working directory : ')
    fdir = os.path.expanduser(fdir)
    for f in os.listdir(fdir):
        print(f)
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
        key = input('Please enter your encryption key : ')
        print('-'*60)
        for f in os.listdir(fdir):
            print(f)
        print('-'*60)
        filename = input('Please enter your data file : ')
        fabspath = os.path.join(fdir, filename)
        print('''
        1. Image File
        2. Audio File
        ''')
        fformat = input('Please select your file format : ')
        if fformat == '1':
            ifilename = input('Please enter your image filename : ')
            ifabspath = os.path.join(fdir, ifilename)
            imgfile = Image.open(ifabspath, 'r')
            ofilename = ifilename.split('.')[0]+'_1.png'
        elif fformat == '2':
            afilename = input('Please enter your audio filename : ')
            afabspath = os.path.join(fdir, afilename)

        print('-'*60)
        if choice == '1':
            encryptfile(key, fabspath, fabspath)
            if fformat == '1':
                embed_data_from_file(ifabspath, fabspath, ofilename)
            elif fformat == '2':
                embed_file_to_wave(afabspath, fabspath)
            os.remove(fabspath)
        elif choice == '2':
            if fformat == '1':
                extract_data_from_file(ifabspath, filename)
            elif fformat == '2':
                extract_file_from_wave(afabspath, filename)
            decryptfile(key, fabspath, fabspath)

if __name__ == '__main__':
    main()
