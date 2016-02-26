#!/usr/bin/env python
# -*- utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
# import urllib2
import HTMLParser
import re
permissions = ['READ_SMS','READ_CONTACTS', 'READ_CALENDAR']

ORIG_DES = 'G:\\FtpDir\\RESULT\\PLAY_APP\\MODDES\\'

def get_des_from_perm():
    for permission in permissions:
        if not os.path.exists('./'+permission):
            os.mkdir(permission)
        with open(permission+'.txt','rb') as handler:
            line = handler.read()
            lines = line.split('\r')
            for line in lines:
                line = line.strip()
                if line:
                    if os.path.exists(ORIG_DES+line):
                        open(permission+'\\'+line,'wb').write(open(ORIG_DES+line,'rb').read())
                    else:
                        print permission + '|' + line
                        open(permission+'.lost','a+').write(line+os.linesep)


                    # print line
        # break

# get_des_from_perm()

# html_parser = HTMLParser.HTMLParser()
# p = re.compile(r'\\u[\d\w]{4}')
# for permission in permissions:
#     f = open(permission+'.des','wb')
#     with open(permission,'rb') as handler:
#         for line in handler:
#             line = line.strip()
#             if line:
#                 infos = line.split('|')
#                 info = html_parser.unescape(infos[1])
#                 info = info.strip('"')
#                 info = re.sub(p,'',info)
#                 len = 0
#                 for c in info:
#                     if c.isalpha():
#                         len += 1
#                 if len < 50:
#                     info = '*******'
#                 f.write(info)
#                 f.write(os.linesep)
#     f.close()

# """
#         ("'", '&#39;'), ('"', '&quot;'),
#             ('>', '&gt;'),
#             ('<', '&lt;'),
#             ('&', '&amp;')
#         ):
# """

# pattern = r'''
#       (?x)    # set flag to allow verbose regexps
# 	     ([A-Z]\.)+        # abbreviations, e.g. U.S.A.
# 	   | \w+(-\w+)*        # words with optional internal hyphens
# 	   | \$?\d+(\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
# 	   | \.\.\.            # ellipsis
# 	   | [][.,;"'?():-_`]  # these are separate tokens
# 	   '''
# flag = True
# for permission in permissions:
#     with  open(permission+'.des','rb') as handler:
#         for line in handler:
#             line = line.strip()
#             if line and flag:
#                 print line
#                 flag = False
#                 print re.findall(pattern,line)
#             break
#     break

