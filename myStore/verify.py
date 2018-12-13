from PIL import Image, ImageDraw, ImageFont, ImageFilter

import random, string,time,os


def getRandomChar(count=4):
    # s是一个素材池，包含了字母和数字 每循环一次从s中取出一个数据
    s = string.ascii_letters + string.digits
    char = ''
    for i in range(count):
        char += random.choice(s)
    return char


def getRandomColor():
    return (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))


def create_code(save_path='static/cache/',):
    img=Image.new('RGBA',size=(120,30),color=(255,255,255,200))
    draw=ImageDraw.Draw(img)
    font=ImageFont.truetype('arial.ttf',25)
    code=getRandomChar(4)
    for i in range(4):
        draw.text(xy=(30*i+5,0),text=code[i],fill=getRandomColor(),font=font)
    for i in range(10):
        draw.point(xy=(random.randint(0,120),random.randint(0,30)),fill=(0,0,0))
        draw.line([(random.randint(0,120),random.randint(0,30)),(random.randint(0,120),random.randint(0,30))],
                  fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    img=img.filter(ImageFilter.SMOOTH_MORE)
    return img,code