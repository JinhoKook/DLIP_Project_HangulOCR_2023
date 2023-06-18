import numpy as np
from PIL import Image
import cairo
import matplotlib.font_manager as fm
import os

FONT_LIST = [f.name for f in fm.fontManager.ttflist]
FONT_LIST = list(set([f for f in FONT_LIST if "Nanum" in f ]))

# env = PY39


def paint_text(text, max_word=None, font_size=28, color_noise=(0.,0.01), random_shift=False, font_list=FONT_LIST):
    '''
    Text가 그려진 이미지를 만드는 함수
    '''
    if max_word is None:
        # None이면, text의 word 갯수에 맞춰서 생성
        max_word = len(text)
    h = font_size + 12  # 이미지 높이, font_size + padding
    w = font_size * (1 + max_word) + 12  # 이미지 폭

    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
    context = cairo.Context(surface)
    context.set_source_rgb(1, 1, 1)  # White
    context.paint()

    # Font Style : Random Pick
    context.select_font_face(
        np.random.choice(font_list),
        cairo.FONT_SLANT_NORMAL,
        np.random.choice([cairo.FONT_WEIGHT_BOLD, cairo.FONT_WEIGHT_NORMAL]))

    context.set_font_size(font_size)
    box = context.text_extents(text)
    border_w_h = (4, 4)
    if box[2] > (w - 2 * border_w_h[1]) or box[3] > (h - 2 * border_w_h[0]):
        raise IOError(('Could not fit string into image.'
                       'Max char count is too large for given image width.'))

    # Random Shift을 통해, 이미지 Augmentation
    max_shift_x = w - box[2] - border_w_h[0]
    max_shift_y = h - box[3] - border_w_h[1]

    if random_shift:
        top_left_x = np.random.randint(0, int(max_shift_x))
        top_left_y = np.random.randint(0, int(max_shift_y))
    else:
        top_left_x = np.random.randint(3, 10) # Default padding
        top_left_y = int(max_shift_y)//2 # Default position = center in heights

    context.move_to(top_left_x - int(box[0]),
                    top_left_y - int(box[1]))

    # Draw Text
    rgb = np.random.uniform(*color_noise, size=3)

    context.set_source_rgb(*rgb)
    context.show_text(text)

    # cairo data format to numpy data format
    buf = surface.get_data()
    text_image = np.frombuffer(buf, np.uint8)
    text_image = text_image.reshape(h, w, 4)
    text_image = text_image[:, :, :3]
    text_image = text_image.astype(np.float32) / 255

    return text_image



def generate_word_images(words):
    # 폴더가 존재하지 않을 경우 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for word in words:
        # 이미지 생성
        image = paint_text(word)
        image_path = os.path.join(output_folder, f"{word}.jpg")

        # 이미지 저장
        Image.fromarray((image * 255).astype(np.uint8)).save(image_path)
        print(f"The image with the word '{word}' has been saved as '{image_path}'.")

# 이미지로 변환할 단어들
words = ["안녕", "세상", "Hello", "World"]

# 이미지가 저장될 폴더 경로
output_folder = "words_for_test"

# 단어 이미지 생성 및 저장
generate_word_images(words)









