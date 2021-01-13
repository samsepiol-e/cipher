from PIL import Image
import os
def genData(data):
    newd = []
    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd

def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)
    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] + imdata.__next__()[:3] + imdata.__next__()[:3]]
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1

            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1

        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def embed_data(output_img, data):
    w = output_img.size[0]
    (x, y) = (0, 0)
    for pixel in modPix(output_img.getdata(), data):
        output_img.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

def extract_data(imgfile):
    data = ''
    imgdata = iter(imgfile.getdata())
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] + imgdata.__next__()[:3] + imgdata.__next__()[:3]]
        binstr = ''
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

def main():
    wdir = input('Please enter your working directory : ')
    wdir = os.path.expanduser(wdir)
    imgname = input('Please enter your image file name : ')
    filename = input('Please enter your data file name : ')
    imgfile = Image.open(os.path.join(wdir, imgname), 'r')
    filepath = os.path.join(wdir, filename)
    print('-'*60)
    print('''
    1. Embed Data
    2. Extract Data
    ''')
    choice = input('Please choose from above option : ')
    print('-'*60)
    if choice == '1':
        f = open(filepath, 'r')
        data = f.read()
        f.close()
        oimage = imgfile.copy()
        embed_data(oimage, data)
        print(f'embedding data into image file {imgname}')
        print(f'Data : {data}')
        outname = imgname.split('.')[0]+'_1'+'.png'
        oimage.save(os.path.join(wdir, outname), 'PNG')
        print(f'data embedded into file {outname}')
    elif choice == '2':
        print(f'Extracting Data From {imgname}')
        extracted = extract_data(imgfile)
        print(f'Extracted {extracted}')
        f = open(filepath, 'w+')
        f.write(extracted)

if __name__ == '__main__' :
    main()

