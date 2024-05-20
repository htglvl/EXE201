import os
import cv2
from PIL import Image
import pickle

import numpy as np

from ultralytics import YOLO

def simple_remove(image_rgb, binary_mask):
    # Replace the segment area with white color
    image_rgb[binary_mask == 1] = [255, 255, 255]
    return image_rgb
