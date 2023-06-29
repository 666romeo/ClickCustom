from rembg.bg import remove
from PIL import Image
from io import BytesIO
import base64

def remove_background(input_path):
    open_image = Image.open(input_path)
    open_image = open_image.resize((1400, 1400))  # Изменение размера изображения
    output = remove(open_image)

    # Замена фона на белый
    width, height = output.size
    pixels = output.load()

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                pixels[x, y] = (255, 255, 255, 255)  # Замена прозрачного пикселя на белый цвет

    # Преобразование изображения в формат Base64
    buffered = BytesIO()
    output.save(buffered, format='PNG')
    encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return encoded_image