# Python program implementing Image Steganography

# PIL module is used to extract pixels of image and modify its
from tkinter import *
from tkinter import messagebox as mb
import PIL.Image
from PIL import ImageTk, Image

root = Tk()
root.title("Steganography")
root.geometry("450x350")
root.resizable(False,False)
root.configure(bg="#EEEEDF")

logo = PhotoImage(file = "icon.png")
root.iconphoto(False, logo)

image = Image.open("header.jpg")
resize_img = image.resize((445, 125))
img = ImageTk.PhotoImage(resize_img)
label = Label(root, image=img).place(x=0, y=0)

Label(root, text="The Science Of Hiding Information!", bg ="#EEEEDF" ,fg="black", font=("Lucida Handwriting",14), wraplength =500).place(x=30, y=145)

# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):

        # list of binary codes
        # of given data
        newd = []

        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd

# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):

    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):

        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
                                imdata.__next__()[:3] +
                                imdata.__next__()[:3]]

        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1
            
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                pix[j] -= 1

        # Eighth pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means thec
        # message is over.
        if (lendata-1) == i:
            if (pix[-1] % 2 == 0):
                pix[j] -= 1

        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    w = newimg.size[0] #.size – Is used to count the number of pixels along with the image.
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):

        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

# Encode data into image
def main_encode(img, data, new_img_name):
    image = PIL.Image.open(img, 'r')
    if (len(data) == 0) or (len(img) == 0) or (len(new_img_name) == 0):
        mb.showerror("Error", 'You have not put a value! Please put all values before pressing the button')
    new_img = image.copy()
    encode_enc(new_img, data)
    new_img_name += '.png'
    new_img.save(new_img_name, 'png')

# Decode the data in the image
def main_decode(img):
    image = PIL.Image.open(img, 'r')

    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]

        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        
        if (pixels[-1] % 2 != 0):
            return text_entry_msg.insert(END, data)
           

def encode_window():
    encode_wn = Toplevel(root)
    encode_wn.title("Encode an Image")
    encode_wn.geometry('600x220')
    encode_wn.resizable(0, 0)
    encode_wn.config(bg='#CDCDC8')

    Label(encode_wn, text='Hide data in Image', font=("Bookman Old Style", 15), bg='#CDCDC8').place(x=220, rely=0)
    Label(encode_wn, text='Enter the path or name of the image(with extension):', font=("Bell MT", 13),
          bg='#CDCDC8').place(x=2, y=50)
    Label(encode_wn, text='Enter the data to be encoded:', font=("Bell MT", 13), bg='#CDCDC8').place(
        x=2, y=90)
    Label(encode_wn, text='Enter the output file name (without extension):', font=("Bell MT", 13),
          bg='#CDCDC8').place(x=2, y=130)

    img_path = Entry(encode_wn, width=35)
    img_path.place(x=372, y=53)
    
    global text_to_be_encoded
    text_to_be_encoded = Entry(encode_wn, width=40)
    text_to_be_encoded.place(x=212, y=94)

    after_save_path = Entry(encode_wn, width=30)
    after_save_path.place(x=338, y=133)
   
    Button(encode_wn, text='Encode the Image', font=('Bookman Old Style', 12), bg='#EEEED5', command=lambda: main_encode(img_path.get(), text_to_be_encoded.get(), after_save_path.get())).place(x=220, y=170)

def decode_window():
    decode_wn = Toplevel(root)
    decode_wn.title("Decode an Image")
    decode_wn.geometry('600x300')
    decode_wn.resizable(0, 0)
    decode_wn.config(bg='#CDCDC8')
    Label(decode_wn, text='Unhide data from Image', font=("Bell MT", 15), bg='#CDCDC8').place(x=200, rely=0)
    Label(decode_wn, text='Enter the path to the image (with extension):', font=("Bell MT", 13),
          bg='#CDCDC8').place(x=2, y=50)

    img_entry = Entry(decode_wn, width=40)
    img_entry.place(x=320, y=55)

    Button(decode_wn, text='Decode the Image', font=('Bookman Old Style', 12), bg='#EEEED5', command=lambda:
    main_decode(img_entry.get())).place(x=220, y=90)

    Label(decode_wn, text='Text that has been encoded in the image', font=("Times New Roman", 14), bg='#CDCDC8').place(
        x=150, y=140)

    global text_entry_msg
    text_entry_msg = Entry(decode_wn, width=80)
    text_entry_msg.place(x=55, y=170, heigh =90)

# Main Function
def main():
    a = int(input("Enter answer: "))
    if (a == 1):
        encode_window()
    elif (a == 2):
        print("Decoded Word:  " + decode_window())
    else:
        raise Exception("Enter correct input")

Button(root, text="Encode", width=15, height=1, font="Georgia 14 bold",bg="#EEEED5" , command=encode_window).place(x=120, y=200)
Button(root, text="Decode", width=15, height=1, font="Georgia 14 bold", bg="#EEEED5", command=decode_window).place(x=120, y=250)

if __name__ == '__main__' :
    root.mainloop()