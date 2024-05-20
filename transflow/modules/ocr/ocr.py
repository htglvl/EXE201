import os
from PIL import Image
import pickle

from manga_ocr import MangaOcr
# import paddleocr
from transflow.modules.utils import *

import warnings
warnings.filterwarnings("ignore")

def get_text_from_bubble(args, ocr_model, dt_output): 
    '''
    OCR to get the text from the input bubble

    Args:
    ocr_language(str) : user define specific language to ocr from
    the_bubble_output(nested_dict): the output from bubble_text_detector.py

    Return:
    {
    'img_0': {
        'img': original image path,
        'rm_img': removed text image path,
        'bubbles': {
            'bubble_0': {
                'coord': (x1, y1, x2, y2),
                'text': text from the bubble,
                },
            ...
            },
        },
    ...
    }
    '''
    start_time = time.time()
    # Load from output.pkl (which is a nested dict by itself)
    if dt_output:
        nested_data = dt_output
    else:
        bubble_pkl_output = os.path.join(args.output, 'output_dt.pkl') 
        if bubble_pkl_output.endswith('.pkl'):
            with open(bubble_pkl_output, 'rb') as file:
                nested_data = pickle.load(file)
    
    #TODO: implement if it load directly
    # # Load directly from the output (which is a nested dict by itself)
    # nested_data = the_bubble_output

    # # Get ocr model based on the ocr_language user choose
    # ocr_model = get_OCR_model(ocr_language)

    # Get info from the nested_data
    for k, value in nested_data.items():
        image_path = value['img']         # relative image path (images should be in a folder and that image folder should be put in the dataset folder [just create the dataset folder in the transflow folder by yourself cuz idk why Khanh not do it])
        full_image = Image.open(image_path)
        for bk, bubb_value in value['bubbles'].items():
            bubble_coordinate = bubb_value['coord'] # tuple vd: (1458, 313, 1598, 589)
            bubble_image = crop_image(image=full_image,
                                      coordinates=bubble_coordinate)
            text = ocr_model(bubble_image)
            bubb_value['text'] = text

    # dump to .pkl
    if args.save_ocr_output:
        pkl_path = os.path.join(args.output, 'output_ocr.pkl')
        with open(pkl_path, 'wb') as file:
            pickle.dump(nested_data, file)
        
    print(f'OCR time: {round(time.time() - start_time, 3)}s')    
    return nested_data

# x = get_text_from_bubble('jp', '/home/doki/Code_workspace/EXE_project/transflow/TEST/output.pkl')
# print(x)         



            

