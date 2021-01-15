# cipher tools
This tool performs encryption on any file and embed the data in an image file, or restore decrypted file from image file.
You can use this tool to hide your data in a plain sight. Even if attacker finds data embedded into image, they can't decrypt it unless they know the key.

##How to Use
Simply running
```
python ciphertools.py
```
is sufficient.
It then prompts you to choose a working directory.
After the data is embedded, the original file will be deleted.

##Encryption
First, key is hashed using SHA256 to create a 256 bit key for AES256 encryption.
After encryption is done, that data is encoded with base64.

##Steganography
Each byte of data is embedded into RGB values of 3 pixels.
That is pix = [R[0], G[0], B[0], R[1], G[1], B[1], R[2], G[2], B[2]]
Then XOR(byte[i], pix[i]%2) is performed to reduce RGB value by 1. (or if 0, then bumps 1)
This will guarantee that odd numbered RGB value is mapped to 1 and even numbered RGB value is mapped to 0 of original data.
The last element of RGB value (Blue value of RGB) is used to determine continuation/termination. Odd number represents termination thus will stop extraction process. For extraction, simply calculating modulo 2 will be sufficient.
