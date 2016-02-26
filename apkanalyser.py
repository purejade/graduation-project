# -*- coding: utf-8-*-

import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')
import subprocess
import shutil
from analysermanifest import parser_manifest

def apk_decompiler(apkname):
    apkrealname = apkname
    try:
        if os.path.exists('tst'):
            rmdir('tst')
        outdir = 'tst'
        result = subprocess.check_output('apktool.bat d ' + apkrealname + ' ' + outdir,shell=True)
    except Exception as e:
        print str(e)
        return
    parser_manifest(outdir+os.sep+'AndroidManifest.xml')
    try:
        result = subprocess.check_output('apktool.bat b ' + outdir +' unsigned_' + apkname,shell=True)
    except Exception as e:
        print str(e)
        return
    retval = subprocess.call('signapk.bat ' + 'unsigned_'+apkname + ' signed_'+ apkname)
    if retval == 0:
        print '>>> signed done <<<'
    else:
        print '!!! signed error !!!'

def rmfile(filepath):
    os.remove(filepath)
    pass

def rmdir(dirpath):
    shutil.rmtree(dirpath)
    pass

if __name__ == '__main__':
    apkname = 'com.quiz.twd.main.apk'
    apk_decompiler(apkname)
    # rmdir('tst')
    # rmfile('unsigned_com.quiz.twd.main.apk')