from stegano import dataToBin
import os
import wave

def format_bytes(size):
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return round(size, 2), power_labels[n]+'B'

def framebytes_from_wave(filename):
    music = wave.open(filename, mode='rb')
    frame_bytes = bytearray(list(music.readframes(music.getnframes())))
    print(f'Number of Frames : {len(frame_bytes)}')
    fsize, label = format_bytes(len(frame_bytes)//9)
    print(f'Maximum Data Size To Embed : {fsize} {label}')
    musicparams = music.getparams()
    music.close()
    return musicparams, frame_bytes

def embed_data_to_frame(frame_bytes, data):
    datalen = len(data)
    size, label = format_bytes(datalen)
    print(f'Embedding Data of size {size} {label}')
    modified_frames = modFrame(frame_bytes, data)
    return modified_frames + frame_bytes[len(modified_frames):]

def framebytes_to_file(filename, musicparams, frame_bytes):
    with wave.open(filename, 'wb') as fd:
        fd.setparams(musicparams)
        fd.writeframes(frame_bytes)

def embed_file_to_wave(wavefilepath, filepath):
    wdir = os.path.dirname(wavefilepath)
    basename = os.path.basename(wavefilepath)
    ofilename = basename.split('.')[0]+'_embedded.wav'
    params, framebytes = framebytes_from_wave(wavefilepath)
    f = open(filepath, 'rb')
    data = f.read()
    f.close()
    modified_frames = embed_data_to_frame(framebytes, data)
    framebytes_to_file(os.path.join(wdir, ofilename), params, modified_frames)

def extract_file_from_wave(wavefilepath, ofilename):
    wdir = os.path.dirname(wavefilepath)
    params, framebytes = framebytes_from_wave(wavefilepath)
    data = extractDataFromFrame(framebytes)
    f = open(os.path.join(wdir, ofilename), 'wb+')
    f.write(data)
    f.close()



def modFrame(frame_bytes, data):
    datalist = dataToBin(data)
    lendata = len(datalist)
    frames = iter(frame_bytes)
    lenframebytes = len(frame_bytes)
    modframes = []
    for i in range(lendata):
        for j in range(0, 9):
            if j != 8:
                frame = (frames.__next__() & 254) | int(datalist[i][j])
                modframes.append(frame)
            else:
                frame = frames.__next__()
                if (i == lendata - 1):
                    frame = frame & 254 | 1

                else:
                    frame = frame & 254
                modframes.append(frame)
    return bytearray(modframes)

def extractDataFromFrame(frame_bytes):
    frames = iter(frame_bytes)
    data = b''
    while True:
        last_bits = [frames.__next__() & 1 for i in range(9)]
        binstr = ''
        for i in range(0, 8):
            binval = str(last_bits[i])
            binstr+=binval

        data += bytes([int(binstr, 2)])
        if last_bits[-1] == 1:
            return data


