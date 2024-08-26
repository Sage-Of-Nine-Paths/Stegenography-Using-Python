from PIL import Image
import binascii as t
import optparse

def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def hex2rgb(hexcode):
    hexcode = hexcode.lstrip('#')
    return tuple(int(hexcode[i:i+2], 16) for i in (0, 2, 4))

def str2bin(message):
    binary = bin(int(t.hexlify(message.encode()), 16))
    return binary[2:]

def bin2str(binary):
    message = t.unhexlify('%x' % (int(binary, 2)))
    return message.decode()

def encode(hexcode, digit):
    if hexcode[-1] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
        hexcode = hexcode[:-1] + digit
        return hexcode
    else:
        return None

def decode(hexcode):
    if hexcode[-1] in ('0', '1'):
        return hexcode[-1]
    else:
        return None

def hide(filename, message):
    img = Image.open(filename)
    binary = str2bin(message) + '1111111111111110'
    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()
        newdata = []
        digit = 0
        temp = ''
        for item in datas:
            if digit < len(binary):
                newpix = encode(rgb2hex(item[0], item[1], item[2]), binary[digit])
                if newpix is None:
                    newdata.append(item)
                else:
                    r, g, b = hex2rgb(newpix)
                    newdata.append((r, g, b, 255))
                    digit += 1
            else:
                newdata.append(item)
        img.putdata(newdata)
        img.save(filename, "PNG")
        return "Completed!"
    return "Couldn't hide :("

def retr(filename):
    img = Image.open(filename)
    binary = ''
    if img.mode in ('RGBA'):
        img = img.convert('RGBA')
        datas = img.getdata()
        
        for item in datas:
            digit = decode(rgb2hex(item[0], item[1], item[2]))
            if digit is None:
                pass
            else:
                binary = binary + digit
                if binary[-16:] == '1111111111111110':
                    print("Success!")
                    return bin2str(binary[:-16])
        return bin2str(binary)
    return "Couldn't retrieve it :("

def Main():
    parser = optparse.OptionParser('usage %prog ' + '-e/-d <target file>')
    parser.add_option('-e', dest='hide', type='string', help='target pic to hide text path')
    parser.add_option('-d', dest='retr', type='string', help='target pic to retrieve text path')
    (options, args) = parser.parse_args()

    if options.hide is not None:
        text = input("Enter your message to hide: ")
        print(hide(options.hide, text))
    elif options.retr is not None:
        print(retr(options.retr))
    else:
        print(parser.usage)
        exit(0)

if __name__ == '__main__':
    Main()
