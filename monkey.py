

import sys

# reload(sys)
# sys.setdefaultencoding('utf-8') # sys.setdefaultencoding('utf-8')


import subprocess
import os
def install_and_monkey(apkname,apkpath,seed,eventscnt):
    print '>>> installing package %s <<<'% apkname
    try:
        print 'adb.exe install -r ' + apkpath
        command_str =  'adb.exe install -r ' + apkpath
        command_str = 'adb.exe install -r ' + apkpath
        install_outputs = subprocess.check_output(command_str,shell=True)
        install_outputs = install_outputs.splitlines()
        print install_outputs
        if len(install_outputs) >= 3 and install_outputs[2] == "Success" :
            print '>>> install done <<<'
            monkey_result_dir = 'monkey_result' + os.sep + apkname
            if(not os.path.isdir(monkey_result_dir)):
                os.makedirs(monkey_result_dir)
            outf = open(monkey_result_dir + os.sep + 'output.txt', 'w')
            #errf = open(monkey_result_dir + os.sep + 'error.txt', 'w')
            print '>>> monkey running package %s with seed %s and results in %s <<<'%(apkname, str(seed).strip(), monkey_result_dir)
            if seed == None:
                monkey_cmd = 'adb.exe  shell monkey -p '+ apkname + " -v -v -v " + str(eventscnt).strip()
            else:
                monkey_cmd = 'adb.exe shell monkey -p ' + apkname + " -v -v -v " + str(eventscnt).strip() + ' -s '+ str(seed).strip()
            retval = subprocess.call(monkey_cmd, stdout=outf, stderr=outf)
            if retval == 0:
                print '>>> monkey done <<<'
            else:
                print '!!! monkey error !!!'
            print '>>> uninstalling package %s <<<'%apkname
            retval = subprocess.call('adb.exe uninstall ' + apkname)
            if retval == 0:
                print '>>> uninstall done <<<'
            else:
                print '!!! uninstall error !!!'
            return 0
        else:
            print '!!! install error !!!'
            return 1
    except subprocess.CalledProcessError as e :
        print str(e)
        print '!!! install error !!!'
        return 1


if __name__ == '__main__':
    apkname = 'signed_com.quiz.twd.main'
    # apkpath ='G:'+os.sep+'FtpDir'+os.sep+'AndroidTool'+os.sep+'apktool'+os.sep+'com.quiz.twd.main.apk'
    apkpath = 'G:\\FtpDir\\AndroidTool\\Auto-sign-tt-v1.1\\Signed\\unsigned_com.quiz.twd.main_signed.apk'
    seed = 13
    eventscnt = 500
    install_and_monkey(apkname,apkpath,seed,eventscnt)