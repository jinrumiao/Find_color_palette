from PIL import Image
import numpy as np
from sklearn.cluster import KMeans


def median_cut(image, num_colors):
    pixels = np.array(image)
    original_shape = tuple(pixels.shape)
    pixels = pixels.reshape(-1, 3)

    def cut(colors, level):
        if level == 0 or len(colors) <= num_colors:
            return colors
        max_range = np.max(colors, axis=0) - np.min(colors, axis=0)
        channel = np.argmax(max_range)
        colors = colors[colors[:, channel].argsort()]
        median_index = len(colors) // 2
        return np.concatenate((cut(colors[:median_index], level-1), cut(colors[median_index:], level-1)))

    colors = cut(pixels, np.ceil(np.log2(num_colors)))

    palette = np.array(colors, dtype=np.uint8)

    palette_image = np.reshape(palette, original_shape)

    color_palette = []
    for y in range(0, int(original_shape[0]), int(original_shape[0] // num_colors)):
        if len(color_palette) < num_colors:
            color_palette.append(palette_image[y, original_shape[0] // 2, :])

    return color_palette

    # return Image.fromarray(palette_image)


def kmeans_extraction(image, num_colors):
    pixels = np.array(image)
    original_shape = tuple(pixels.shape)
    pixels = pixels.reshape(-1, 3)

    model = KMeans(n_clusters=num_colors, n_init="auto", init="k-means++")
    model.fit_predict(pixels)
    palette = np.array(model.cluster_centers_, dtype=int)
    # print(palette)

    return palette


if __name__ == '__main__':
    image_path = "./sample_image/sample2.png"
    image = Image.open(image_path)

    num_colors = 10
    # processed_image = median_cut(image, num_colors)
    processed_image = kmeans_extraction(image, num_colors)

    color_palette_image = np.zeros((100, 100 * num_colors, 3), dtype=np.uint8)
    for i, color in enumerate(processed_image):
        color_palette_image[:, (100 * i): (100 * (i + 1)), :] = color
    image_c = Image.fromarray(color_palette_image)
    image_c.show()

    # processed_image.show()
