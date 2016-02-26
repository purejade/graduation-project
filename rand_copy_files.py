# -*- coding: utf-8-*-

import sys
import os
import random
import shutil
reload(sys)
sys.setdefaultencoding('utf-8')

seg_words_dir = 'G:\\FtpDir\\NEW_XIAO_APPS\\SEG_WORDS'
rand_file_dir = 'G:\\FtpDir\\NEW_XIAO_APPS\\TEST_DATA_SET'

def rand_copy_files(count):
    files = os.listdir(seg_words_dir)
    filenames = []
    for file in files:
        filenames.append(file)
    datas = {}
    cnt = 1

    while cnt < count:
        number = random.randint(1,20000)
        if number >= len(filenames): continue
        number = filenames[number]
        if number in datas:
            continue
        datas[number] = 1
        src = os.path.join(seg_words_dir,str(number))
        dst = os.path.join(rand_file_dir,str(number))
        if os.path.exists(src):
            shutil.move(src,dst)
            cnt += 1

if __name__ == '__main__':
    count = 4000
    rand_copy_files(count)
