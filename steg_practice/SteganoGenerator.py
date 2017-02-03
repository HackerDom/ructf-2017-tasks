import os

import qrcode
from PIL import Image, ImageDraw, ImageFont


class ImageWriterException(Exception):
    def __init__(self):
        pass


class NotInitialezed(ImageWriterException):
    def __init__(self):
        pass


class AlredyInitialezed(ImageWriterException):
    def __init__(self):
        pass


class BitesOrderError(ImageWriterException):
    def __init__(self):
        pass


class ImageDataWriter:
    def __init__(self):
        self.working_image = None
        self.data_to_write = None
        self.pixels_map = None
        self.initialized = False
        pass

    def init_image_by_data(self, data, bites_amount=3, is_bin=False):
        if self.initialized:
            raise AlredyInitialezed()
        size = 0
        if is_bin:
            size = (len(data) + bites_amount - 1) // bites_amount
        else:
            size = (len(data) * 8 + bites_amount - 1) // bites_amount  # data to binary in 3 chanels
        size_x = int(size ** 0.5 + 1)
        size_y = size_x
        self.working_image = Image.new('RGB', (size_x, size_y), "black")
        self.pixels_map = self.working_image.load()
        self.initialized = True

    def data_byte_stream(self, data, bites_amount=3):
        counter = 0
        bit_stream = ''
        for byte in data:
            for bit in bin(byte)[2:]:
                if counter < bites_amount:
                    bit_stream += bit
                    counter += 1
                else:
                    counter = 0
                    yield bit_stream
                    bit_stream = ''
        if counter != 0:
            bit_stream += "0" * (bites_amount - counter)
            yield bit_stream

    def data_bin_stream(self, data, bites_amount=3):
        data += "0" * (len(data) % bites_amount)
        for i in range(0, len(data) - bites_amount, bites_amount):
            yield data[i: i + bites_amount]

    def data_stream(self, data, bites_amount=3, is_bin=False):
        if is_bin:
            for x in self.data_bin_stream(data, bites_amount):
                yield x
        else:
            for x in self.data_byte_stream(data, bites_amount):
                yield x

    def pixel_stream(self):
        if not self.initialized:
            raise NotInitialezed()
        x_bound = self.working_image.size[0]
        y_bound = self.working_image.size[1]
        for x in range(x_bound):
            for y in range(y_bound):
                yield self.pixels_map[x, y], x, y

    def mask_apply(self, bites, bites_amount, bit_mask):
        if len(bites) != bites_amount or sum(int(b) for b in bit_mask) != bites_amount:
            raise BitesOrderError()
        temp_data = ''
        bites_index = 0
        for x in bit_mask:
            if int(x):
                temp_data += bites[bites_index]
                bites_index += 1
            else:
                temp_data += "0"
        return temp_data

    def write_data_to_working_image(self, data, bites_amount=3, is_bin=False, bit_mask="111"):  # bytes
        if not self.initialized:
            raise NotInitialezed()
        ds = self.data_stream(data, bites_amount, is_bin)
        ps = self.pixel_stream()
        for data, pixel in zip(ds, ps):
            temp_data = self.mask_apply(data, bites_amount, bit_mask)
            print(temp_data, '  ', data, '  ', bit_mask)
            temp = tuple((val_p & 254) | int(val_d) for val_d, val_p in zip(temp_data, pixel[0]))
            print(temp)
            self.pixels_map[
                pixel[1], pixel[2]] = temp  # tuple((val_p & 254) | int(val_d) for val_d, val_p in zip(data, pixel[0]))

    def show_result(self):
        if not self.initialized:
            raise NotInitialezed()
        self.working_image.show()

    def save(self, path="./huinya.bmp", file_format="bmp"):
        if not self.initialized:
            raise NotInitialezed()
        self.working_image.save(path, file_format)

    def drop_image(self):
        if not self.initialized:
            raise NotInitialezed()
        self.working_image = None
        self.data_to_write = None
        self.pixels_map = None
        self.initialized = False

    @property
    def image(self):
        if not self.initialized:
            raise NotInitialezed()
        return self.working_image


