__author__ = 'purejade'

import os

import subprocess

import time

# aapt dump permissions com.makem.makem_01_44.apk


OUT_DIR = 'G:'+os.sep+'FtpDir'+os.sep+'RESULT'+os.sep+'XIAO_APP'+os.sep+'PERMISSIONS'+os.sep

TOTAL_OUT_DIR = 'G:'+os.sep+'FtpDir'+os.sep+'RESULT'+os.sep+'XIAO_APP'+os.sep

time_file_name = os.path.join(TOTAL_OUT_DIR,'time')

time_file = open(time_file_name,'a+')

stat_file_name = os.path.join(TOTAL_OUT_DIR,'stat')

sorted_stat_file_name = os.path.join(TOTAL_OUT_DIR,'sorted_stat')

stat_file = open(stat_file_name,'a+')

failed_file = open( os.path.join(TOTAL_OUT_DIR,'fail'),'a+')

succ_file = open( os.path.join(TOTAL_OUT_DIR,'succ'),'a+')


PERMISSION_FREQ={}

SUCC_MAP = {}
total_time = 0
total_num = 0

def get_permissions_from_pkg(permission_infos,filename):

    filename = filename[0:filename.rfind('.')]  # com.cn.name.pkg
    output_file_name = os.path.join(OUT_DIR,filename)
    output_file = open(output_file_name,'wb')
    output_file.write(permission_infos)
    output_file.close()
    infos = permission_infos.splitlines()
    for info in infos:
        if info.startswith('uses-permission'):
            permission = info.split(':')[1]
            PERMISSION_FREQ[permission] = PERMISSION_FREQ.get(permission,0) + 1
    # pass

def get_all_permissions(dirs):
    global  total_time,total_num
    if os.path.exists(dirs):
        if os.path.isdir(dirs):
            filenames = os.listdir(dirs)
            abs_dirs = os.path.abspath(dirs)
            for filename in filenames:
                if filename.endswith('apk') and not SUCC_MAP.has_key(filename):
                    try:
                        start = time.clock()
                    # subprocess.check_output('notepad.exe test.txt')
                        pkg = os.path.join(abs_dirs,filename)
                        permission_infos = subprocess.check_output('aapt.exe dump permissions '+pkg)
                        used_time = time.clock() - start
                        time_file.write(filename+'|'+str(used_time))
                        time_file.write(os.linesep)
                        total_time += used_time
                        total_num += 1
                        get_permissions_from_pkg(permission_infos,filename)
                        succ_file.write(filename)
                        succ_file.write(os.linesep)
                    except Exception as e:
                        failed_file.write(filename)
                        failed_file.write(os.linesep)


def main():

    # PKG_DIRS = 'G:\\FtpDir\\AndroidTool\\apktool\\'
    PKG_DIRS = 'G:'+os.sep+'FtpDir'+os.sep+'NEW_XIAO_APPS'+os.sep+'APK'+os.sep

    try:
        if not os.path.exists(OUT_DIR):
            os.mkdir(OUT_DIR)
    except:
        return
    if os.path.exists(os.path.join(TOTAL_OUT_DIR,'succ')):
        with open(os.path.join(TOTAL_OUT_DIR,'succ'),'rb') as f:
            for line in f:
                line = line.strip()
                if line:
                    SUCC_MAP[line] = 1

    # get all permissions
    get_all_permissions(PKG_DIRS)

    time_file.write('******************')
    time_file.write(os.linesep)
    time_file.write('total_time : '+str(total_time))
    time_file.write(os.linesep)
    time_file.write('total_num : '+str(total_num))
    time_file.write(os.linesep)
    time_file.close()
    print total_time/total_num
    for key,value in PERMISSION_FREQ.iteritems():
        stat_file.write(key+'|'+str(value))
        stat_file.write(os.linesep)
    stat_file.close()
    # pass

def cmp(x,y):
    if x > y:
        return 1
    elif x < y:
        return -1;
    else:
        return  0

def sort_stat(file_handler):
    result = {}
    from operator import itemgetter

    for line in file_handler:
        line = line.strip()
        if line:
            infos = line.split('|')
            pkg = infos[0]
            feq = infos[1]
            result[pkg] = int(feq)
    tuple = sorted(result.iteritems(),key=itemgetter(1),reverse=True)
    sorted_stat_file_handler = open(sorted_stat_file_name,'wb')
    for item in tuple:
        sorted_stat_file_handler.write(item[0]+'|'+str(item[1]))
        sorted_stat_file_handler.write(os.linesep)
    sorted_stat_file_handler.close()
    # print tuple[0:10]

if __name__ == '__main__':

    main()

    stat_file_r = open(stat_file_name,'rb')

    sort_stat(stat_file_r)
