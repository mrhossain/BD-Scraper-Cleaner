from os import listdir, mkdir, makedirs
from os.path import *
from difflib import SequenceMatcher
from shutil import copyfile, move, rmtree
import io

import os

import sys


import re






def cleanbl():

    test_files = {}
    dir_path = '/mnt/4248075B48074CDB/ICO-2020/6-class-text-classification/train/Sports'
    for f in listdir(dir_path):
        file_path = join(dir_path, f)
        if not isfile(file_path):
            continue
        print(file_path)
        size = os.path.getsize(file_path)
        size = size/1024

        text = ""
        with open(file_path,"r") as f:
            text = f.read()
            #print(text)
            text = str(text).replace('।', '\n')

            whitespace = re.compile(u"[\s\u0020\u00a0\u1680\u180e\u202f\u205f\u3000\u2000-\u200a]+", re.UNICODE)
            bangla_fullstop = u"\u0964"
            punctSeq = u"['\"“”‘’]+|[.?!,…]+|[:;]+"
            punc = u"[(),$%^&*+={}\[\]:\"|\'\~`<>/,¦!?½£¶¼©⅐⅑⅒⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞⅟↉¤¿º;-]+"
            text = whitespace.sub(" ", text).strip()
            text = re.sub(punctSeq, " ", text)
            text = re.sub(bangla_fullstop, " ", text)
            text = re.sub(punc, " ", text)
            text = text.split(None, 1)[1]
            f.close()
            with open(file_path, "w") as fs:
                fs.write(text)
                fs.close()
if __name__ == "__main__":
    cleanbl()