from PIL import Image
import io
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
    f = open('testfile', 'r')
    data = f.read()
    ifilename = 'test.jpg'
    imgfile = Image.open('test.jpg', 'r')
    oimage = imgfile.copy()
    print('-'*60)
    print(f'embedding data into image file {ifilename}')
    print(f'Data : {data}')
    embed_data(oimage, data)
    print('-'*60)
    print('Extracting Data From Image')
    print('file name test_em.png')
    extracted = extract_data(oimage)
    oimage.save('test_em.png', 'PNG')
    emb_image = Image.open('test_em.png', 'r')
    extracted = extract_data(emb_image)
    print(f'Extracted {extracted}')
    print('-'*60)

if __name__ == '__main__' :
    main()

