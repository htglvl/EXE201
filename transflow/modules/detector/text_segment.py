import os
import cv2
from PIL import Image
import pickle
import time

import numpy as np

from ultralytics import YOLO
from transflow.modules.render.remove_text import *

def segment_text(args, sg_model=None):
    '''
    Detect text in image and remove it
    Args:
        args: argument parser
        sg_model: YOLO model for segmentation
    Returns:
        output_dict: detection information
            {
            'img_0': {
                'img': original image path,
                'rm_img': removed text image path,
                'bubbles': {
                    'bubble_0': {
                        'coord': (x1, y1, x2, y2),
                        },
                    ...
                    },
                },
            ...
            }
    '''
    start_time = time.time()
    # Load the model
    if sg_model:
        sg_model = sg_model
    else:
        sg_model = YOLO(args.sg_weight, task='segment')

    # Perform prediction
    results = sg_model.predict(source=args.image, device=args.device) 
    output_dict = dict() # Save the detection information
    
    # Visualize the segmentation masks and draw bounding boxes
    for i, result in enumerate(results):
        bubble_dict = dict() # save bubble text information

        # Load the image using OpenCV
        image_path = result.path
        re_image_path = image_path.replace(os.getcwd() + '/', '') # convert to relative path
        original_image = cv2.imread(image_path)
        # Ensure the image is in the correct format (BGR to RGB)
        image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

        # Loop through each segmentation result
        if result.masks:
            for mask in result.masks:
                # Convert the mask to a binary mask
                binary_mask = mask.data.cpu().numpy().astype(np.uint8)
                
                # Ensure the binary_mask is 2D
                if binary_mask.ndim == 3:
                    binary_mask = binary_mask.squeeze(0)
                
                # Resize the binary mask to match the original image size
                binary_mask = cv2.resize(binary_mask, (original_image.shape[1], original_image.shape[0]), interpolation=cv2.INTER_NEAREST)
                
                # Replace the segment area with white color
                image_rgb = simple_remove(image_rgb, binary_mask)
        # Save removed text image
        os.makedirs(f'{args.output}/removed', exist_ok=True)
        # Convert the image back to BGR format for OpenCV
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        cv2.imwrite(f'{args.output}/removed/{re_image_path.split("/")[-1]}', image_bgr)

        # Loop through each bounding box result
        for j, box in enumerate(result.boxes):
            # Extract box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
            bubble_dict[j] = {'coord':(x1, y1, x2, y2)}
            
            # Draw the bounding box on the image
            # cv2.rectangle(image_rgb, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green box with thickness 2
        # Get all information
        output_dict[i] = {
            # 'img': result.orig_img,
            'img': re_image_path,
            'rm_img': f'{args.output}/removed/{re_image_path.split("/")[-1]}',
            'bubbles': bubble_dict
        }
    print(f"Segmentation time: {round(time.time() - start_time, 3)}s")

    return output_dict


