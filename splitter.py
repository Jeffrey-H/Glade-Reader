import glob
import os
import time
from itertools import product

import pytesseract as pytesseract
from PIL import Image, ImageChops, ImageStat

block_height = 28


def crop():
    im = Image.open("./input.png")
    width, height = im.size

    left = 70
    top = 53
    right = width - 70
    bottom = height - 87

    out = os.path.join(".", f'cropped.png')
    im.crop((left, top, right, bottom)).save(out)


def tile(filename, dir_in, dir_out, d):
    name, ext = os.path.splitext(filename)
    img = Image.open(os.path.join(dir_in, filename))
    w, h = img.size

    for image in glob.glob("./splitted/*.png"):
        os.remove(image)

    grid = product(range(0, h - h % d, d), range(0, w - w % d, d))
    for i, j in grid:
        box = (j, i, j + d, i + d)
        out = os.path.join(dir_out, f'{name}_{i}_{j}{ext}')
        img.crop(box).save(out)


def get_by_char(d):
    if d == '‘':
        d = '0'
    if d == 'q':
        d = '8'
    if d == 'i':
        d = '1'
    if d == 'a':
        d = '3'
    if d == '*' or d == ':)' or d == ')':
        d = '9'
    if d == '?':
        d = '2'
    if d == 'c':
        d = '0'
    if d == 'v':
        d = '0'

    return d


def get_type(image_path, char):
    for path_two in glob.glob("./types/*.png"):
        image = Image.open(image_path)
        image_two = Image.open(path_two)

        width, height = image_two.size
        box = (7, 1, width, height)

        image = image.crop(box).convert('RGB')
        image_two = image_two.crop(box).convert('RGB')

        diff = ImageChops.difference(image, image_two)
        stat = ImageStat.Stat(diff)
        diff_ratio = sum(stat.mean) / (len(stat.mean) * 255)

        if diff_ratio < 0.01:
            type_name = path_two.replace('./types/', '').replace('.png', '')
            if type_name == "stone" or type_name == "tree" or type_name == "spike" or type_name == "wood":
                return "q"
            if type_name == "bomb":
                return "x" + str(char)
            if type_name == "white":
                return "w"
            if type_name == "black":
                return "l"
            if type_name == "blue":
                return "b"
            if type_name == "green":
                return "e"
            if type_name == "money":
                return "m" + str(char)
            if type_name == "orange":
                return "o"
            if type_name == "purple":
                return "p"
            if type_name == "red":
                return "r"
            if type_name == "gray":
                return "g"
            if type_name == "start":
                return "s" + str(char)
            if type_name == "target":
                return "t" + str(char)
            if type_name == "turn":
                return "d" + str(char)
            if type_name == "yellow":
                return "y"
    return "none"


def to_csv():
    current_size = block_height
    for image_path in glob.glob("./splitted/*.png"):
        image = Image.open(image_path)

        box = (1, 0, 6, 10)

        image = image.crop(box)
        image = ImageChops.invert(image.convert('RGB'))
        d = pytesseract.image_to_string(image, config="--psm 10")

        d = d.strip()
        d = get_by_char(d)
        image_type = get_type(image_path, d)

        if not d.isnumeric():
            out = os.path.join('./failed', f'' + str(d) + '-' + str(time.time() * 1000) + '.png')
            image.crop(box).save(out)

        image_height = image_path.replace('./splitted/cropped_', '').split('_')[0]

        if current_size != image_height:
            print()
            current_size = image_height

        print(image_type + ';', end='')


crop()
tile("./cropped.png", '.', './splitted', block_height)
to_csv()
