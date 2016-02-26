# -*- coding: utf-8-*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import re

def parser_manifest(manifest):
    removed__permission_set = ('android.permission.READ_SMS')
    with open(manifest,'rb') as handler:
        # cnt = 1
        # for line in handler:
        #     print str(cnt) + '---' +  line
        #     cnt += 1
        content = handler.read()
        content = re.sub(r'android.permission.ACCESS_NETWORK_STATE','',content)
        print content
        open(manifest,'wb').write(content)

if __name__ == '__main__':

    parser_manifest('.\\tst\\AndroidManifest.xml')