import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image

from image_process import median_cut, kmeans_extraction


def main_page():
    st.title("# Find the color palette")

    sample_image = Image.open("./sample_image/sample1.png")
    image_area = st.image(sample_image)

    df = find_color(sample_image, 10)

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
                                           min_value=3, max_value=10)
        selected_method = st.selectbox(
            "How would you like to extract the color palette?",
            ("Top N", "Median cut", "K-Means"),
            index=None,
            placeholder="Select extracting method...",
        )
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        uploaded_image = Image.open(file_upload)
        image_area.image(uploaded_image)

        color_palette_area.dataframe(empty_df(), use_container_width=True)

        df = find_color(uploaded_image, number_of_colors, selected_method)

        color_palette_area.dataframe(
            df,
            use_container_width=True,
            column_config={
                "Color": st.column_config.ImageColumn(
                    "Color", help="Preview color"
                )
            }
        )


def find_color(image_file, number_of_colors, method=None):
    image_array = np.array(image_file)

    total_pixels = image_array.shape[0] * image_array.shape[1]

    sorted_hex = count_hex(image_array)

    if not method:
        top_n_color = dict(sorted_hex[:number_of_colors])

        df = formatted_df(top_n_color, total_pixels)

        return df

    if method == "Median cut":
        median_cut_result = median_cut(image_file, number_of_colors)

        median_cut_hex = [rgb2hex(tuple(rgb)) for rgb in median_cut_result]

        hex_dict = dict(sorted_hex)

        find_frequency = {hex_code: hex_dict[hex_code] for hex_code in median_cut_hex}
        find_frequency = dict(sorted(find_frequency.items(), key=lambda x: x[1])[::-1])

        df = formatted_df(find_frequency, total_pixels)

        return df

    if method == "K-Means":
        kmeans_result = kmeans_extraction(image_file, number_of_colors)

        kmeans_hex = [rgb2hex(tuple(rgb)) for rgb in kmeans_result]

        hex_dict = dict(sorted_hex)

        find_frequency = {hex_code: hex_dict[hex_code] for hex_code in kmeans_hex}
        find_frequency = dict(sorted(find_frequency.items(), key=lambda x: x[1])[::-1])

        df = formatted_df(find_frequency, total_pixels)

        return df


def count_hex(image_array):
    hex_frequency = {}
    for x in range(image_array.shape[0]):
        for y in range(image_array.shape[1]):
            hex_code = rgb2hex(image_array[x][y])
            if hex_code in hex_frequency:
                hex_frequency[hex_code] += 1
            else:
                hex_frequency[hex_code] = 1

    sorted_hex = sorted(hex_frequency.items(), key=lambda x: x[1])

    return sorted_hex[::-1]


def rgb2hex(rgb_tuple):
    return f"#{rgb_tuple[0]:0>2X}{rgb_tuple[1]:0>2X}{rgb_tuple[2]:0>2X}"


def hex2rgb(hex_code):
    hex_code = hex_code.strip("#")
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex_code[i:i + 2], 16)
        rgb.append(decimal)

    return tuple(rgb)


def formatted_df(hex_dict, total_pixels):
    df = pd.DataFrame(
        {
            'Color': [f"https://www.colorhexa.com/{hex_code.strip('#')}.png" for hex_code in hex_dict.keys()],
            'Hex Code': hex_dict.keys(),
            'Percentage (%)': (np.array(list(hex_dict.values())) / total_pixels) * 100
        }
    )
    df.index += 1

    return df


def empty_df():
    return pd.DataFrame(
        {
            'Color': [],
            'Hex Code': [],
            'Percentage (%)': []
        }
    )


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_page()
