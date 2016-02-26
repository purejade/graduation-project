
#!/usr/bin/env python
# -*- utf-8 -*-
import os
import json

ROOT = 'G:'+os.sep+'FtpDir'+os.sep+'Play Store JSON'+os.sep;
input_file_name = os.path.join(ROOT,'playstore.json')
output_file_name = os.path.join(ROOT,'apps_detail.json')

PKG_DIRS = 'G:'+os.sep+'FtpDir'+os.sep+'PLAY_APP'+os.sep
# OUT_DIRS = 'G:'+os.sep+'FtpDir'+os.sep
finished_app_file = os.path.join(PKG_DIRS,'finished_app_file')

OUT_DIR = 'G:'+os.sep+'FtpDir'+os.sep+'RESULT'+os.sep+'PLAY_APP'+os.sep+'PERMISSIONS'+os.sep

def get_app_detail():
    apps_map = {}
    with open(finished_app_file,'rb') as handler:
        for app_name in handler:
            app_name = app_name.strip()
            if app_name:
                apps_map[app_name] = 1
    output_handler = open(output_file_name,'wb')
    with open(input_file_name,'rb') as handler:
        for line in handler:
            line = line.strip()
            if line:
                lineObject = json.loads(line)
                id_value = lineObject["Url"]
                id_value = id_value[id_value.find('=')+1:] + '.apk'
                if apps_map.has_key(id_value):
                    output_handler.write(line)
                    output_handler.write(os.linesep)
    output_handler.close()

PERMISSION = '' #READ_SMS   SEND_SMS  READ_CONTACTS READ_CALENDAR

permissions = ['READ_SMS','READ_CONTACTS', 'READ_CALENDAR']

def get_appinfo_from_permissions():

    files = os.listdir(OUT_DIR)
    absdir = os.path.abspath(OUT_DIR)

    for file in files:
        with open(absdir+os.sep+file) as handler:
            content = handler.read()
            for permission in permissions:
                if permission in content:
                    f = open(permission+'.txt','a+')
                    f.write(file)
                    f.write(os.linesep)
                    f.close()
    for permission in permissions:
        TMP_MAP = {}
        with open(permission+'.txt','rb') as handler:
            for line in handler:
                line = line.strip()
                if line:
                    TMP_MAP[line] = 1
        f = open(permission,'a+')
        with open(output_file_name,'rb') as handler:
            for line in handler:
                line = line.strip()
                if line:
                    lineObject = json.loads(line)
                    id_value = lineObject["Url"]
                    id_value = id_value[id_value.find('=')+1:]
                    if TMP_MAP.has_key(id_value):
                        f.write(id_value+'|'+json.dumps(lineObject['Description']))
                        f.write(os.linesep)
        f.close()


def main():
    with open(input_file_name,'rb') as handler:
        for line in handler:
            print line
            app_details = json.loads(line)
            print app_details.keys()
            for key,item in app_details.items():
                print key+':'+json.dumps(item)
            break

    pass

def finished_apps():
    PKG_DIRS = 'G:'+os.sep+'FtpDir'+os.sep+'PLAY_APP'+os.sep
    OUT_DIRS = 'G:'+os.sep+'FtpDir'+os.sep
    apps_file = os.path.join(OUT_DIRS,'finished_apps_file')
    handler = open(apps_file,'wb')
    files = os.listdir(PKG_DIRS)
    for file in files:
        file = file.strip()
        if file and file.endswith('apk'):
                handler.write(file);
                handler.write(os.linesep)
    handler.close()

if __name__ == '__main__':

    # main()
    # finished_apps()
    # get_app_detail()
    get_appinfo_from_permissions()