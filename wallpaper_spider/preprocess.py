import PIL.Image as Image
import os
from tqdm import tqdm
import random

PATH = './data/'
CROP = './out/crop/'
STRECH = './out/stretch/'
TRAINING_RATE = 0.8


def stretch_img(path, shape=(256, 256)):
    img = Image.open(path)
    img = img.resize(shape, Image.ANTIALIAS)
    return img


def crop_img(path, shape=(256, 256)):
    img = Image.open(path)
    img = img.crop((0, 0, 219, 219))
    img = img.resize(shape, Image.ANTIALIAS)
    return img


def color_with_gray(img: Image):
    """
    Combine image with its gray image horizontally [img, gray_img]
    :param img:
    :return:
    """
    gray_img = img.convert('L')
    new_img = Image.new('RGB', (512, 256))

    new_img.paste(img, (0, 0))
    new_img.paste(gray_img, (256, 0))

    return new_img


def resize(path, method):
    return method(path)


def preprocess():
    if not os.path.exists(CROP):
        os.makedirs(CROP)
        os.makedirs(CROP + 'train')
        os.makedirs(CROP + 'test')
    if not os.path.exists(STRECH):
        os.makedirs(STRECH)
        os.makedirs(STRECH + 'train')
        os.makedirs(STRECH + 'test')

    files = []
    for (dirpath, dirnames, filenames) in os.walk(PATH):
        if len(filenames) > 0:
            files.extend([dirpath + '/' + name for name in filenames])

    for image in tqdm(files):
        train = 'train/' if random.random() < TRAINING_RATE else 'test/'
        # color_with_gray(resize(image, crop_img)).save(CROP + train + image.split('/')[-1])
        resize(image, crop_img).convert('L').save(CROP + train + image.split('/')[-1])
        # color_with_gray(resize(image, stretch_img)).save(STRECH + train + image.split('/')[-1])
        # color_with_gray(resize(image, stretch_img)).save(STRECH + train + image.split('/')[-1])


if __name__ == '__main__':
    preprocess()

