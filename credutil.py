from encryption import *
from passgen import *
import configparser
import os

def new_credential(fabspath, section, username, genpass = True, passlen=16, password = ''):
    config = configparser.ConfigParser()
    if not os.path.exists(fabspath):
        open(fabspath, 'a').close()
    config.read(fabspath)
    if not section in config.sections():
        config.add_section(section)
    if genpass:
        while True:
            password = generate_password(passlen)
            print(f'Password Generated for {username} : {password}')
            yn = input('Would you like to use this password? (Y/n) : ')
            if yn in ['', 'Y', 'y']:
                break
    config[section][username] = password
    with open(fabspath, 'w') as f:
        config.write(f)

def main():
    fdir = input('Please enter your working directory : ')
    filename = input('Please enter your filename : ')
    fabspath = os.path.join(os.path.expanduser(fdir), filename)
    key = input('Please enter your encryption key : ')
    while True:
        print('-'*60)
        print('''
        1. Encrypt File
        2. Decrypt File
        3. Add an account to file
        4. Exit
        ''')
        choice = input(' What Would you like to do? : ')
        print('-'*60)
        if choice == '1':
            encryptfile(key, fabspath, fabspath)
        elif choice == '2':
            decryptfile(key, fabspath, fabspath)
        elif choice == '4':
            break
        elif choice == '3':
            while True:
                print('*'*60)
                print('''
                1. Add existing account (user enters password)
                2. Create new account (generate random password)
                3. Exit
                ''')
                choice = input(': ')
                print('*'*60)
                if choice == '3':
                    break
                section = input('Please enter section to add : ')
                username = input('Please enter username : ')
                if choice == '1':
                    password = input('Please enter your password : ')
                    new_credential(fabspath, section, username, False, password=password)
                elif choice == '2':
                    passlen = input('Please enter your password length (Default is 16) : ')
                    if passlen == '':
                        passlen = 16
                    else:
                        passlen = int(passlen)
                    new_credential(fabspath, section, username, passlen = passlen)
                else:
                    print('Not a valid entry')
                    continue
        else:
            print('Not a valid entry')
            continue

if __name__ == '__main__':
    main()
