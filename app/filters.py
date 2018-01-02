from PIL import ImageFilter, Image


def filtering(filt, image, path):
    if filt == 'Black':
        blackfilter(image, path)
    elif filt == 'Jofilt':
        jofilter(image, path)
    elif filt == 'AKA':
        akafilter(image, path)
    elif filt == 'Random':
        randomfilter(image, path)
    else:
        image.filter(filt).save(path)


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