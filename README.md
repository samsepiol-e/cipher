# Installation
It is pip installable. Run
```
pip install StegCipher-Tools
```

# stegtools
This tool performs encryption on any file and embed the data in an image file, or restore decrypted file from image file.
You can use this tool to hide your data in a plain sight. Even if attacker finds data embedded into image, they can't decrypt it unless they know the key.

## Steganography
For each byte of data, it is embedded into 9 bytes of image/audio file by changing the LSB (Least Significant Bit).
This operation is done by masking the first 7 bits of image/audio file by applying AND operation with 254 (11111110) and last bit is changed using OR operation.
9th byte is reserved for termination flag i.e. 0 to continue and 1 to stop the extraction process.
For image file, RGB values of 3 pixels is used to embed 1 byte of data, so maximum data size is NumPixels/9 bytes.
For audio file, 9 frame bytes are used. The maximum data size is calculated by sampling_rate*bits_per_sample/8*num_channels*duration(s)/9.
For instance, 5 minutes of wav file with 48kHz sampling rate, 16 bits stereo can embed 48,000*16/8*2*5*60/9 = approx 6.1MB of data.
## How to Use
run
For Linux/MacOS run
```
stegtools
```
or
```
python -m stegtools
```
if you are on Windows.
After the data is embedded, the original file will be deleted, so please make sure to backup your files when you are running it the first time.

# credtools
This is a tool to manage your credentials. You can automatically generate password, add/modify/retrieve your password.
## How to Use
run
For Linux/MacOS run
```
credtools
```
or
```
python -m credtools
```
if you are on Windows.

## Shortcut Keys
Action
```
<C-o> Open File
<C-g> Generate New Password
<C-a> Add Password to file
<C-r> Remove Selected
<C-l> Clear Current Entry
<C-c> Copy Password to Clipboard
<C-v> Paste Password from Clipboard
<C-q> Encrypt and Quit
```
Navigation
```
<C-k> Jump to Key Entry
<C-f> Jump to Search Entry
<C-s> Jump to Section Entry
<C-u> Jump to User Name Entry
```

## Password Strength
You can check strength of existing or generated password in password entry field by its color.
```
Sky Blue : Very Strong. Password contains all 3 alphabets, numeral, and numbers case sensitive.
Light Green : Strong. Password contains all 3 alphabets, numeral, and numbers case insensitive.
Yellow : Okay. Password contains 2 out of alphabets, numeral, and numbers case insensitive.
Orange : Weak. Password contains 1 out of alphabets, numeral, and numbers case insensitive.
Red : Very weak. Password is less than 6 letters long.
```


## Encryption
First, key is hashed using SHA256 to create a 256 bit key for AES256 encryption.
After encryption is done, that data is encoded with base64.


