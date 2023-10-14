import base64
import io
from PIL import Image
from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route('/compress', methods=['POST'])
def getvalues():
    if(request.method == 'POST'):
        img = request.json['Img']
        imgs = request.json["Imgsize"]
        imgq = request.json["Imgquality"]
        res = compressMe(img, imgs, imgq)
        return jsonify({
                        'Original size': '',
                        'Compressed size': '',
                        'CompressedImg': res})


def compressMe(image, size, imgquality):

    image_bytes = io.BytesIO(base64.b64decode(image))


    pil_image = Image.open(image_bytes)



    pil_image = pil_image.resize((size, size))

    rgb_im = pil_image.convert('RGB')
  

    rgb_im.save(image_bytes, format='JPEG', quality=imgquality)

#     image_file_size = rgb_im.tell()

#     print(f"compressed image size {image_file_size}")

    compressed_image = base64.b64encode(image_bytes.getvalue()).decode('utf-8')

    # print(compressed_size)

    return compressed_image



def compress_img(image_name, new_size_ratio=0.2, quality=30, width=None, height=None, to_jpg=True):
   
    image_bytes = io.BytesIO(base64.b64decode(image))
    # load the image to memory
    img = Image.open(image_name)
    # print the original image shape
    print("[*] Image shape:", img.size)
    # get the original image size in bytes
    image_size = os.path.getsize(image_name)
    # print the size before compression/resizing
    print("[*] Size before compression:", get_size_format(image_size))
    if new_size_ratio < 1.0:
        # if resizing ratio is below 1.0, then multiply width & height with this ratio to reduce image size
        img = img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)), Image.ANTIALIAS)
        # print new image shape
        print("[+] New Image shape:", img.size)
    elif width and height:
        # if width and height are set, resize with them instead
        img = img.resize((width, height), Image.ANTIALIAS)
        # print new image shape
        print("[+] New Image shape:", img.size)
    # split the filename and extension
    filename, ext = os.path.splitext(image_name)
    # make new filename appending _compressed to the original file name
    if to_jpg:
        # change the extension to JPEG
        new_filename = f"{filename}_compressed.jpg"
    else:
        # retain the same extension of the original image
        new_filename = f"{filename}_compressed{ext}"
    try:
        # save the image with the corresponding quality and optimize set to True
        img.save(new_filename, quality=quality, optimize=True)
    except OSError:
        # convert the image to RGB mode first
        img = img.convert("RGB")
        # save the image with the corresponding quality and optimize set to True
        img.save(new_filename, quality=quality, optimize=True)
    print("[+] New file saved:", new_filename)
    # get the new image size in bytes
    new_image_size = os.path.getsize(new_filename)
    

# print the new size in a good format
    print("[+] Size after compression:", get_size_format(new_image_size))
    # calculate the saving bytes
    saving_diff = new_image_size - image_size
    # print the saving percentage
    print(f"[+] Image size change: {saving_diff/image_size*100:.2f}% of the original image size.")




if __name__ == '__main__':

    app.run(debug=True)