class Morse:
    def __init__(self, text):
        self.morse_alphabet = {
            "A": ".-",
            "B": "-...",
            "C": "-.-.",
            "D": "-..",
            "E": ".",
            "F": "..-.",
            "G": "--.",
            "H": "....",
            "I": "..",
            "J": ".---",
            "K": "-.-",
            "L": ".-..",
            "M": "--",
            "N": "-.",
            "O": "---",
            "P": ".--.",
            "Q": "--.-",
            "R": ".-.",
            "S": "...",
            "T": "-",
            "U": "..-",
            "V": "...-",
            "W": ".--",
            "X": "-..-",
            "Y": "-.--",
            "Z": "--..",
            " ": "/",
            "": "",
            "0": "-----",
            "1": ".----",
            "2": "..---",
            "3": "...--",
            "4": "....-",
            "5": ".....",
            "6": "-....",
            "7": "--...",
            "8": "---..",
            "9": "----.",

            "_": "..--.-"
        }

        self.inverse_morse_alphabet = dict((v, k) for (k, v) in self.morse_alphabet.items())
        self.message = text
        self.position_in_string = 0

    def __str__(self):
        return self.message

    def get(self):
        return self.message

    def __morse_to_bin(self, morse_char):
        return "0".join(morse_char).replace(".", "1").replace("-", "111")

    def __decode_morse(self):
        return " ".join(
            "".join(self.inverse_morse_alphabet[b] for b in a) for a in [x.split(' ') for x in self.message.split('/')])

    def __del_end(self, string):
        if len(string) >= 3 and string[-3:] == '000':
            return string[:-3]
        else:
            return string

    def encode(self):
        encoded_message = ''
        for char in self.message:
            if char == " ":
                encoded_message = self.__del_end(encoded_message) + "0000000"
            else:
                encoded_message += self.__morse_to_bin(self.morse_alphabet[char.upper()]) + "000"

        self.message = self.__del_end(encoded_message)

    def decode(self):
        self.position_in_string = 0
        self.message = " / ".join(
            " ".join(("".join(["." if g == "1" else "-" for g in b.split("0")])) for b in x) for x in
            [i.split('000') for i in self.message.split('0000000')]) + " "
        self.message = self.__decode_morse()


class QRCreator:
    def __init__(self, text):
        self.qr_code = qrcode.QRCode(version=1, box_size=8, border=1)
        self.qr_code.add_data(text)
        self.qr_code.make(fit=True)
        self._image = self.qr_code.make_image()
        self._image = self._image.convert("RGB")
        draw = ImageDraw.Draw(self._image)
        pix = self._image.load()
        qr_width, qr_height = self._image.size
        for i in range(qr_width):
            for j in range(qr_height):
                if pix[i, j] != (0, 0, 0):
                    draw.point((i, j), (3, 3, 3))

    @property
    def image(self):
        return self._image

    @property
    def qr_width(self):
        _qr_width, _qr_height = self._image.size
        return _qr_width

    @property
    def qr_height(self):
        _qr_width, _qr_height = self._image.size
        return _qr_height

    @property
    def qr_size(self):
        return self._image.size  # self._image.width , self._image.height


class TaskCreator:
    def __init__(self, flag_text, easter_egg_link):
        self.qr = QRCreator(easter_egg_link)
        self.morse = Morse(flag_text)
        self.morse.encode()
        self.flag_data = self.morse.get()
        self.image_data_writer = ImageDataWriter()
        self.image_data_writer.init_image_by_data(self.flag_data, is_bin=True)
        self.image_data_writer.write_data_to_working_image(self.flag_data, is_bin=True)
        self.flag_image = self.image_data_writer.image
        self.easter_egg_image = self.qr.image

    def compile_image(self , image_name):
        img_width = 450
        img_height = 350
        font_size = 32
        text_width = 10
        text_height = (img_height - font_size) // 2
        len_text = 120
        indent = 10
        text = "Flag in "
        color = (0, 0, 0)

        key = self.flag_image  # Image.open("huinya (2).bmp")
        key_width, key_height = key.size
        fonts_folder = 'FONT_FOLDER'  # e.g. 'Liinverse_morse_alphabetbrary/Fonts'
        arial_font = ImageFont.truetype(os.path.join(fonts_folder, 'arial.ttf'), font_size)

        img = Image.new('RGB', (img_width, img_height), color)
        img_drawer = ImageDraw.Draw(img)
        img_drawer.text((text_width, text_height), text, font=arial_font)
        img.paste(self.easter_egg_image,
                  (len_text + key_width + indent, (img_height - self.qr.qr_height) // 2))
        img.paste(key, (len_text, (img_height - key_height) // 2))
        img.save(image_name)

if  __name__ == "__main__":
    """flag = input("Flag: ")
    easter_egg = input("Easter egg: ")
    task_name = input("Output name: ")
    """
    flag = "RUCTF_2017_ba40a495fcfd4c1ae547fd273eb05dfb"
    easter_egg = "https://goo.gl/3dlwyt"
    task_name = "Output.png"
    ts = TaskCreator(flag, easter_egg)
    ts.compile_image(task_name)
