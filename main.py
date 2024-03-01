import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

from image_process import median_cut


def main_page():
    st.title("# Find the color palette")

    sample_image = Image.open("./sample_image/sample0.png")
    image_area = st.image(sample_image)

    top_n_color,  total_pixels = find_color(sample_image, 10)

    df = pd.DataFrame(
        {
            'Color': [f"https://www.colorhexa.com/{hex_code.strip('#')}.png" for hex_code in top_n_color.keys()],
            'Hex Code': top_n_color.keys(),
            'Percentage (%)': (np.array(list(top_n_color.values())) / total_pixels) * 100
        }
    )
    df.index += 1
    color_palette_area = st.dataframe(
        df,
        use_container_width=True,
        column_config={
            "Color": st.column_config.ImageColumn(
                "Color", help="Preview color"
            )
        }
    )

    with st.form(key='my_form'):
        file_upload = st.file_uploader('Upload a PNG image', type='png')
        number_of_colors = st.number_input(label='Number of colors:', placeholder='How many color do you want to find?',
                                           min_value=10, max_value=20)
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        uploaded_image = Image.open(file_upload)
        image_area.image(uploaded_image)

        top_n_color, total_pixels = find_color(uploaded_image, number_of_colors)

        df = pd.DataFrame(
            {
                'Color': [f"https://www.colorhexa.com/{hex_code.strip('#')}.png" for hex_code in top_n_color.keys()],
                'Hex Code': top_n_color.keys(),
                'Percentage (%)': (np.array(list(top_n_color.values())) / total_pixels) * 100
            }
        )
        df.index += 1
        color_palette_area.dataframe(
            df,
            use_container_width=True,
            column_config={
                "Color": st.column_config.ImageColumn(
                    "Color", help="Preview color"
                )
            }
        )


def find_color(image_file, number_of_colors):
    image_array = np.array(image_file)

    total_pixels = image_array.shape[0] * image_array.shape[1]

    hex_list = []
    for x in range(image_array.shape[0]):
        for y in range(image_array.shape[1]):
            hex_list.append(rgb2hex(image_array[x][y]))

    return top_n(hex_list, number_of_colors), total_pixels


def top_n(hex_list, number_of_colors):
    hex_frequency = {}

    for hex_code in hex_list:
        if hex_code in hex_frequency:
            hex_frequency[hex_code] += 1
        else:
            hex_frequency[hex_code] = 1

    sorted_hex = sorted(hex_frequency.items(), key=lambda x: x[1])

    return dict(sorted_hex[::-1][:number_of_colors])


def rgb2hex(rgb_tuple):
    return f"#{rgb_tuple[0]:0>2X}{rgb_tuple[1]:0>2X}{rgb_tuple[2]:0>2X}"


def hex2rgb(hex_code):
    hex_code = hex_code.strip("#")
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex_code[i:i + 2], 16)
        rgb.append(decimal)

    return tuple(rgb)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_page()
