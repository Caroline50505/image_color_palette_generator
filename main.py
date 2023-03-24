from flask import Flask, render_template, request
from PIL import Image, ImageOps
import numpy as np

app = Flask(__name__)


def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb


def give_main_hex(file, code):
    my_image = Image.open(file).convert('RGB')
    size = my_image.size
    if size[0] >= 400 or size[1] >= 400:
        my_image = ImageOps.scale(image=my_image, factor=0.2)
    elif size[0] >= 600 or size[1] >= 600:
        my_image = ImageOps.scale(image=my_image, factor=0.4)
    elif size[0] >= 800 or size[1] >= 800:
        my_image = ImageOps.scale(image=my_image, factor=0.5)
    elif size[0] >= 1200 or size[1] >= 1200:
        my_image = ImageOps.scale(image=my_image, factor=0.6)
    my_image = ImageOps.posterize(my_image, 2)

    image_array = np.array(my_image)
    unique_colors = {}
    for column in image_array:
        for rgb in column:
            rgb_tuple = tuple(rgb)
            if rgb_tuple not in unique_colors:
                unique_colors[rgb_tuple] = 1
            if rgb_tuple in unique_colors:
                unique_colors[rgb_tuple] += 1

    unique_colors_sorted = sorted(unique_colors.items(), key=lambda x: x[1], reverse=True)
    converted_dic = dict(unique_colors_sorted)
    values = list(converted_dic.keys())
    main_values = values[0:10]

    if code == 'hex':
        hex_list = []
        for key in main_values:
            hex = rgb_to_hex(key)
            hex_list.append(hex)
        return hex_list
    else:
        return main_values


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        requested_file = request.files["file"]
        color_code = request.form["color_code"]
        hexes = give_main_hex(requested_file.stream, color_code)
        return render_template("index.html", colors_list=hexes, code=color_code)
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
