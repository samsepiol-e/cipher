from encryption import *
from stegano import *
import configparser
import os

def main():
    fdir = input('Please enter your working directory : ')
    fdir = os.path.expanduser(fdir)
    while True:
        print('-'*60)
        print('''
        1. Encrypt File and Embed in Image
        2. Extract File from Image and Decrypt
        3. Exit
        ''')
        choice = input(' What Would you like to do? : ')
        if choice == '3':
            break
        key = input('Please enter your encryption key : ')
        filename = input('Please enter your filename : ')
        ifilename = input('Please enter your image filename : ')
        fabspath = os.path.join(fdir, filename)
        ifabspath = os.path.join(fdir, ifilename)
        imgfile = Image.open(ifabspath, 'r')
        ofilename = ifilename.split('.')[0]+'.png'

        print('-'*60)
        if choice == '1':
            encryptfile(key, fabspath, fabspath)
            embed_data_from_file(ifabspath, fabspath, ofilename)
            os.remove(fabspath)
        elif choice == '2':
            extract_data_from_file(ifabspath, filename)
            decryptfile(key, fabspath, fabspath)

if __name__ == '__main__':
    main()
