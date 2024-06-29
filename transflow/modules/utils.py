# IMPORT
import argparse
import time
import os
import pickle
from pathlib import Path

from PIL import Image
import cv2

from ultralytics import YOLO
from manga_ocr import MangaOcr
from paddleocr import PaddleOCR

import warnings
warnings.filterwarnings("ignore")


# Get parser function
def get_parser():
    parser = argparse.ArgumentParser(description='Detect bubble text')
    # General options
    parser.add_argument('--image', type=str, help='path to image or image folder')
    parser.add_argument('--output', type=str, default='', help='path to save the output')
    parser.add_argument('--device', type=str, default='cpu', help='device to use (cpu, cuda:0, cuda:1, ...)')

    # Render options
    parser.add_argument('--font-path', type=str, default='transflow/fonts/AndikaNewBasic-B.ttf', help='path to font file')
    parser.add_argument('--font-size', type=int, default='50', help='init font size')
    parser.add_argument('--align', type=str, default='center', help='text alignment: left, center, right')
    parser.add_argument('--colour', type=str, default='#000', help='text colour')

    # YOLO detect options
    parser.add_argument('--dt-weight', type=str, default='transflow/checkpoints/comic-speech-bubble-detector.pt', help='path to pretrained weight')
    parser.add_argument('--conf', type=float, default=0.25, help='confidence threshold')
    parser.add_argument('--iou', type=float, default=0.7, help='IoU threshold')
    parser.add_argument('--save-crop', action='store_true', help='save crop bubble text')
    parser.add_argument('--save-dt-output', action='store_true', help='save output of detection')

    # YOLO segment options
    parser.add_argument('--sg-weight', type=str, default='transflow/checkpoints/comic-text-segmenter.pt', help='path to pretrained weight')

    #argos translator
    parser.add_argument('--argosmodel', type=str, default='transflow/checkpoints/translate-en_vi-1_2.argosmodel', help='path to pretrained weight')
    
    # OCR options
    parser.add_argument('--ocr-lang', type=str, default='jp', help="language to OCR from ['jp', 'cn', 'kr', 'en']")
    parser.add_argument('--save-ocr-output', action='store_true', help='save output of OCR')

    # Segment options
    return parser

# Get model
def get_model(args):
    '''
    Load the YOLO model
    Args:
        weight: path to the pretrained weight
    Returns:
        model: YOLO model    
    '''
    # Get YOLO detector model
    # dt_model = YOLO(args.dt_weight, task='detect')
    # Get YOLO segment model
    sg_model = YOLO(args.sg_weight, task='segment')

    # Get OCR model
    lang_abbrv = ['jp', 'cn', 'kr', 'en']
    lang_full = ['japan', 'china', 'korea', 'english']

    # Get model according to the language
    if args.ocr_lang.lower() in lang_abbrv or lang_full:
        if args.ocr_lang == 'jp' or args.ocr_lang == 'japan':
            ocr_model = MangaOcr()
        elif args.ocr_lang == 'cn' or args.ocr_lang == 'china':
            # model = PaddleOCR(with china in mind)
            raise NotImplementedError 
        elif args.ocr_lang == 'kr' or args.ocr_lang == 'korea':
            # model = PaddleOCR(with korea in mind)
            raise NotImplementedError
        elif args.ocr_lang == 'en' or args.ocr_lang == 'english':
            ocr_model = PaddleOCR(lang='en', use_gpu=False)
    else:
        print("The language you want have NOT been implemented yet, stay tune for future update")
        raise NotImplementedError
    return ocr_model, sg_model

# Utils
def crop_image(image, coordinates):
    '''
    Args:
        image(PIL.Image): input image
        coordinates(tuple): coordinates to crop the image
    Return:
        cropped_img(PIL.Image): cropped image
    '''
    # cropped_img = image.crop(coordinates)
    cropped_img = image[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]]
    return cropped_img

def convert_xyxy_to_xywh(xyxy_box):
    x1, y1, x2, y2 = xyxy_box
    x = x1
    y = y1
    width = x2 - x1
    height = y2 - y1
    return x, y, width, height

def extract_strings(nested):
    strings = []
    for item in nested:
        if isinstance(item, list):
            strings.extend(extract_strings(item))
        elif isinstance(item, tuple) and isinstance(item[0], str):
            strings.append(item[0])
    return strings