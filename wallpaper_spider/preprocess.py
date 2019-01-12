import PIL.Image as Image
import os
from tqdm import tqdm
import random


def stretch_img(path, shape=(256, 256)):
    img = Image.open(path)
    img = img.resize(shape, Image.ANTIALIAS)
    return img


def crop_img(path, shape=(256, 256)):
    img = Image.open(path)
    img = img.crop((0, 0, 219, 219))
    img = img.resize(shape, Image.ANTIALIAS)
    return img


# Combine image with its gray image horizontally [img, gray_img]
def color_with_gray(img: Image):
    gray_img = img.convert('L')
    new_img = Image.new('RGB', (512, 256))

    new_img.paste(img, (0, 0))
    new_img.paste(gray_img, (256, 0))

    return new_img


def resize(path, method):
    return method(path)


def preprocess(input, output, method, train_ratio=0.8):
    if not os.path.exists(output):
        os.makedirs(output)
        os.makedirs(output + 'train')
        os.makedirs(output + 'test')

    files = []
    for (dirpath, dirnames, filenames) in os.walk(input):
        if len(filenames) > 0:
            files.extend([dirpath + '/' + name for name in filenames])

    for image in tqdm(files):
        train = 'train/' if random.random() < train_ratio else 'test/'
        color_with_gray(resize(image, method)).save(output + train + image.split('/')[-1])


if __name__ == '__main__':
    data = './data/'
    save = './out/crop/'
    preprocess(data, save, crop_img)
