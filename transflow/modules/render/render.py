from PIL import Image, ImageFont, ImageDraw
import cv2
import numpy as np
from typing import Tuple, List
from transflow.modules.render.hyphen_textwrap import wrap as hyphen_wrap
from transflow.modules.render.textblock import TextBlock
from transflow.modules.utils import *

def cv2_to_pil(cv2_image: np.ndarray):
    # Convert color channels from BGR to RGB
    rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    # Convert the NumPy array to a PIL Image
    pil_image = Image.fromarray(rgb_image)
    return pil_image

def pil_to_cv2(pil_image: Image):
    # Convert the PIL image to a numpy array
    numpy_image = np.array(pil_image)
    
    # PIL images are in RGB by default, OpenCV uses BGR, so convert the color space
    cv2_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
    
    return cv2_image

def pil_word_wrap(image: Image, tbbox_top_left: Tuple, font_pth: str, init_font_size, text: str, roi_width, roi_height, align: str, spacing):
    """Break long text to multiple lines, and reduce point size
    until all text fits within a bounding box."""
    mutable_message = text
    font_size = init_font_size
    font = ImageFont.truetype(font_pth, font_size)

    def eval_metrics(txt, font):
        """Quick helper function to calculate width/height of text."""
        (left, top, right, bottom) = ImageDraw.Draw(image).multiline_textbbox(xy=tbbox_top_left, text=txt, font=font, align=align, spacing=spacing)
        return (right-left, bottom-top)

    while font_size > 1:
        font = font.font_variant(size=font_size)
        width, height = eval_metrics(mutable_message, font)
        if height > roi_height:
            font_size -= 1  # Reduce pointsize
            mutable_message = text  # Restore original text
        elif width > roi_width:
            columns = len(mutable_message)
            while columns > 0:
                columns -= 1
                if columns == 0:
                    break
                mutable_message = '\n'.join(hyphen_wrap(text, columns, break_on_hyphens=False, break_long_words=False, hyphenate_broken_words=True)) 
                wrapped_width, _ = eval_metrics(mutable_message, font)
                if wrapped_width <= roi_width:
                    break
            if columns < 1:
                font_size -= 1  # Reduce pointsize
                mutable_message = text  # Restore original text
        else:
            break

    return mutable_message, font_size

def draw_text(image: np.ndarray, coord_list: list, text_list: list, font_pth: str, init_font_size: int, align: str, colour: str):
    image = cv2_to_pil(image)
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(font_pth, size=init_font_size)

    for i in range(len(coord_list)):
        x1, y1, width, height = convert_xyxy_to_xywh(coord_list[i])
        tbbox_top_left = (x1, y1)

        translation = text_list[i]
        if not translation or len(translation) == 1:
            continue
        
        translation, font_size = pil_word_wrap(image, tbbox_top_left, font_pth, init_font_size, translation, width, height, align, 4)
        font = font.font_variant(size=font_size)
        
        draw.multiline_text(tbbox_top_left, translation, colour, font, align=align, spacing=1)
    image = pil_to_cv2(image)
    return image

def render(args, trs_output: dict):
    start_time = time.time()
    for i in range(len(trs_output)):
        image_dict = trs_output[i]
        image_path = image_dict['rm_img']
        image = cv2.imread(image_path)
        coord_list = []
        text_list = []
        for k, v in image_dict['bubbles'].items():
            coord_list.append(v['coord'])
            text_list.append(v['trs_text'])
        image = draw_text(image, coord_list, text_list, args.font_path, args.font_size, args.align, args.colour)

        output_folder = os.path.join(args.output, 'final')
        os.makedirs(output_folder, exist_ok=True)
        cv2.imwrite(f"{output_folder}/{image_path.split('/')[-1]}", image)
    print(f"Rendering time: {time.time() - start_time:.3f}s")



