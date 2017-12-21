from PIL import Image, ImageFilter
from resizeimage import resizeimage
from random import randint

image = Image.open(
    '/home/basecamp/Documents/DailyExercises/Dec/Finstagram/app/static/app/images/60F2CB82-9F94-428C-A167-EF67760B7E54.jpeg'
)
image = resizeimage.resize_cover(image, [500, 500], validate=False)

image = image.convert('L').quantize(3).convert('RGB').filter(
    ImageFilter.SMOOTH_MORE).filter(ImageFilter.SMOOTH_MORE).filter(
        ImageFilter.SMOOTH_MORE).quantize(3).convert('RGB')

# l = list(image.getdata())
# n = len(l)

# new_data = []

# new_data.extend(
#     list(map(lambda t: (255 - t[0], 255 - t[2], 255), l[0:(n // 3)])))
# new_data.extend(
#     list(map(lambda t: (255, 255 - t[1], 255), l[(n // 3):(n // 3 * 2)])))
# new_data.extend(
# list(map(lambda t: (155, 255 - t[2], 100 - t[2]), l[(n // 3 * 2):])))
w, h = image.size
ca = (randint(100, 255), randint(0, 100), randint(0, 200))
cb = (randint(0, 100), randint(101, 201), randint(201, 255))

data = list(image.getdata())
color_a, color_b, _ = tuple(set(data))
# d = [{
#     str(color_a): (239, 186, 209),
#     str(color_b): (16, 165, 0)
# }, {
#     str(color_b): (239, 186, 209),
#     str(color_a): (16, 165, 0)
# }]
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

im2 = Image.new('RGB', image.size)
im2.putdata(data)
# im2.putdata(list(map(lambda t: (255 - t[2], t[2], 255 - t[2]), data)))

# aka = new_data.extend(
#     )
# calhoun = new_data.extend(
#     list(
#         map(lambda t: (250 - t[2], 255 - t[1], 255 - t[0]), l[(n // 3 * 2):])))

im2.show()