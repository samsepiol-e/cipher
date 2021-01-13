import random

def generate_password(passlen=16):
    p = ''
    for i in range(passlen):
        p += chr(random.randint(33, 123))
    return p

if __name__ == '__main__':
    password = generate_password()
    print(password)
