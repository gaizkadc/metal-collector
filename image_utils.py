import datetime
import os
import random
import urllib.request
import math

from PIL import Image, ImageFont, ImageDraw, ImageEnhance


def create_header(logger):
    logger.info('creating header')

    today = datetime.datetime.now()
    today_str = today.strftime('%Y%m%d')

    img_folder_path = os.getenv('IMGS_FOLDER')

    if not os.path.exists(img_folder_path):
        os.makedirs(img_folder_path)

    header_path = img_folder_path + '/header.png'

    background_folder_path = os.getenv('BACKGROUND_FOLDER_PATH')
    background_path = get_background(logger, background_folder_path)

    prepare_background(logger, background_path, header_path)

    text_color = (255, 255, 255)

    write_header(logger, today_str, header_path, text_color)

    logger.info('header image created')

    return header_path


def get_background(logger, background_folder_path):
    logger.info('getting background')

    backgrounds = [bg for bg in os.listdir(background_folder_path) if bg.endswith(".png")]
    return background_folder_path + '/' + random.choice(backgrounds)


def darken_img(logger, img_path, dark_img_path):
    logger.info('darkening image ' + img_path)

    background_img = Image.open(img_path)
    enhancer = ImageEnhance.Brightness(background_img)
    darker_background_img = enhancer.enhance(0.4)
    darker_background_img.save(dark_img_path)


def write_header(logger, today_str, img_path, text_color):
    logger.info('writing title')

    font_size = 135
    fonts_path = os.getenv('FONTS_PATH')
    body_font = ImageFont.truetype(fonts_path + '/Montserrat-Bold.ttf', font_size)

    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)

    title_position = (140, 35)
    draw.text(title_position, today_str, text_color, font=body_font)

    img.save(img_path)


def prepare_background(logger, background_path, resulting_img_path):
    logger.info('preparing background')

    darken_img(logger, background_path, resulting_img_path)

    header_size = (900, 225)

    header = Image.new('RGB', header_size)
    bg_image = Image.open(resulting_img_path)
    bg_image.resize((300, 300), Image.ANTIALIAS)

    header.paste(bg_image, (0, 0))
    header.paste(bg_image, (300, 0))
    header.paste(bg_image, (600, 0))

    header.save(resulting_img_path)


def create_patch(logger, album, index):
    logger.info('creating patch ' + str(index))

    img_folder_path = os.getenv('IMGS_FOLDER')
    patch_path = img_folder_path + '/' + str(index) + '.png'

    urllib.request.urlretrieve(album['cover'], patch_path)

    patch_height = 300
    patch_size = (patch_height, patch_height)
    angle = 180
    gradient_magnitude = 1.5

    patch = Image.open(patch_path)
    patch = patch.resize(patch_size, Image.ANTIALIAS)
    patch = patch.rotate(angle)

    patch = patch.convert('RGBA')
    gradient = Image.new('L', (1, patch_height), color=0xFF)
    for x in range(patch_height):
        gradient.putpixel((0, x), int(255 * (1 - gradient_magnitude * float(x) / patch_height)))
    alpha = gradient.resize(patch_size)
    black_im = Image.new('RGBA', patch_size, color=0)
    black_im.putalpha(alpha)
    gradient_im = Image.alpha_composite(patch, black_im)
    gradient_im = gradient_im.rotate(angle)

    gradient_im.save(patch_path)

    add_text_to_patch(logger, patch_path, album)


def add_text_to_patch(logger, patch_path, album):
    logger.info('adding text to patch')

    text_offset = 10
    text_color = (255, 255, 255)
    line_max_width = 280

    fonts_path = os.getenv('FONTS_PATH')
    font_artist = ImageFont.truetype(fonts_path + '/OpenSans-Bold.ttf', 24)
    font_album = ImageFont.truetype(fonts_path + '/OpenSans-Regular.ttf', 24)

    artist_lines = text_wrap(logger, album['artist'], font_artist, line_max_width)
    album_lines = text_wrap(logger, album['album'], font_album, line_max_width)

    total_lines = len(artist_lines) + len(album_lines)

    artist_position = [text_offset, 240 - text_offset]
    album_position = [artist_position[0], artist_position[1] + 30]

    patch = Image.open(patch_path)
    patch_draw = ImageDraw.Draw(patch)

    for i, line in enumerate(artist_lines):
        patch_draw.text((artist_position[0], artist_position[1] - 30 * (total_lines - i - 2)), line, text_color, font=font_artist)
    for i, line in enumerate(album_lines):
        patch_draw.text((album_position[0], album_position[1] - 30 * (len(album_lines) - i - 1)), line, text_color, font=font_album)

    patch.save(patch_path)


def text_wrap(logger, text, font, max_width):
    logger.info('wrapping text: ' + text)

    lines = []

    if font.getsize(text)[0] <= max_width:
        lines.append(text)
    else:
        words = text.split(' ')
        i = 0
        while i < len(words):
            line = ''
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            lines.append(line)

    return lines


def create_collage(logger, album_list):
    logger.info('creating collage')

    for i, album in enumerate(album_list):
        if i >= 9:
            break

        else:
            create_patch(logger, album, i)

    img_folder_path = os.getenv('IMGS_FOLDER')
    collage_path = img_folder_path + '/collage.png'
    header_path = img_folder_path + '/header.png'
    header_height = 225

    collage_size = (900, 1125)

    collage = Image.new('RGB', collage_size)

    header = Image.open(header_path)
    collage.paste(header, (0, 0))

    for i in range(0, 9):
        patch_path = img_folder_path + '/' + str(i) + '.png'
        patch = Image.open(patch_path)

        collage_position = (300 * math.floor(i / 3), header_height + (300 * (i % 3)))

        collage.paste(patch, collage_position)

    collage.save(collage_path)

    return collage_path
