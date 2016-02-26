# -*- coding: utf-8-*-

import sys
import os
import json
import codecs
reload(sys)
sys.setdefaultencoding('utf-8')

DIR = 'G:\\FtpDir\\NEW_XIAO_APPS\\'
app_details = os.path.join(DIR,"app_details")
app_details_utf8 = os.path.join(DIR,"app_details_utf8")
app_detail_dir = os.path.join(DIR,'DETAILS')
count = 0
def desanalyser():
    global  count
    count += 1
    if not os.path.exists(app_detail_dir):
        os.mkdir(app_detail_dir)
    handler = open(app_details,"rb")
    out_handler = codecs.open(app_details_utf8,"wb","utf-8")
    for line in handler:
        lineJson = json.loads(line)
        # category = lineJson["category"]
        app_code = lineJson['app_code']
        app_file = codecs.open(os.path.join(app_detail_dir,str(app_code)),"wb","utf-8")
        app_text = lineJson['app_text']
        app_file.write(app_text)
        app_file.close()

def get_category_of_app():
    INPUT_DIR = 'G:\\FtpDir\\NEW_XIAO_APPS'
    OUT_DIR = 'G:\\FtpDir\\NEW_XIAO_APPS\\STAND'
    files = os.listdir(INPUT_DIR)
    used_id = {}
    category_id_map = {}
    for file in files:
        if file.isdigit():
            with open(os.path.join(INPUT_DIR,file),'rb') as handler:
                for line in handler:
                    lineObject = json.loads(line)
                    category_name = lineObject['level1CategoryName']
                    category_id_map[category_name] = file
                    break
    category_id = open(os.path.join(INPUT_DIR,'category_id'),'wb')
    for key,item in category_id_map.iteritems():
        category_id.write(key+':'+str(item)+'\n')
    category_id.close()
    # with open(os.path.join(INPUT_DIR,'app_details'),'rb') as handler:
    #     for line in handler:
    #         lineJson = json.loads(line)
    #         category = lineJson["category"]
    #         app_code = lineJson['app_code']
    #         if used_id.has_key(app_code): continue
    #         used_id[app_code] = 1
    #         out_handler = open(os.path.join(OUT_DIR,category_id_map[category]),'a+')
    #         out_handler.write(str(app_code)+'\n')
    #         out_handler.close()

if __name__ == '__main__':
    # desanalyser()
    # print count

    get_category_of_app()