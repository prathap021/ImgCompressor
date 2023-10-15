import base64
import io
from PIL import Image
from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route('/api/compress', methods=['PUT'])
def getvalues():
    if(request.method == 'PUT'):

        payload = request.get_json()

        res = compressMe(payload["Img"], payload["ImgRatio"],
                         payload["Imgquality"], payload["Imgwidth"], payload["Imgheight"])

        return jsonify({
            'Original size': '',
            'Compressed size': '',
            'CompressedImg': res}), 201


def compressMe(image, new_size_ratio, quality, width=None, height=None):

    image_bytes = io.BytesIO(base64.b64decode(image))

    pil_image = Image.open(image_bytes)

    width, height, = pil_image.size
    
    print(pil_image.size)

    print(f"{width}x{height}")


    if new_size_ratio > 0.0:
        print("Ratio block called")

        pil_image = pil_image.resize((int(pil_image.size[0] * new_size_ratio),
                                     int(pil_image.size[1] * new_size_ratio)), Image.ANTIALIAS)

    elif width and height:

        print("height and width block called")

        pil_image = pil_image.resize((width, height), Image.ANTIALIAS)

    rgb_im = pil_image.convert("RGB")

    rgb_im.save(image_bytes, quality=quality, optimize=True, format='JPEG')
    image_file_size = image_bytes.tell()
    print(f"Image size {image_file_size}")

    compressed_image = base64.b64encode(image_bytes.getvalue()).decode('utf-8')

    return compressed_image


if __name__ == '__main__':

    app.run(debug=True,port=7000)
