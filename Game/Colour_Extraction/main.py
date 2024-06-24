import colorgram

def image_color_extractor(image_file: str, colors_to_extract: int=1_000_000):
    colors = colorgram.extract(image_file, colors_to_extract)
    rgb_colors = []
    for color in colors:
        r = color.rgb.r
        g = color.rgb.g
        b = color.rgb.b
        rgb_colors.append((r, g, b))
    return rgb_colors

if __name__ == '__main__':
    print(image_color_extractor('image.jpg'))