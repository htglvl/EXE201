import pandas as pd
# import translators as ts
import argostranslate.package
import argostranslate.translate
import pickle
import pathlib
from transformers import MarianMTModel, MarianTokenizer
from typing import Sequence
from transflow.modules.utils import *

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

    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    available_package = list(
    filter(
        lambda x: x.from_code == 'ja' and x.to_code == 'en', available_packages
        )
    )[0]
    
    download_path = available_package.download()
    argostranslate.package.install_from_path(download_path)
    package_path = pathlib.Path(args.argosmodel)
    argostranslate.package.install_from_path(package_path)
    installed_languages = argostranslate.translate.get_installed_languages()
    from_lang = list(filter(
        lambda x: x.code == 'ja',
        installed_languages))[0]
    to_lang = list(filter(
        lambda x: x.code == 'vi',
        installed_languages))[0]
    translation = from_lang.get_translation(to_lang)

    for key, value in data.items():
        temp_list = []
        for key, small_value in value['bubbles'].items():
            temp_list.append(small_value['text'])
        if len(temp_list) == 0:
            continue #don't need to translate an empty list
        temp_text = "\n".join(temp_list)
        # try:
        #     trans_text = ts.translate_text(temp_text, translator = "bing", from_language = 'ja', to_language='vi')
        # except:
        #     trans_text = translation.translate(temp_text)
        print(temp_text)
        trans_text = argostranslate.translate.translate(temp_text, 'ja', 'vi')
        temp_text = ""
        trans_list = trans_text.split('\n')
        # print(trans_text)
        if len(trans_list) != len(temp_list):
            print('translate wrong', len(trans_list), len(temp_list))
            for key, small_value in value['bubbles'].items():
                small_value['trs_text'] = argostranslate.translate.translate(temp_list[key], 'ja', 'vi')
        else:
            counter = 0
            for key, small_value in value['bubbles'].items():
                small_value['trs_text'] = trans_list[counter]
                print(small_value['trs_text'])
                counter += 1
    print(f"Translation time: {time.time() - start_time:.3f}s")
    return data