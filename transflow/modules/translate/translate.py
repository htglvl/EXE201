import pandas as pd
# import translators as ts
import argostranslate.package
import argostranslate.translate
import pickle
import pathlib
from transformers import MarianMTModel, MarianTokenizer
from typing import Sequence
from transflow.modules.utils import *
import anthropic

def translate_claude(text, from_lang, to_lang='Vietnamese'):
    if from_lang == 'en' or from_lang == 'english':
        from_lang = 'English'
    elif from_lang == 'jp' or from_lang == 'japanese':
        from_lang = 'Japanese'
    elif from_lang == 'kr' or from_lang == 'korea':
        from_lang = 'korea'
    elif from_lang == 'cn' or from_lang == 'chinese':
        from_lang = 'Chinese'

    client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="",
    )
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": f'''Translate the comic dialog from {from_lang} into {to_lang}, Present only the translated text, without any additional formatting or surrounding text: {text}'''}
        ]
    )
    return message.content[0].text

def translate(args, data):
    '''
    Return:
        {
        'img_0': {
            'img': original image path,
            'rm_img': removed text image path,
            'bubbles': {
                'bubble_0': {
                    'coord': (x1, y1, x2, y2),
                    'text': text from the bubble,
                    'trs_text': translated text,
                    },
                ...
                },
            },
        ...
        }
    '''
    start_time = time.time()

    for key, value in data.items():
        temp_list = []
        for key, small_value in value['bubbles'].items():
            temp_list.append(small_value['text'])
        if len(temp_list) == 0:
            continue #don't need to translate an empty list
        temp_text = "\n".join(temp_list)
        trans_text =translate_claude(temp_text, args.ocr_lang)
        temp_text = ""
        trans_list = trans_text.split('\n')
        # print(trans_text)
        if len(trans_list) != len(temp_list):
            print('translate wrong', len(trans_list), len(temp_list))
            for key, small_value in value['bubbles'].items():
                small_value['trs_text'] = translate_claude(temp_list[key], args.ocr_lang)
        else:
            counter = 0
            for key, small_value in value['bubbles'].items():
                small_value['trs_text'] = trans_list[counter]
                print(small_value['trs_text'])
                counter += 1
    print(f"Translation time: {time.time() - start_time:.3f}s")
    return data