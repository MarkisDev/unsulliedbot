"""
Unsullied Bot - A script to automate blog stuff.
This script has the needed code to finish image manipulation
@author : MarkisDev
@copyright : https://markis.dev
"""
# Importing all the lib needed
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from urllib.request import Request, urlopen
import requests
from unique_id import get_unique_id
import base64
import json
import codecs

# Defining our imgBB API key
imgBB_key = "YOUR_imgBB_API_KEY"

# Function to fetch Image from URL 
def get_img(url):
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        i = Image.open(urlopen(req))
        width, height = i.size

        # Not saving it currently, didn't see the need to. Keeping it here because I wrote this while listening to Brodha V 
        # Let's face it Brodha V is awesome. 
        # Yes, I like Brodha V and KSHMR and Ritviz, if you don't thats cool
        # Eitherways, I'm not removing this bit (>.<)

        # directory = "temp/" + get_unique_id(excluded_chars=r'~`!@#$%^&*()_-+=\|]}[{;:"/?.>,<') + ".png"
        # i.save(directory, quality=5)
        # return {"status":True, "image":i, "directory":directory, "width":width, "height":height}
        return {"status":True, "image":i, "width":width, "height":height}
    except Exception as e:
        print(e)
        return {"status":False}

# Function to resize image
def resize_img(image, width, height):
    size = (width, height)
    image.thumbnail(size)
    return image

# Function to paste the URL fetched image onto template
def make_img(image, color, x, y):
    directory = ''
    if color.lower() == 'orange':
        directory = 'img/orange.png'
    elif color.lower() == 'purple':
        directory = 'img/purple.png'
    elif color.lower() == 'green':
        directory = 'img/green.png'
    template = Image.open(directory)
    template.thumbnail((671,671))
    template.paste(image, (x, y))
    return template

# Function to draw title onto the image (also unescaping \n)
def write_title(image, text, size, x, y):
    text = codecs.decode(text, 'unicode-escape')
    draw = ImageDraw.Draw(image)
    title = ImageFont.truetype(r'fonts/deathstar.otf', size)
    draw.text((x, y), text, (255,255,255), font=title)
    return image

# Function to draw author onto image (also unescaping \n)
def write_author(image, color, text, size, x, y):
    text = codecs.decode(text, 'unicode-escape')
    if text.lower() == '- sarahfin' and x == 488 and y == 526:
        x = 465
        y = 521
    elif text.lower() == '- swapneel' and x == 488 and y == 526:
        x = 460
        y = 526
    elif text.lower() == '- dheeraj' and x == 488 and y == 526:
        x = 463
        y = 526
    elif text.lower() == '- rijuth' and x == 488 and y == 526:
        x = 488
        y = 526
    elif text.lower() == '- joe' and x == 488 and y == 526:
        x = 505
        y = 526
    r = 255
    g = 255
    b = 255
    draw = ImageDraw.Draw(image)
    author = ImageFont.truetype(r'fonts/deathstar.otf', size)
    if color.lower() == 'orange':
        r = 204
        g = 51
        b = 0
    elif color.lower() == 'purple':
        r = 128
        g = 0
        b = 128        
    elif color.lower() == 'green':
        r = 34
        g = 153
        b = 84
    draw.text((x, y), text, (r,g,b), font=author)
    return image

# Function to save the image so that we can upload it (will be deleted later on)
def save_img(image):
    directory = "temp/" + get_unique_id(excluded_chars=r'~`!@#$%^&*()_-+=\|]}[{;:"/?.>,<') + ".png"
    image.save(directory, quality=95)
    return {"directory": directory}

# Function to upload the image to imgBB
def upload_img(directory):
    try:
        with open(directory, "rb") as file:
            url = "https://api.imgbb.com/1/upload"
            payload = {"key":imgBB_key, "image":base64.b64encode(file.read()), "expiration":259200}
            response = requests.post(url, payload)
            result = json.loads(response.text)
            return result
    except:
        return {"success" : False}


