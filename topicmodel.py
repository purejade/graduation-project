# -*- coding: utf-8-*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import numpy as np
import itertools
import operator
import os

DETAIL_MAP={}

def get_text_topic():

    doctopic_triples = []

    mallet_docnames = []

    lineNum = 0
    with open('G:\\FtpDir\\mallet-2.0.7\\docstopics.txt ') as f:
        f.readline()
        for line in f:
            values = line.rstrip().split('\t')
            docnum,docname = values[0],values[1]
            lineNum += 1
            mallet_docnames.append(docname)
            cnt = 2
            while cnt < len(values):
                topic = values[cnt]
                share = values[cnt+1]
                cnt += 2
                triple = (docname,int(topic),float(share))
                doctopic_triples.append(triple)
            # if lineNum == 10:
            #     break

    # sort the triples
    # triple is (docname, topicnum, share) so sort(key=operator.itemgetter(0,1))
    # sorts on (docname, topicnum) which is what we want
    doctopic_triples = sorted(doctopic_triples,key=operator.itemgetter(0,1))

    # sort the document names rather than relying on MALLET's ordering
    mallet_docnames = sorted(mallet_docnames)

    # collect into a document-term matrix
    num_docs = len(mallet_docnames)

    num_topics = len(doctopic_triples) // len(mallet_docnames)

    print len(doctopic_triples)

    print num_topics

    # the following works because we know that the triples are in sequential order
    doctopic = np.zeros((num_docs,num_topics))

    for triple in doctopic_triples:
        docname,topic,share = triple
        row_num = mallet_docnames.index(docname)
        doctopic[row_num,topic] = share

    # print doctopic
    print "Top topics in ..."

    OUT_DIR = 'G:\\FtpDir\\NEW_XIAO_APPS\\RESULT\\'

    for i in range(len(doctopic)):
        top_topics = np.argsort(doctopic[i,:])[::-1][0:4]
        top_topics_str = ' '.join(str(t) for t in top_topics)
        top_topics_share = ' '.join(str(round(doctopic[i][share]*100,4)) for share in top_topics)
        # print "{} : {} : {}".format(mallet_docnames[i],top_topics_str,top_topics_share)
        filename = mallet_docnames[i][mallet_docnames[i].rfind('/')+1:]
        print filename + ' is over!'
        topics_array = []
        for topic in top_topics:
            if doctopic[i][topic] - doctopic[i][top_topics[0]] < 1:
                topics_array.append(topic);
        for topic in topics_array:
            handler = open(os.path.join(OUT_DIR,str(topic)),'a+')
            handler.write(filename+'\n')
            handler.close()




# if the novel is divided into several parts, we need  emerge them together.
# print doctopic
# novel_names = []
#
# for fn in mallet_docnames:
#     basename = os.path.basename(fn)
#     name, ext = os.path.splitext(basename)
#     name = name.rstrip()
#     novel_names.append(name)
# # turn this into an array so we can use NumPy functions
# novel_names = np.asarray(novel_names)
#
# # use method described in preprocessing section
# num_groups = len(set(novel_names))
#
# doctopic_grouped = np.zeros((num_groups, num_topics))
#
# for i, name in enumerate(sorted(set(novel_names))):
#     doctopic_grouped[i, :] = np.mean(doctopic[novel_names == name, :], axis=0)
#     print doctopic_grouped[i,:]
#
# doctopic = doctopic_grouped
# print doctopic

# 无法应用到中文上，可能需要语料库
def get_topic_words(keys_file=None):

    with open('G:\\FtpDir\\mallet-2.0.7\\docstopics-key.txt') as input:
        topic_keys_line = input.readlines()

    topic_words = []
    for line in topic_keys_line:
        _,_, words = line.split('\t')
        words = words.rstrip(' ')
        topic_words.append(words)

    print topic_words[0]

def get_distance(array1,array2) :
    # array1 = np.array(list1)
    # array2 = np.array(list2)
    return np.linalg.norm(array1-array2)


def init_data(list1,ids_map):
    global  DETAIL_MAP
    array = np.zeros(15000)
    for ele in list1:
        # if DETAIL_MAP.has_key(ele):
        if ele in ids_map:
            array[ids_map[ele]] = 1  # details and app_id are differnet, and detail_ids is more than the app_ids
        # else:
        #     print "lost :" + ele
    return array



def get_nearest_topic(ids_map):

    INPUT_DIR = 'G:\\FtpDir\\NEW_XIAO_APPS\\RESULT\\'
    STAND_DIR = 'G:\\FtpDir\\NEW_XIAO_APPS\\STAND'
    stand_files = os.listdir(STAND_DIR)
    filenames = os.listdir(INPUT_DIR)
    result = np.zeros((29,29))
    topic_result = open(os.path.join(INPUT_DIR,'topic_result'),'wb')
    for file in filenames:
        file_handler = open(os.path.join(INPUT_DIR,file),'rb')
        content = file_handler.read()
        name_ids =  content.split()
        max_index = -1
        max_count = 0
        name_ids_array = init_data(name_ids,ids_map)
        for stand in stand_files:
            stand_handler = open(os.path.join(STAND_DIR,stand),'rb')
            stand_ids = stand_handler.read().split()
            stand_ids_array = init_data(stand_ids,ids_map)
            similar = get_distance(name_ids_array,stand_ids_array)
            # for id in name_ids:
            #     if id in stand_ids:
            #         count += 1
            if similar > max_count:
                max_count = similar
                max_index = stand

        #     result[file][int(stand)-1] = int(count)
        print "the " + str(file) + " topic is : " + str(max_index)
        topic_result.write("the " + str(file) + " topic is : " + str(max_index)+'\n')
    topic_result.close()

def get_details_map():
    global  DETAIL_MAP
    INPUT_DIR = 'G:\\FtpDir\\NEW_XIAO_APPS\\DETAILS'
    files = os.listdir(INPUT_DIR)
    count = 0
    for file in files:
        line = line.rstrip()
        DETAIL_MAP[file] = count
        count += 1
    return ids_map
    # print result

def map_id():
    global  DETAIL_MAP
    INPUT_DIR = 'G:\\FtpDir\\NEW_XIAO_APPS\\RESULT'
    files = os.listdir(INPUT_DIR)
    ids_map = {}
    count = 0
    for file in files:
        with open(os.path.join('G:\\FtpDir\\NEW_XIAO_APPS\\',file),'rb') as handler:
            for line in handler:
                line = line.strip()
                if not line: continue
                if ids_map.has_key(line): continue  # 一个应用可能属于2-3个topic
                ids_map[line] = count
                count += 1
    print count
    return ids_map

if __name__ == '__main__':

    # get_topic_words()
    # get_text_topic()
    ids_map = map_id()
    get_nearest_topic(ids_map)