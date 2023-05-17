from flask import Flask, render_template, request
from rembg import remove
from PIL import Image
import requests
import asyncio
import imgbbpy
import uuid6
import os


async def imgbbuploader(imagename):
    client = imgbbpy.AsyncClient('63ade78000b432d3027d259c0c2678d4')
    image = await client.upload(file='temp/'+imagename)
    if os.path.exists('temp/'+imagename):
        os.remove('temp/'+imagename)
    else:
        print("The file does not exist")
    return image.url


def removebackground(url):
    imagename = str(uuid6.uuid6()) + '.png'
    input = Image.open(requests.get(url, stream=True).raw)
    output = remove(input)
    output.save('temp/' + imagename)
    return asyncio.run(imgbbuploader(imagename))


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/removebg')
def removebg():
    print('trying to remove background')
    url = request.args.get('url')
    if(url):
        return removebackground(url)
    else:
        return 'error'

if __name__ == '__main__':
    app.run(debug=True)