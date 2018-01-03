from PIL import ImageFilter, Image, ImageFont, ImageDraw
from resizeimage import resizeimage
from random import randint, choice


def filtering(filt, image, path):
    if filt == 'Black':
        blackfilter(image, path)
    elif filt == 'Jofilt':
        jofilter(image, path)
    elif filt == 'AKA':
        akafilter(image, path)
    elif filt == 'Random':
        randomfilter(image, path)
    elif filt == 'Andy':
        filter_warhol(
            image,
            path,
            size=999,
            colors=4,
            color=(0, 0, 0),
            padding=24,
            smooths=8, )
    elif filt == 'ColorScale':
        filter_colorscale(image, path, size=1200, color=(0, 0, 0))
    elif filt == 'Minimalist':
        filter_minimalist(image, path)
    elif filt == 'Lettertext':
        filter_lettertext(image, path)
    else:
        image.filter(filt).save(path)


def filter_lettertext(image,
                      path,
                      text="Base Camp Coding Academy",
                      fontsize=200,
                      size=1024,
                      colors=256,
                      color=(255, 255, 255),
                      padding=64):
    # image properties
    colors = max(1, min(256, colors))
    r, g, b = color
    color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))

    # load image into memory
    image = resizeimage.resize_cover(
        image, [
            size,
            size,
        ], validate=False).convert('RGB')
    image = image.quantize(colors).convert('RGB')
    data = image.getdata()

    # create text image
    text_image = Image.new('RGB', (size, size))
    text_image.putdata([color for _ in range(size**2)])
    text_image = text_image.convert('RGB')

    # draw on text_image
    font = ImageFont.truetype(
        '/home/basecamp/.local/share/fonts/Blackout Two AM.ttf', fontsize)
    draw = ImageDraw.Draw(text_image, mode='RGB')
    c = 0
    for word in text.split():
        draw.text((padding // 2, padding + c), word, font=font, fill=(0, 0, 0))
        c += size // len(text.split())

    # get data from text image
    text_image = text_image.convert('RGB')
    text_image = resizeimage.resize_cover(
        text_image, [
            size,
            size,
        ], validate=False).convert('RGB')
    text_data = text_image.getdata()

    # make new data
    new_data = [
        data[i] if text_data[i] == color else color for i in range(size**2)
    ]

    image = Image.new('RGB', (size, size))
    image.putdata(new_data)
    image.save(path)


def filter_colorscale(image,
                      path,
                      size=1024,
                      color=(255, 255, 255),
                      padding=16):
    # image properties
    colors = 256
    r, g, b = color
    color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    q_size = (size - (4 * padding)) // 3
    size = size - (size % (q_size * 3 + padding * 4))

    # load image into memory
    image = resizeimage.resize_cover(
        image, [q_size, q_size], validate=False).convert('RGB')
    image = image.quantize(colors).convert('RGB')

    # get image data
    px_data = []
    # rgb
    rgb = list(image.getdata())
    for r in range(3):
        for g in range(3):
            for b in range(3):
                if ((r + g + b) == 3) and ((r**2 + b**2 + g**2) == 5):
                    px_data.append(
                        list(map(lambda t: (t[r], t[g], t[b]), rgb)))

    # r g b only
    px_data.append(list(map(lambda t: (t[0], 0, 0), rgb)))
    px_data.append(list(map(lambda t: (0, t[1], 0), rgb)))
    px_data.append(list(map(lambda t: (0, 0, t[2]), rgb)))

    px_data[3], px_data[7], px_data[6], px_data[2], px_data[5] = px_data[
        2], px_data[3], px_data[5], px_data[6], px_data[7]

    data = []
    long_pad = [color for _ in range(size)]
    short_pad = [color for _ in range(padding)]
    for r in range(3):
        for _ in range(padding):
            data.extend(long_pad)
        for i in range(0, q_size**2, q_size):
            data.extend(short_pad)
            data.extend(px_data[3 * r][i:i + q_size])
            data.extend(short_pad)
            data.extend(px_data[3 * r + 1][i:i + q_size])
            data.extend(short_pad)
            data.extend(px_data[3 * r + 2][i:i + q_size])
            data.extend(short_pad)
    for _ in range(padding):
        data.extend(long_pad)

    image = Image.new('RGB', (size, size))
    image.putdata(data)
    image.save(path)


def filter_warhol(
        image,
        path,
        size=1024,
        colors=4,
        color=(0, 0, 0),
        padding=24,
        smooths=8, ):
    # image properties
    colors = max(1, min(256, colors))
    r, g, b = color
    color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    q_size = (size - (3 * padding)) // 2
    size = size - (size % (q_size * 2 + padding * 3))

    # load image into memory
    image = resizeimage.resize_cover(
        image, [
            q_size,
            q_size,
        ], validate=False).convert('RGB')
    # smooth image
    for _ in range(smooths):
        image = image.filter(ImageFilter.SMOOTH_MORE).convert('RGB').quantize(
            colors).convert('RGB')

    # get image data
    data = list(image.getdata())

    # get colors in picture
    def sum_tuple(t):
        r, g, b = t
        return r + g + b

    def random_color():
        return (randint(0, 255), randint(0, 255), randint(0, 255))

    colors_in_picture = sorted(list(set(data)), key=sum_tuple)
    k = str(colors_in_picture[0])
    warhol = []

    # generate lists of data with new colors
    for _ in range(4):
        d = {str(v): random_color() for v in colors_in_picture[1:]}
        d[k] = (0, 0, 0)
        warhol.append([d.get(str(px)) for px in data])

    data = []
    long_pad = [color for _ in range(size)]
    short_pad = [color for _ in range(padding)]
    for r in range(2):
        for _ in range(padding):
            data.extend(long_pad)
        for i in range(0, q_size**2, q_size):
            data.extend(short_pad)
            data.extend(warhol[2 * r][i:i + q_size])
            data.extend(short_pad)
            data.extend(warhol[2 * r + 1][i:i + q_size])
            data.extend(short_pad)
    for _ in range(padding):
        data.extend(long_pad)

    image = Image.new('RGB', (size, size))
    image.putdata(data)

    image.save(path)


def filter_minimalist(image,
                      path,
                      size=1024,
                      colors=4,
                      color=(255, 255, 255),
                      padding=128):
    # image properties
    colors = max(1, min(256, colors))
    r, g, b = color
    color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    height = (size - ((colors + 1) * padding)) // colors
    size = size - (size % ((height * colors) + (colors + 1) * padding))
    width = size - (2 * padding)

    # load image into memory
    image = resizeimage.resize_cover(
        image, [size, size], validate=False).convert('RGB')
    image = image.quantize(colors).convert('RGB')

    # get image data
    colors_in_picture = list(set(list(image.getdata())))

    # padding data sets
    long_pad = [color for _ in range(padding * size)]
    short_pad = [color for _ in range(padding)]

    data = long_pad[:]
    for unique_color in colors_in_picture:
        for i in range(height):
            data.extend(short_pad)
            data.extend([unique_color for _ in range(width)])
            data.extend(short_pad)
        data.extend(long_pad)

    image = Image.new('RGB', (size, size))
    image.putdata(data)
    image.save(path)


def blackfilter(image, path):
    image.convert('L').convert('RGB').save(path)


def jofilter(image, path):
    image2 = Image.open(
        '/home/basecamp/Documents/DailyExercises/Dec/Finstagram/app/static/app/images/jofilter.jpg'
    )
    Image.blend(image, image2, 0.33).save(path)


def akafilter(image, path):
    image = image.convert('L').quantize(3).convert('RGB').filter(
        ImageFilter.SMOOTH_MORE).filter(ImageFilter.SMOOTH_MORE).filter(
            ImageFilter.SMOOTH_MORE).quantize(3).convert('RGB')
    data = image.getdata()
    color_a, color_b, _ = tuple(set(data))
    d = {str(color_a): (239, 186, 209), str(color_b): (16, 165, 0)}
    image = Image.new('RGB', image.size)
    image.putdata([d.get(str(t), (255, 255, 255)) for t in data])
    image.save(path)


def randomfilter(image, path):
    image = image.convert('L').quantize(3).convert('RGB').filter(
        ImageFilter.SMOOTH_MORE).filter(ImageFilter.SMOOTH_MORE).filter(
            ImageFilter.SMOOTH_MORE).quantize(3).convert('RGB')
    w, h = image.size
    ca = (randint(0, 255), randint(0, 255), randint(0, 255))
    cb = (randint(0, 255), randint(0, 255), randint(0, 255))

    data = list(image.getdata())
    color_a, color_b, _ = tuple(set(data))
    d = [{
        str(color_a): ca,
        str(color_b): cb
    }, {
        str(color_b): ca,
        str(color_a): cb
    }]
    n = len(data)
    c = 0
    while c < n // 2:
        for i in range(w // 2):
            key = str(data[c + i])
            data[c + i] = d[0].get(key, (255, 255, 255))
        for i in range(w // 2, w):
            key = str(data[c + i])
            data[c + i] = d[1].get(key, (255, 255, 255))
        c += n // h

    while c < n:
        for i in range(w // 2):
            key = str(data[c + i])
            data[c + i] = d[1].get(key, (255, 255, 255))
        for i in range(w // 2, w):
            key = str(data[c + i])
            data[c + i] = d[0].get(key, (255, 255, 255))
        c += n // h
    image = Image.new('RGB', image.size)
    image.putdata(data)
    image.save(path)