# -*- coding: utf-8-*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import pprint
__author__ = 'purejade'

import os

import nltk
import re
import time
from nltk.corpus import wordnet as wn

INPUT_DIR = 'G:\\FtpDir\\RESULT\\PLAY_APP\\DESCRIPTION\\'

OUT_DIR = 'C:\\Users\\purejade\\AppData\\Roaming\\nltk_data\\corpora\\gutenberg\\'

MOD_DES = 'G:\\FtpDir\\RESULT\\PLAY_APP\\MODDES\\'

def static_words():
    WORD_MAP={}
    files = os.listdir(MOD_DES)
    for file in files:
        filename = os.path.join(MOD_DES,file)
        handler = open(filename,'rb')
        content = handler.read()
        pattern = r'''
            (?x)    # set flag to allow verbose regexps
             [[A-Z]\.]+        # abbreviations, e.g. U.S.A.
           | \w+[-\w+]*        # words with optional internal hyphens
           | \$?\d+[\.\d+]?%?  # currency and percentages, e.g. $12.40, 82%
           | \.\.\.            # ellipsis
           | [][.,;"'?():-_`]  # these are separate tokens
           '''
        words = re.findall(pattern,content)
        for word in words:
            word = word.strip()
            if word:
                check = wn.synsets(word)
                if check:
                    WORD_MAP[word] = WORD_MAP.get(word,0) + 1
        handler.close()
    with open('word_count.txt','wb') as handler:
        for key,value in WORD_MAP.iteritems():
            handler.write(key+'|'+str(value)+os.linesep)

def precessor_text():
    time_file_handler = open('time.txt','a+')
    files = os.listdir(INPUT_DIR)
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    total_start = time.clock()
    lost_file_handler = open('lost.txt','a+')

    for file in files:
        start = time.clock()
        filename = os.path.join(INPUT_DIR,file)
        desfile = os.path.join(OUT_DIR,file)
        handler = open(filename,'rb')
        content  = handler.read()
        content = content[content.find(os.linesep)+1:]
        open(desfile,'wb').write(content)
        handler = open(desfile,'rb')
        content = handler.read()
        pattern = r'''
            (?x)    # set flag to allow verbose regexps
             [[A-Z]\.]+        # abbreviations, e.g. U.S.A.
           | \w+[-\w+]*        # words with optional internal hyphens
           | \$?\d+[\.\d+]?%?  # currency and percentages, e.g. $12.40, 82%
           | \.\.\.            # ellipsis
           | [][.,;"'?():-_`]  # these are separate tokens
           '''
        words = re.findall(pattern,content)
        count = 0
        not_word = 0
        for word in words:
            word = word.strip()
            if word:
                count += 1
                check = wn.synsets(word)
                if not check:
                    not_word += 1
        if not_word > count/2:
            lost_file_handler.write(file+os.linesep)
            print 'current text not english text'
            continue

        text = nltk.corpus.gutenberg.raw(file)
        sents = sent_tokenizer.tokenize(text)
        res_list=[]
        out_handler = open(os.path.join(MOD_DES,file),'wb')
        for sent in sents:
            sent = sent.strip()
            sent = sent.strip('*')
            if sent.split('-') > 3:
                for item in sent.split('-'):
                    out_handler.write(item+os.linesep)
            elif sent.split('*') >  3:
                for item in sent.split('*'):
                    out_handler.write(item+os.linesep)
            elif sent.split('>') >  3:
                for item in sent.split('>'):
                    out_handler.write(item+os.linesep)
            elif sent.split(',') > 4:
                for item in sent.split(','):
                    out_handler.write(item+os.linesep)
            else:
                out_handler.write(sent+os.linesep)
        out_handler.close()
        handler.close()
        time_file_handler.write(str(time.clock() - start))
        time_file_handler.write(os.linesep)
        os.remove(desfile)  # throw a exception if the file is using
        # break

    total_end = time.clock()

    print total_end - total_start

    time_file_handler.write("**************")
    time_file_handler.write(str(total_end - total_start))
    time_file_handler.write(os.linesep)

    lost_file_handler.close()
    time_file_handler.close()

def seg_sent(sent):
    pattern = r'''
        (?x)    # set flag to allow verbose regexps
         [[A-Z]\.]+        # abbreviations, e.g. U.S.A.
       | \w+[-\w+]*        # words with optional internal hyphens
       | \$?\d+[\.\d+]?%?  # currency and percentages, e.g. $12.40, 82%
       | \.\.\.            # ellipsis
       | [][.,;"'?():-_`]  # these are separate tokens
       '''
    words = re.findall(pattern,sent)
    return words

# 基于关键字匹配的方法来查看是否需要短信权限
def search_keywords():
    #sms
    sms_set = ("display", "view", "read", "access", "send","receive", "share", "search")
    sms_nouns = ("text","message", "text message", "IM", "text","messages")
    files = os.listdir(MOD_DES)
    sms_set_map = {}
    for item in sms_set:
        sms_set_map[item] = 1
    sms_nouns_map = {}
    for item in sms_nouns:
        sms_nouns_map[item] = 1
    sms_handler = open('sms_result','wb')
    sms_lost_handler = open('sms_only_key','wb')
    for file in files:
        print file
        filename = os.path.join(MOD_DES,file)
        handler = open(filename,'rb')
        for line in handler:
            line = line.lower()
            words = seg_sent(line)
            flag = False
            for word in words:
                word = word.strip()
                if word:
                    check = wn.synsets(word)
                    if check:
                        if sms_nouns_map.has_key(word):
                            if flag:
                               print 'ok'
                               sms_handler.write(file+'|'+line+os.linesep)
                               break
                            else:
                                # print line
                                sms_lost_handler.write(file+'|'+line+os.linesep)
                        if sms_set_map.has_key(word):
                            flag = True
        handler.close()
    sms_handler.close()
    sms_lost_handler.close()


if __name__ == '__main__':
    # static_words()
    #  search_keywords()
    pass